"""Spec 06, cards #15, #17, #21 e #26: evolução pela API, sem exclusão."""

from datetime import datetime, timedelta, timezone

import pytest

from app.models import Assistido, Evolucao, RegistroAuditoria, Usuario


@pytest.fixture
def assistido(api):
    with api.banco() as db:
        pessoa = Assistido(nome_tratamento="Assistido Fictício E")
        pessoa.vincular_profissional(db.session.get(Usuario, api.pessoas["educadora"]))
        db.session.add(pessoa)
        db.session.commit()
        api.assistido_id = pessoa.id
    return api


def _lancar(api, como="educadora", **campos):
    corpo = {"data": "2026-11-10", "area_atuacao": "Pedagógica", "descricao": "Registro fictício.", **campos}
    return api.post(f"/api/assistidos/{api.assistido_id}/evolucoes", json=corpo, como=como)


def _auditoria(api):
    with api.banco() as db:
        return [
            (r.acao, r.recurso, r.recurso_id, r.assistido_id, r.detalhe)
            for r in db.session.scalars(db.select(RegistroAuditoria).order_by(RegistroAuditoria.id))
        ]


def _quantas(api):
    with api.banco() as db:
        return db.session.query(Evolucao).count()


# --- POST ------------------------------------------------------------------------------


def test_lanca_com_autor_profissional_e_momento_do_servidor(assistido):
    antes = datetime.now(timezone.utc) - timedelta(seconds=1)
    resposta = _lancar(assistido, como="assistente")
    assert resposta.status_code == 201
    corpo = resposta.get_json()
    assert corpo["autor_id"] == corpo["profissional_id"] == assistido.pessoas["assistente"]
    assert corpo["autor_nome"] == "Bruna Fictícia"
    assert (corpo["data"], corpo["area_atuacao"], corpo["vigente"]) == ("2026-11-10", "Pedagógica", True)
    assert datetime.fromisoformat(corpo["ocorrido_em"]) >= antes
    assert _auditoria(assistido) == [("criar", "evolucao", corpo["id"], assistido.assistido_id, None)]


@pytest.mark.parametrize(
    "campos, mensagem",
    [
        ({"data": None}, "Informe a data da evolução."),
        ({"data": "ontem"}, "Informe a data da evolução."),
        ({"area_atuacao": " "}, "Informe a área de atuação."),
        ({"area_atuacao": "x" * 81}, "A área de atuação aceita até 80 caracteres."),
        ({"descricao": ""}, "Escreva a descrição da evolução."),
        ({"autor_id": 1}, "Campo não aceito: confira o formulário."),
        ({"ocorrido_em": "2020-01-01T00:00:00-03:00"}, "Campo não aceito: confira o formulário."),
    ],
)
def test_corpo_invalido_devolve_422_sem_gravar(assistido, campos, mensagem):
    resposta = _lancar(assistido, **campos)
    assert resposta.status_code == 422
    assert resposta.get_json() == {"erro": mensagem}
    assert _quantas(assistido) == 0
    assert _auditoria(assistido) == []


def test_assistido_inexistente_devolve_404(assistido):
    resposta = assistido.post("/api/assistidos/9999/evolucoes", json={"data": "2026-11-10", "area_atuacao": "X", "descricao": "Y"})
    assert resposta.status_code == 404
    assert resposta.get_json() == {"erro": "Assistido inexistente."}


def test_sem_token_devolve_401(assistido):
    assert _lancar(assistido, como=None).status_code == 401
    assert assistido.get(f"/api/assistidos/{assistido.assistido_id}/evolucoes", como=None).status_code == 401
    assert _auditoria(assistido) == []


# --- GET --------------------------------------------------------------------------------


def test_lista_em_ordem_cronologica_com_filtros_e_audita(assistido):
    _lancar(assistido, data="2026-11-12", area_atuacao="Social", descricao="terceira")
    _lancar(assistido, data="2026-11-01", descricao="primeira")
    _lancar(assistido, data="2026-11-05", descricao="segunda")
    url = f"/api/assistidos/{assistido.assistido_id}/evolucoes"

    todas = assistido.get(url, como="direcao").get_json()
    assert [e["descricao"] for e in todas] == ["primeira", "segunda", "terceira"]

    periodo = assistido.get(f"{url}?de=2026-11-02&ate=2026-11-12").get_json()
    assert [e["descricao"] for e in periodo] == ["segunda", "terceira"]
    area = assistido.get(f"{url}?area_atuacao=social").get_json()
    assert [e["descricao"] for e in area] == ["terceira"]
    assert _auditoria(assistido)[-1] == ("listar", "evolucao", None, assistido.assistido_id, "area_atuacao=social")


def test_filtro_de_periodo_invertido_devolve_422(assistido):
    url = f"/api/assistidos/{assistido.assistido_id}/evolucoes?de=2026-11-10&ate=2026-11-01"
    resposta = assistido.get(url)
    assert resposta.status_code == 422
    assert resposta.get_json() == {"erro": "A data inicial não pode ser depois da final."}


# --- PATCH (retificação) -----------------------------------------------------------------


def test_retificar_cria_versao_nova_e_preserva_a_anterior(assistido):
    original = _lancar(assistido, descricao="Leitura de palavras.").get_json()
    resposta = assistido.patch(
        f"/api/evolucoes/{original['id']}", json={"descricao": "Leitura de sílabas."}, como="direcao"
    )
    assert resposta.status_code == 201
    nova = resposta.get_json()
    assert nova["id"] != original["id"]
    assert nova["retifica_id"] == original["id"]
    assert (nova["descricao"], nova["data"], nova["area_atuacao"]) == ("Leitura de sílabas.", "2026-11-10", "Pedagógica")
    assert nova["autor_id"] == assistido.pessoas["direcao"]
    assert nova["profissional_id"] == assistido.pessoas["educadora"]

    antiga = assistido.get(f"/api/evolucoes/{original['id']}").get_json()
    assert antiga["descricao"] == "Leitura de palavras." and antiga["vigente"] is False
    assert antiga["retificada_por_id"] == nova["id"]

    lista = assistido.get(f"/api/assistidos/{assistido.assistido_id}/evolucoes").get_json()
    assert [e["id"] for e in lista] == [nova["id"]]
    assert ("retificar", "evolucao", nova["id"], assistido.assistido_id, f"retifica {original['id']}") in _auditoria(assistido)


def test_versao_nova_mostra_as_anteriores(assistido):
    v1 = _lancar(assistido, descricao="v1").get_json()["id"]
    v2 = assistido.patch(f"/api/evolucoes/{v1}", json={"descricao": "v2"}).get_json()["id"]
    v3 = assistido.patch(f"/api/evolucoes/{v2}", json={"descricao": "v3"}).get_json()["id"]
    corpo = assistido.get(f"/api/evolucoes/{v3}").get_json()
    assert [v["descricao"] for v in corpo["versoes_anteriores"]] == ["v2", "v1"]
    assert corpo["retificada_por_id"] is None
    assert _auditoria(assistido)[-1] == ("consultar", "evolucao", v3, assistido.assistido_id, None)


def test_retificar_versao_antiga_devolve_400(assistido):
    v1 = _lancar(assistido).get_json()["id"]
    assistido.patch(f"/api/evolucoes/{v1}", json={"descricao": "corrigida"})
    resposta = assistido.patch(f"/api/evolucoes/{v1}", json={"descricao": "de novo"})
    assert resposta.status_code == 400
    assert resposta.get_json() == {"erro": "Só a versão vigente da evolução pode ser retificada."}
    assert _quantas(assistido) == 2


def test_corrida_na_retificacao_vira_400_e_nao_500(assistido, monkeypatch):
    """Simula a segunda retificação simultânea: passou pela checagem de vigente, mas o
    banco recusa (retifica_id é único). A resposta é 400, sem texto da evolução."""
    v1 = _lancar(assistido, descricao="texto sigiloso fictício").get_json()["id"]
    assistido.patch(f"/api/evolucoes/{v1}", json={"descricao": "primeira correção"})
    monkeypatch.setattr(Evolucao, "vigente", property(lambda self: True))
    resposta = assistido.patch(f"/api/evolucoes/{v1}", json={"descricao": "segunda correção"})
    assert resposta.status_code == 400
    assert resposta.get_json() == {"erro": "Só a versão vigente da evolução pode ser retificada."}
    assert _quantas(assistido) == 2


@pytest.mark.parametrize(
    "corpo, mensagem",
    [
        ({}, "Informe o que muda na retificação."),
        ({"descricao": "  "}, "Escreva a descrição da evolução."),
        ({"assistido_id": 1}, "Campo não aceito: confira o formulário."),
    ],
)
def test_retificacao_invalida_devolve_422(assistido, corpo, mensagem):
    v1 = _lancar(assistido).get_json()["id"]
    resposta = assistido.patch(f"/api/evolucoes/{v1}", json=corpo)
    assert resposta.status_code == 422
    assert resposta.get_json() == {"erro": mensagem}
    assert _quantas(assistido) == 1


def test_evolucao_inexistente_devolve_404(assistido):
    assert assistido.get("/api/evolucoes/9999").status_code == 404
    resposta = assistido.patch("/api/evolucoes/9999", json={"descricao": "x"})
    assert resposta.status_code == 404
    assert resposta.get_json() == {"erro": "Evolução inexistente."}


# --- Sem exclusão (RF26, card #26) ----------------------------------------------------


def test_nao_existe_exclusao_de_evolucao(assistido):
    v1 = _lancar(assistido).get_json()["id"]
    assert assistido.delete(f"/api/evolucoes/{v1}").status_code == 405
    assert assistido.delete(f"/api/assistidos/{assistido.assistido_id}/evolucoes").status_code == 405
    assert assistido.put(f"/api/evolucoes/{v1}", json={"descricao": "x"}).status_code == 405
    assert _quantas(assistido) == 1


# --- Acesso restrito (card #15) -----------------------------------------------------------


def test_com_regra_restritiva_quem_nao_acompanha_recebe_403_em_tudo(assistido, monkeypatch):
    from app.models import Profissional

    v1 = _lancar(assistido).get_json()["id"]
    antes = _auditoria(assistido)
    monkeypatch.setattr(Profissional, "acesso_restrito", True)
    mensagem = {"erro": "Você não tem acesso às evoluções deste assistido."}
    base = f"/api/assistidos/{assistido.assistido_id}/evolucoes"
    for resposta in (
        _lancar(assistido, como="assistente"),
        assistido.get(base, como="assistente"),
        assistido.get(f"/api/evolucoes/{v1}", como="assistente"),
        assistido.patch(f"/api/evolucoes/{v1}", json={"descricao": "x"}, como="assistente"),
    ):
        assert resposta.status_code == 403
        assert resposta.get_json() == mensagem
    assert _quantas(assistido) == 1
    assert _auditoria(assistido) == antes

    assert assistido.get(base, como="educadora").status_code == 200  # acompanha
    assert assistido.get(base, como="direcao").status_code == 200
