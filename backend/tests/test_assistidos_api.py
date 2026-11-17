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


def test_nao_existe_exclusao_de_assistido(api):
    assistido_id = _cadastrar(api).get_json()["id"]
    assert api.delete(f"/api/assistidos/{assistido_id}").status_code == 405
