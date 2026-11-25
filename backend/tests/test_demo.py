"""Acesso rápido de demonstração (DEMO_ACESSO_RAPIDO)."""

import pytest


@pytest.fixture
def demo_ligado(app, db):
    app.config["DEMO_ACESSO_RAPIDO"] = True
    return app


def test_desligado_por_padrao_as_rotas_nao_existem(client, db):
    assert client.get("/api/demo").status_code == 404
    assert client.post("/api/demo/entrar", json={"perfil": "direcao"}).status_code == 404


def test_ligado_informa_os_perfis(demo_ligado, client):
    resposta = client.get("/api/demo")
    assert resposta.status_code == 200
    assert resposta.get_json()["perfis"] == ["direcao", "assistente_social", "equipe_pedagogica"]


@pytest.mark.parametrize("perfil", ["direcao", "assistente_social", "equipe_pedagogica"])
def test_entra_como_cada_perfil_com_a_carga_ficticia(demo_ligado, client, perfil):
    resposta = client.post("/api/demo/entrar", json={"perfil": perfil})
    assert resposta.status_code == 200
    dados = resposta.get_json()
    assert dados["perfil"] == perfil
    assert dados["token"]
    # O token vale nas rotas protegidas.
    eu = client.get("/api/reunioes", headers={"Authorization": "Bearer " + dados["token"]})
    assert eu.status_code == 200


def test_segunda_entrada_nao_duplica_a_carga(demo_ligado, client, db):
    from app.models import Usuario

    client.post("/api/demo/entrar", json={"perfil": "direcao"})
    client.post("/api/demo/entrar", json={"perfil": "assistente_social"})
    total = len(db.session.scalars(db.select(Usuario)).all())
    client.post("/api/demo/entrar", json={"perfil": "equipe_pedagogica"})
    assert len(db.session.scalars(db.select(Usuario)).all()) == total


def test_perfil_invalido(demo_ligado, client):
    assert client.post("/api/demo/entrar", json={"perfil": "admin"}).status_code == 422
