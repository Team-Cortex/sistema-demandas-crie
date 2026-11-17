"""Spec 01 §1, card #14: login e logout."""

from datetime import datetime, timezone

import pytest
from flask_jwt_extended import decode_token

SENHA = "senha-ficticia-1"  # a mesma da fixture api (conftest)
RECUSADA = {"erro": "E-mail ou senha inválidos."}


def entrar(api, email, senha=SENHA, **kwargs):
    return api.client.post("/api/auth/login", json={"email": email, "senha": senha}, **kwargs)


def test_login_certo_devolve_token_perfil_e_usuario(api):
    resposta = entrar(api, "assistente@exemplo.test")
    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert corpo["perfil"] == "assistente_social"
    assert corpo["usuario"] == {
        "id": api.pessoas["assistente"],
        "nome": "Bruna Fictícia",
        "perfil": "assistente_social",
    }
    assert SENHA not in resposta.get_data(as_text=True)


def test_token_tem_sub_perfil_e_expira_em_30_minutos(api):
    token = entrar(api, "direcao@exemplo.test").get_json()["token"]
    with api.banco():
        dados = decode_token(token)
    assert dados["sub"] == str(api.pessoas["direcao"])
    assert dados["perfil"] == "direcao"
    assert dados["exp"] - dados["iat"] == 30 * 60
    assert dados["jti"]


def test_email_e_comparado_sem_maiuscula_e_espaco(api):
    assert entrar(api, "  Direcao@Exemplo.TEST ").status_code == 200


@pytest.mark.parametrize(
    "email, senha",
    [
        ("assistente@exemplo.test", "senha-errada-1"),
        ("ninguem@exemplo.test", SENHA),
        ("inativa@exemplo.test", SENHA),
    ],
)
def test_recusa_com_a_mesma_mensagem_sem_revelar_o_email(api, email, senha):
    resposta = entrar(api, email, senha)
    assert resposta.status_code == 401
    assert resposta.get_json() == RECUSADA


@pytest.mark.parametrize(
    "corpo",
    [
        {"email": "direcao@exemplo.test", "senha": ""},
        {"email": "", "senha": SENHA},
        {"email": "direcao@exemplo.test"},
        {"email": "  ", "senha": "  "},
        {"email": 123, "senha": SENHA},
        {},
        [],
    ],
)
def test_corpo_incompleto_devolve_422(api, corpo):
    resposta = api.client.post("/api/auth/login", json=corpo)
    assert resposta.status_code == 422
    assert resposta.get_json() == {"erro": "Informe e-mail e senha."}


def test_sem_corpo_devolve_422(api):
    resposta = api.client.post("/api/auth/login", data="não é json", content_type="text/plain")
    assert resposta.status_code == 422
    assert resposta.get_json() == {"erro": "Informe e-mail e senha."}


def test_token_do_login_abre_rota_protegida(api):
    from flask import Blueprint, jsonify

    from app.routes.sessao import exigir_login, usuario_atual

    bp = exigir_login(Blueprint("_prova_login", __name__))
    bp.get("/_prova_login")(lambda: jsonify({"nome": usuario_atual().nome}))
    api.app.register_blueprint(bp, url_prefix="/api")

    token = entrar(api, "educadora@exemplo.test").get_json()["token"]
    resposta = api.client.get("/api/_prova_login", headers={"Authorization": f"Bearer {token}"})
    assert resposta.get_json() == {"nome": "Carlos Fictício"}


def test_login_e_publico_mas_get_nao_existe(api):
    assert api.client.get("/api/auth/login").status_code == 405


def test_momento_de_emissao_e_agora(api):
    antes = int(datetime.now(timezone.utc).timestamp()) - 1
    token = entrar(api, "direcao@exemplo.test").get_json()["token"]
    with api.banco():
        assert decode_token(token)["iat"] >= antes
