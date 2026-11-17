"""Spec 01, cards #14 e #16: rota protegida exige token válido e conta ativa."""

from datetime import timedelta

import pytest
from flask import Blueprint, jsonify

from app.routes.sessao import exigir_login, usuario_atual


@pytest.fixture
def protegida(api):
    bp = exigir_login(Blueprint("_prova_sessao", __name__))

    @bp.get("/_prova_sessao")
    def quem_sou():
        usuario = usuario_atual()
        return jsonify({"id": usuario.id, "perfil": usuario.perfil})

    api.app.register_blueprint(bp, url_prefix="/api")
    return api


def test_token_valido_chega_na_rota_com_o_usuario_do_banco(protegida):
    resposta = protegida.get("/api/_prova_sessao", como="assistente")
    assert resposta.status_code == 200
    assert resposta.get_json() == {"id": protegida.pessoas["assistente"], "perfil": "assistente_social"}


def test_sem_token_devolve_401(protegida):
    resposta = protegida.get("/api/_prova_sessao", como=None)
    assert resposta.status_code == 401
    assert resposta.get_json() == {"erro": "Entre no sistema para continuar."}


@pytest.mark.parametrize("cabecalho", ["Bearer abc.def.ghi", "Bearer nada"])
def test_token_malformado_devolve_401(protegida, cabecalho):
    resposta = protegida.get("/api/_prova_sessao", como=None, headers={"Authorization": cabecalho})
    assert resposta.status_code == 401
    assert resposta.get_json() == {"erro": "Sessão inválida. Entre de novo."}


def test_token_assinado_com_outra_chave_devolve_401(protegida):
    import jwt as pyjwt

    falso = pyjwt.encode({"sub": str(protegida.pessoas["direcao"]), "type": "access"}, "outra-chave-qualquer-com-32-bytes!!")
    resposta = protegida.get("/api/_prova_sessao", como=None, headers={"Authorization": f"Bearer {falso}"})
    assert resposta.status_code == 401
    assert resposta.get_json() == {"erro": "Sessão inválida. Entre de novo."}


def test_token_expirado_devolve_401(protegida):
    token = protegida.token("direcao", expires_delta=timedelta(seconds=-1))
    resposta = protegida.get("/api/_prova_sessao", como=None, headers={"Authorization": f"Bearer {token}"})
    assert resposta.status_code == 401
    assert resposta.get_json() == {"erro": "Sessão expirada. Entre de novo."}


def test_conta_inativa_perde_a_sessao(protegida):
    resposta = protegida.get("/api/_prova_sessao", como="inativa")
    assert resposta.status_code == 401
    assert resposta.get_json() == {"erro": "Sessão encerrada. Entre de novo."}


def test_desativar_derruba_o_token_ja_emitido(protegida):
    from app.models import Usuario

    token = protegida.token("educadora")
    with protegida.banco() as db:
        db.session.get(Usuario, protegida.pessoas["educadora"]).ativo = False
        db.session.commit()
    resposta = protegida.get("/api/_prova_sessao", como=None, headers={"Authorization": f"Bearer {token}"})
    assert resposta.status_code == 401


def test_token_de_usuario_inexistente_devolve_401(protegida, usuario_autenticado):
    resposta = protegida.get("/api/_prova_sessao", como=None, headers=usuario_autenticado)
    assert resposta.status_code == 401
    assert resposta.get_json() == {"erro": "Sessão encerrada. Entre de novo."}


def test_token_de_id_que_nao_existe_mais_devolve_401(protegida):
    from flask_jwt_extended import create_access_token

    with protegida.banco():
        token = create_access_token(identity="9999", additional_claims={"perfil": "direcao"})
    resposta = protegida.get("/api/_prova_sessao", como=None, headers={"Authorization": f"Bearer {token}"})
    assert resposta.status_code == 401
    assert resposta.get_json() == {"erro": "Sessão encerrada. Entre de novo."}


def test_perfil_vem_do_banco_e_nao_do_token(protegida):
    from app.extensions import db as _db
    from app.models import Usuario

    token = protegida.token("assistente")
    with protegida.banco():
        _db.session.execute(
            Usuario.__table__.update()
            .where(Usuario.__table__.c.id == protegida.pessoas["assistente"])
            .values(perfil="equipe_pedagogica")
        )
        _db.session.commit()
    resposta = protegida.get("/api/_prova_sessao", como=None, headers={"Authorization": f"Bearer {token}"})
    assert resposta.get_json()["perfil"] == "equipe_pedagogica"


def test_preflight_do_cors_nao_exige_token(protegida):
    resposta = protegida.client.options("/api/_prova_sessao")
    assert resposta.status_code == 200
