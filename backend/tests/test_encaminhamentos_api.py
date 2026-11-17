"""Spec 07, cards #15, #17 e #22: encaminhamento pela API."""

from datetime import date

import pytest

from app.models import (
    Assistido,
    Demanda,
    Encaminhamento,
    Prioridade,
    RegistroAuditoria,
    Reuniao,
    Setor,
    Usuario,
)


@pytest.fixture
def base(api):
    with api.banco() as db:
        educadora = db.session.get(Usuario, api.pessoas["educadora"])
        assistido = Assistido(nome_tratamento="Assistido Fictício G")
        assistido.vincular_profissional(educadora)
        outro = Assistido(nome_tratamento="Assistido Fictício H")
        reuniao = Reuniao(data=date(2026, 11, 3), setor=Setor.SAUDE, participantes=[educadora])
        demanda = Demanda.abrir(educadora, descricao="Vaga no CAPSi (fictício).", prioridade=Prioridade.ALTA,
                                prazo=date(2026, 12, 1), responsavel=educadora, reuniao=reuniao,
                                assistido=assistido)
        sem_assistido = Demanda.abrir(educadora, descricao="Material da turma (fictício).",
                                      prioridade=Prioridade.BAIXA, prazo=date(2026, 12, 1),
                                      responsavel=educadora, reuniao=reuniao)
        db.session.add_all([assistido, outro, reuniao, demanda, sem_assistido])
        db.session.commit()
        api.ids = {
            "assistido": assistido.id,
            "outro": outro.id,
            "demanda": demanda.id,
            "sem_assistido": sem_assistido.id,
        }
    return api


def _registrar(api, como="educadora", **campos):
    corpo = {"destino": "CAPSi (fictício)", "data": "2026-11-10", **campos}
    return api.post("/api/encaminhamentos", json=corpo, como=como)


def _auditoria(api):
    with api.banco() as db:
        return [
            (r.acao, r.recurso, r.recurso_id, r.assistido_id, r.detalhe)
            for r in db.session.scalars(db.select(RegistroAuditoria).order_by(RegistroAuditoria.id))
        ]


def _quantos(api):
    with api.banco() as db:
        return db.session.query(Encaminhamento).count()


# --- POST ---------------------------------------------------------------------------------


def test_registra_ligado_ao_assistido_com_responsavel_do_token(base):
    resposta = _registrar(base, assistido_id=base.ids["assistido"], observacao=" Levar laudo. ")
    assert resposta.status_code == 201
    corpo = resposta.get_json()
    assert (corpo["assistido_id"], corpo["demanda_id"]) == (base.ids["assistido"], None)
    assert corpo["responsavel_id"] == base.pessoas["educadora"]
    assert corpo["observacao"] == "Levar laudo."
    assert corpo["pendente"] is True and corpo["desfecho"] is None
    assert _auditoria(base) == [("criar", "encaminhamento", corpo["id"], base.ids["assistido"], None)]


def test_pela_demanda_herda_o_assistido(base):
    corpo = _registrar(base, demanda_id=base.ids["demanda"]).get_json()
    assert (corpo["demanda_id"], corpo["assistido_id"]) == (base.ids["demanda"], base.ids["assistido"])


def test_demanda_sem_assistido_fica_sem_assistido(base):
    corpo = _registrar(base, demanda_id=base.ids["sem_assistido"]).get_json()
    assert corpo["assistido_id"] is None


@pytest.mark.parametrize(
    "campos, mensagem",
    [
        ({}, "Informe o assistido ou a demanda do encaminhamento."),
        ({"assistido_id": None, "demanda_id": None}, "Informe o assistido ou a demanda do encaminhamento."),
        ({"assistido_id": 9999}, "Assistido inexistente."),
        ({"demanda_id": 9999}, "Demanda inexistente."),
        ({"assistido_id": "x"}, "Assistido inexistente."),
        ({"assistido_id": 1, "destino": "  "}, "Informe o destino do encaminhamento."),
        ({"assistido_id": 1, "destino": "x" * 201}, "Informe o destino do encaminhamento."),
        ({"assistido_id": 1, "data": None}, "Informe a data do encaminhamento."),
        ({"assistido_id": 1, "desfecho": "já resolvido"}, "Campo não aceito: confira o formulário."),
    ],
)
def test_corpo_invalido_devolve_422_sem_gravar(base, campos, mensagem):
    if campos.get("assistido_id") == 1:
        campos["assistido_id"] = base.ids["assistido"]
    resposta = _registrar(base, **campos)
    assert resposta.status_code == 422
    assert resposta.get_json() == {"erro": mensagem}
    assert _quantos(base) == 0
    assert _auditoria(base) == []


def test_demanda_de_outro_assistido_devolve_422(base):
    resposta = _registrar(base, assistido_id=base.ids["outro"], demanda_id=base.ids["demanda"])
    assert resposta.status_code == 422
    assert resposta.get_json() == {"erro": "A demanda informada é de outro assistido."}


def test_sem_token_devolve_401(base):
    assert _registrar(base, como=None, assistido_id=base.ids["assistido"]).status_code == 401
    assert base.get("/api/encaminhamentos", como=None).status_code == 401
    assert _auditoria(base) == []


# --- GET -----------------------------------------------------------------------------------


def _com_tres(api):
    ids = []
    for dia, chave in (("2026-11-12", "assistido"), ("2026-11-02", "outro"), ("2026-11-07", "assistido")):
        ids.append(_registrar(api, assistido_id=api.ids[chave], data=dia).get_json()["id"])
    with api.banco() as db:
        resolvido = db.session.get(Encaminhamento, ids[2])
        resolvido.registrar_desfecho("Consulta marcada.", db.session.get(Usuario, api.pessoas["educadora"]))
        db.session.commit()
    return ids


def test_lista_do_mais_antigo_e_filtra_pendentes(base):
    ids = _com_tres(base)
    todos = base.get("/api/encaminhamentos").get_json()
    assert [e["data"] for e in todos] == ["2026-11-02", "2026-11-07", "2026-11-12"]

    pendentes = base.get("/api/encaminhamentos/pendentes", como="assistente").get_json()
    assert {e["id"] for e in pendentes} == {ids[0], ids[1]}
    assert base.get("/api/encaminhamentos?pendentes=true").get_json() == pendentes
    assert _auditoria(base)[-1] == ("listar", "encaminhamento", None, None, "pendentes=True")


def test_filtra_por_assistido_e_audita_o_assistido(base):
    _com_tres(base)
    corpo = base.get(f"/api/encaminhamentos?assistido_id={base.ids['outro']}").get_json()
    assert [e["assistido_id"] for e in corpo] == [base.ids["outro"]]
    assert _auditoria(base)[-1][3] == base.ids["outro"]


@pytest.mark.parametrize("url", ["/api/encaminhamentos", "/api/encaminhamentos/pendentes"])
def test_filtrar_por_assistido_inexistente_devolve_404_sem_auditoria(base, url):
    resposta = base.get(f"{url}?assistido_id=9999")
    assert resposta.status_code == 404
    assert resposta.get_json() == {"erro": "Assistido inexistente."}
    assert _auditoria(base) == []


def test_consulta_um_e_audita(base):
    encaminhamento_id = _registrar(base, assistido_id=base.ids["assistido"]).get_json()["id"]
    resposta = base.get(f"/api/encaminhamentos/{encaminhamento_id}", como="direcao")
    assert resposta.status_code == 200
    assert resposta.get_json()["destino"] == "CAPSi (fictício)"
    assert _auditoria(base)[-1] == ("consultar", "encaminhamento", encaminhamento_id, base.ids["assistido"], None)


def test_inexistente_devolve_404(base):
    resposta = base.get("/api/encaminhamentos/9999")
    assert resposta.status_code == 404
    assert resposta.get_json() == {"erro": "Encaminhamento inexistente."}


# --- PATCH desfecho --------------------------------------------------------------------


@pytest.mark.parametrize("sufixo", ["/desfecho", ""])
def test_registra_o_desfecho_com_autor_e_momento_uma_vez(base, sufixo):
    encaminhamento_id = _registrar(base, assistido_id=base.ids["assistido"]).get_json()["id"]
    url = f"/api/encaminhamentos/{encaminhamento_id}{sufixo}"
    resposta = base.patch(url, json={"desfecho": " Consulta marcada para dezembro. "}, como="assistente")
    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert corpo["desfecho"] == "Consulta marcada para dezembro."
    assert corpo["desfecho_autor_id"] == base.pessoas["assistente"]
    assert corpo["desfecho_em"].endswith("-03:00")
    assert corpo["pendente"] is False
    assert _auditoria(base)[-1] == (
        "registrar_desfecho", "encaminhamento", encaminhamento_id, base.ids["assistido"], None
    )

    segundo = base.patch(url, json={"desfecho": "Outro desfecho."})
    assert segundo.status_code == 400
    assert segundo.get_json() == {"erro": "Este encaminhamento já tem desfecho registrado."}
    assert base.get(url.replace("/desfecho", "")).get_json()["desfecho"] == "Consulta marcada para dezembro."


@pytest.mark.parametrize("corpo", [{}, {"desfecho": "   "}, {"desfecho": None}])
def test_desfecho_vazio_devolve_422(base, corpo):
    encaminhamento_id = _registrar(base, assistido_id=base.ids["assistido"]).get_json()["id"]
    resposta = base.patch(f"/api/encaminhamentos/{encaminhamento_id}/desfecho", json=corpo)
    assert resposta.status_code == 422
    assert resposta.get_json() == {"erro": "Escreva o desfecho do encaminhamento."}


def test_patch_nao_muda_outros_campos(base):
    encaminhamento_id = _registrar(base, assistido_id=base.ids["assistido"]).get_json()["id"]
    resposta = base.patch(f"/api/encaminhamentos/{encaminhamento_id}", json={"destino": "Outro lugar"})
    assert resposta.status_code == 422


def test_desfecho_some_da_lista_de_pendentes(base):
    encaminhamento_id = _registrar(base, assistido_id=base.ids["assistido"]).get_json()["id"]
    base.patch(f"/api/encaminhamentos/{encaminhamento_id}/desfecho", json={"desfecho": "Resolvido."})
    assert base.get("/api/encaminhamentos/pendentes").get_json() == []


def test_desfecho_em_inexistente_devolve_404(base):
    assert base.patch("/api/encaminhamentos/9999/desfecho", json={"desfecho": "x"}).status_code == 404


def test_nao_existe_exclusao_de_encaminhamento(base):
    encaminhamento_id = _registrar(base, assistido_id=base.ids["assistido"]).get_json()["id"]
    assert base.delete(f"/api/encaminhamentos/{encaminhamento_id}").status_code == 405
    assert _quantos(base) == 1


# --- Acesso restrito (card #15) --------------------------------------------------------


def test_com_regra_restritiva_quem_nao_acompanha_nao_registra_nem_ve(base, monkeypatch):
    from app.models import Profissional

    visivel = _registrar(base, assistido_id=base.ids["assistido"]).get_json()["id"]
    sem_pessoa = _registrar(base, demanda_id=base.ids["sem_assistido"]).get_json()["id"]
    monkeypatch.setattr(Profissional, "acesso_restrito", True)

    negado = _registrar(base, como="assistente", assistido_id=base.ids["assistido"])
    assert negado.status_code == 403
    assert negado.get_json() == {"erro": "Você não tem acesso aos dados deste assistido."}
    assert base.get(f"/api/encaminhamentos/{visivel}", como="assistente").status_code == 403

    da_assistente = base.get("/api/encaminhamentos", como="assistente").get_json()
    assert [e["id"] for e in da_assistente] == [sem_pessoa]
    da_educadora = base.get("/api/encaminhamentos", como="educadora").get_json()
    assert {e["id"] for e in da_educadora} == {visivel, sem_pessoa}
