"""Spec 05 §3, card #17: a direção consulta a auditoria."""

import pytest

from app.models import Assistido, Usuario
from app.services.auditoria import AuditoriaService


@pytest.fixture
def com_registros(api):
    with api.banco() as db:
        assistido = Assistido(nome_tratamento="Fictício Y")
        db.session.add(assistido)
        db.session.commit()
        assistente = db.session.get(Usuario, api.pessoas["assistente"])
        direcao = db.session.get(Usuario, api.pessoas["direcao"])
        AuditoriaService.registrar_leitura(assistente, "consultar", "assistido", assistido.id, assistido.id)
        AuditoriaService.registrar_leitura(assistente, "listar", "assistido")
        AuditoriaService.registrar_leitura(direcao, "emitir", "relatorio_demandas", detalhe="de=2026-10-01")
        api.assistido_id = assistido.id
    return api


def test_direcao_ve_do_mais_recente_para_o_mais_antigo(com_registros):
    resposta = com_registros.get("/api/auditoria")
    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert corpo["total"] == 3 and corpo["pagina"] == 1 and corpo["por_pagina"] == 50
    assert [i["acao"] for i in corpo["itens"]] == ["emitir", "listar", "consultar"]
    item = corpo["itens"][-1]
    assert item["autor_nome"] == "Bruna Fictícia"
    assert item["assistido_id"] == com_registros.assistido_id
    assert item["ocorrido_em"].endswith("-03:00")


def test_filtra_por_assistido_autor_recurso_e_acao(com_registros):
    api = com_registros
    por_assistido = api.get(f"/api/auditoria?assistido_id={api.assistido_id}").get_json()
    assert [i["acao"] for i in por_assistido["itens"]] == ["consultar"]
    por_autor = api.get(f"/api/auditoria?autor_id={api.pessoas['direcao']}").get_json()
    assert [i["recurso"] for i in por_autor["itens"]] == ["relatorio_demandas"]
    assert api.get("/api/auditoria?recurso=assistido&acao=listar").get_json()["total"] == 1


def test_pagina(com_registros):
    corpo = com_registros.get("/api/auditoria?por_pagina=2&pagina=2").get_json()
    assert corpo["total"] == 3
    assert [i["acao"] for i in corpo["itens"]] == ["consultar"]


@pytest.mark.parametrize(
    "consulta, mensagem",
    [
        ("de=16/11/2026", "Use datas no formato AAAA-MM-DD."),
        ("de=2026-11-20&ate=2026-11-01", "A data inicial não pode ser depois da final."),
        ("por_pagina=500", "Use por_pagina de 1 a 200."),
        ("pagina=0", "A página começa em 1."),
        ("acao=apagar", "Ação desconhecida."),
    ],
)
def test_filtro_invalido_devolve_422(com_registros, consulta, mensagem):
    resposta = com_registros.get(f"/api/auditoria?{consulta}")
    assert resposta.status_code == 422
    assert resposta.get_json() == {"erro": mensagem}


@pytest.mark.parametrize("quem", ["assistente", "educadora"])
def test_profissional_recebe_403(com_registros, quem):
    resposta = com_registros.get("/api/auditoria", como=quem)
    assert resposta.status_code == 403
    assert resposta.get_json() == {"erro": "Só a direção consulta a auditoria."}


def test_sem_token_recebe_401(com_registros):
    assert com_registros.get("/api/auditoria", como=None).status_code == 401


# --- Spec 05 §2, regras 1 e 2: sem registro, sem operação --------------------------


def _quebrar_auditoria(monkeypatch):
    from app.models import auditoria

    def recusa(self, **campos):
        raise RuntimeError("auditoria indisponível")

    monkeypatch.setattr(auditoria.RegistroAuditoria, "__init__", recusa)


def test_escrita_sem_auditoria_nao_grava_a_operacao(api, monkeypatch):
    _quebrar_auditoria(monkeypatch)
    resposta = api.post("/api/assistidos", json={"nome_tratamento": "Assistido Fictício W"})
    assert resposta.status_code == 500
    assert resposta.get_json() == {"erro": "Não foi possível concluir a operação."}
    with api.banco() as db:
        assert db.session.query(Assistido).count() == 0


def test_leitura_sem_auditoria_nao_entrega_o_dado(api, monkeypatch):
    with api.banco() as db:
        db.session.add(Assistido(nome_tratamento="Assistido Fictício V"))
        db.session.commit()
    _quebrar_auditoria(monkeypatch)
    resposta = api.get("/api/assistidos")
    assert resposta.status_code == 500
    assert "Fictício V" not in resposta.get_data(as_text=True)


@pytest.mark.parametrize("metodo", ["post", "patch", "put", "delete"])
def test_nao_ha_rota_de_escrever_ou_apagar(com_registros, metodo):
    assert getattr(com_registros, metodo)("/api/auditoria").status_code == 405
