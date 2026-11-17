"""Spec 03, cards #17 e #20: /api/assistidos com auditoria."""

import pytest

from app.models import Assistido, RegistroAuditoria


def _auditoria(api):
    with api.banco() as db:
        return [
            (r.autor_id, r.acao, r.recurso, r.recurso_id, r.assistido_id, r.detalhe)
            for r in db.session.scalars(db.select(RegistroAuditoria).order_by(RegistroAuditoria.id))
        ]


def _cadastrar(api, nome="Assistido Fictício R", como="assistente"):
    return api.post("/api/assistidos", json={"nome_tratamento": nome}, como=como)


# --- POST e PATCH/PUT -----------------------------------------------------------------


def test_cadastra_so_com_nome_de_tratamento_e_audita(api):
    resposta = _cadastrar(api, "  Assistido Fictício R  ")
    assert resposta.status_code == 201
    corpo = resposta.get_json()
    assert corpo["nome_tratamento"] == "Assistido Fictício R"
    assert (corpo["demandas"], corpo["evolucoes"], corpo["encaminhamentos"]) == ([], [], [])
    assert _auditoria(api) == [
        (api.pessoas["assistente"], "criar", "assistido", corpo["id"], corpo["id"], None)
    ]


@pytest.mark.parametrize(
    "corpo, mensagem",
    [
        ({"nome_tratamento": "X", "data_nascimento": "2015-01-01"}, "Este dado ainda não foi autorizado pela instituição."),
        ({"data_nascimento": "2015-01-01"}, "Este dado ainda não foi autorizado pela instituição."),
        ({"nome_tratamento": "X", "diagnostico": "..."}, "Este dado ainda não foi autorizado pela instituição."),
        ({"nome_tratamento": "  "}, "Informe o nome de tratamento."),
        ({}, "Informe o nome de tratamento."),
        ({"nome_tratamento": "x" * 121}, "O nome de tratamento aceita até 120 caracteres."),
    ],
)
def test_dado_nao_autorizado_ou_invalido_devolve_422_sem_gravar(api, corpo, mensagem):
    resposta = api.post("/api/assistidos", json=corpo)
    assert resposta.status_code == 422
    assert resposta.get_json() == {"erro": mensagem}
    with api.banco() as db:
        assert db.session.query(Assistido).count() == 0
    assert _auditoria(api) == []


@pytest.mark.parametrize("metodo", ["patch", "put"])
def test_altera_o_nome_e_audita(api, metodo):
    assistido_id = _cadastrar(api).get_json()["id"]
    resposta = getattr(api, metodo)(
        f"/api/assistidos/{assistido_id}", json={"nome_tratamento": "Assistido Fictício S"}, como="educadora"
    )
    assert resposta.status_code == 200
    assert resposta.get_json()["nome_tratamento"] == "Assistido Fictício S"
    assert _auditoria(api)[-1] == (
        api.pessoas["educadora"], "alterar", "assistido", assistido_id, assistido_id, None
    )


def test_alterar_com_campo_nao_autorizado_devolve_422(api):
    assistido_id = _cadastrar(api).get_json()["id"]
    resposta = api.patch(f"/api/assistidos/{assistido_id}", json={"contato": "(00) 0000-0000"})
    assert resposta.status_code == 422
    assert resposta.get_json() == {"erro": "Este dado ainda não foi autorizado pela instituição."}


def test_alterar_inexistente_devolve_404_sem_auditoria(api):
    resposta = api.patch("/api/assistidos/9999", json={"nome_tratamento": "X"})
    assert resposta.status_code == 404
    assert resposta.get_json() == {"erro": "Assistido inexistente."}
    assert _auditoria(api) == []


def test_sem_token_devolve_401_sem_auditoria(api):
    assert _cadastrar(api, como=None).status_code == 401
    assert _auditoria(api) == []


# --- GET ------------------------------------------------------------------------------


def test_lista_em_ordem_alfabetica_e_audita_a_consulta(api):
    for nome in ("Assistido Fictício B", "Assistido Fictício A"):
        _cadastrar(api, nome)
    resposta = api.get("/api/assistidos", como="educadora")
    assert resposta.status_code == 200
    assert [a["nome_tratamento"] for a in resposta.get_json()] == ["Assistido Fictício A", "Assistido Fictício B"]
    assert set(resposta.get_json()[0]) == {"id", "nome_tratamento"}
    assert _auditoria(api)[-1] == (api.pessoas["educadora"], "listar", "assistido", None, None, None)


def test_busca_por_nome_nao_guarda_o_texto_na_auditoria(api):
    _cadastrar(api, "Assistido Fictício A")
    _cadastrar(api, "Outra Pessoa Fictícia")
    corpo = api.get("/api/assistidos?busca=outra").get_json()
    assert [a["nome_tratamento"] for a in corpo] == ["Outra Pessoa Fictícia"]
    detalhe = _auditoria(api)[-1][-1]
    assert detalhe == "busca=*"


def test_consulta_traz_ids_da_ficha_e_audita(api):
    assistido_id = _cadastrar(api).get_json()["id"]
    resposta = api.get(f"/api/assistidos/{assistido_id}", como="educadora")
    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert set(corpo) == {
        "id", "nome_tratamento", "ativo", "criado_em", "demandas", "evolucoes", "encaminhamentos",
    }
    assert _auditoria(api)[-1] == (
        api.pessoas["educadora"], "consultar", "assistido", assistido_id, assistido_id, None
    )


def test_leitura_sem_token_nao_grava_auditoria(api):
    assistido_id = _cadastrar(api).get_json()["id"]
    antes = _auditoria(api)
    assert api.get(f"/api/assistidos/{assistido_id}", como=None).status_code == 401
    assert api.get("/api/assistidos", como=None).status_code == 401
    assert _auditoria(api) == antes


def test_consultar_inexistente_devolve_404_sem_auditoria(api):
    assert api.get("/api/assistidos/9999").status_code == 404
    assert _auditoria(api) == []


# --- GET /<id>/ficha --------------------------------------------------------------------


@pytest.fixture
def com_ficha(api):
    """Um assistido com demanda, evolução retificada e encaminhamento, todos fictícios."""
    from datetime import date

    from app.models import Demanda, Encaminhamento, Evolucao, Prioridade, Reuniao, Setor, Usuario

    with api.banco() as db:
        educadora = db.session.get(Usuario, api.pessoas["educadora"])
        assistido = Assistido(nome_tratamento="Assistido Fictício F")
        assistido.vincular_profissional(educadora)
        reuniao = Reuniao(data=date(2026, 11, 3), setor=Setor.PEDAGOGICO, participantes=[educadora])
        demanda = Demanda.abrir(educadora, descricao="Pedir material adaptado (fictício).",
                                prioridade=Prioridade.BAIXA, prazo=date(2026, 12, 1),
                                responsavel=educadora, reuniao=reuniao, assistido=assistido)
        original = Evolucao.lancar(educadora, assistido=assistido, data=date(2026, 11, 4),
                                   area_atuacao="Pedagógica", descricao="Registro fictício original.")
        db.session.add_all([assistido, reuniao, demanda, original])
        db.session.flush()
        db.session.add(original.retificar(educadora, descricao="Registro fictício corrigido."))
        db.session.add(Encaminhamento(assistido=assistido, destino="CAPSi (fictício)",
                                      data=date(2026, 11, 5), responsavel=educadora))
        db.session.commit()
        api.assistido_id = assistido.id
    return api


def test_ficha_reune_demandas_evolucoes_vigentes_e_encaminhamentos(com_ficha):
    resposta = com_ficha.get(f"/api/assistidos/{com_ficha.assistido_id}/ficha", como="assistente")
    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert corpo["assistido"]["nome_tratamento"] == "Assistido Fictício F"
    assert [p["nome"] for p in corpo["profissionais"]] == ["Carlos Fictício"]
    assert [d["descricao"] for d in corpo["demandas"]] == ["Pedir material adaptado (fictício)."]
    assert [e["descricao"] for e in corpo["evolucoes"]] == ["Registro fictício corrigido."]
    assert corpo["evolucoes"][0]["retifica_id"] is not None
    assert [e["destino"] for e in corpo["encaminhamentos"]] == ["CAPSi (fictício)"]
    assert _auditoria(com_ficha)[-1] == (
        com_ficha.pessoas["assistente"], "consultar", "assistido",
        com_ficha.assistido_id, com_ficha.assistido_id, "ficha",
    )


def test_ficha_vazia_traz_listas_vazias(api):
    assistido_id = _cadastrar(api).get_json()["id"]
    corpo = api.get(f"/api/assistidos/{assistido_id}/ficha").get_json()
    assert (corpo["profissionais"], corpo["demandas"], corpo["evolucoes"], corpo["encaminhamentos"]) == (
        [], [], [], [],
    )


def test_com_regra_restritiva_so_quem_acompanha_ve_a_ficha(com_ficha, monkeypatch):
    from app.models import Profissional

    monkeypatch.setattr(Profissional, "acesso_restrito", True)
    antes = _auditoria(com_ficha)
    url = f"/api/assistidos/{com_ficha.assistido_id}/ficha"

    negada = com_ficha.get(url, como="assistente")
    assert negada.status_code == 403
    assert negada.get_json() == {"erro": "Você não tem acesso às evoluções deste assistido."}
    assert _auditoria(com_ficha) == antes

    assert com_ficha.get(url, como="educadora").status_code == 200  # acompanha
    assert com_ficha.get(url, como="direcao").status_code == 200


def test_ficha_continua_depois_que_quem_acompanha_muda_de_perfil(com_ficha):
    educadora = com_ficha.pessoas["educadora"]
    assert com_ficha.patch(f"/api/usuarios/{educadora}", json={"perfil": "direcao"}).status_code == 200
    resposta = com_ficha.get(f"/api/assistidos/{com_ficha.assistido_id}/ficha")
    assert resposta.status_code == 200
    assert resposta.get_json()["profissionais"] == [{"id": educadora, "nome": "Carlos Fictício"}]


def test_ficha_de_inexistente_devolve_404(api):
    assert api.get("/api/assistidos/9999/ficha").status_code == 404


def test_nao_existe_exclusao_de_assistido(api):
    assistido_id = _cadastrar(api).get_json()["id"]
    assert api.delete(f"/api/assistidos/{assistido_id}").status_code == 405
