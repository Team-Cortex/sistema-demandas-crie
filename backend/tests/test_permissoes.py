"""Card #15: perfil verificado por rota, 403 no formato único."""

import pytest
from flask import Blueprint, jsonify

from app.models import AssistenteSocial, Direcao, EquipePedagogica
from app.routes.sessao import exige_permissao, exigir_login

PERMISSOES_DA_DIRECAO = ["pode_gerir_usuarios", "pode_emitir_relatorio", "pode_consultar_auditoria"]


def _pessoa(classe, **campos):
    return classe(nome="P", email="p@exemplo.test", **campos)


@pytest.mark.parametrize("permissao", PERMISSOES_DA_DIRECAO)
def test_so_a_direcao_ativa_tem_as_permissoes_de_gestao(permissao):
    assert getattr(_pessoa(Direcao), permissao)() is True
    assert getattr(_pessoa(Direcao, ativo=False), permissao)() is False
    assert getattr(_pessoa(AssistenteSocial), permissao)() is False
    assert getattr(_pessoa(EquipePedagogica), permissao)() is False


@pytest.fixture
def rota_da_direcao(api):
    bp = exigir_login(Blueprint("_prova_perfil", __name__))

    @bp.post("/_prova_perfil")
    @exige_permissao("pode_gerir_usuarios", "Você não pode cadastrar usuários.")
    def so_direcao():
        return jsonify({"ok": True})

    api.app.register_blueprint(bp, url_prefix="/api")
    return api


def test_direcao_passa(rota_da_direcao):
    assert rota_da_direcao.post("/api/_prova_perfil", como="direcao").status_code == 200


@pytest.mark.parametrize("quem", ["assistente", "educadora"])
def test_profissional_recebe_403_com_a_mensagem_da_rota(rota_da_direcao, quem):
    resposta = rota_da_direcao.post("/api/_prova_perfil", como=quem)
    assert resposta.status_code == 403
    assert resposta.get_json() == {"erro": "Você não pode cadastrar usuários."}


def test_sem_token_e_401_e_nao_403(rota_da_direcao):
    resposta = rota_da_direcao.post("/api/_prova_perfil", como=None)
    assert resposta.status_code == 401


def test_decorador_protege_mesmo_fora_de_blueprint_com_login(api):
    bp = Blueprint("_prova_sem_guarda", __name__)

    @bp.get("/_prova_sem_guarda")
    @exige_permissao("pode_consultar_auditoria", "Só a direção.")
    def rota():
        return jsonify({"ok": True})

    api.app.register_blueprint(bp, url_prefix="/api")
    assert api.get("/api/_prova_sem_guarda", como=None).status_code == 401
    assert api.get("/api/_prova_sem_guarda", como="assistente").status_code == 403
    assert api.get("/api/_prova_sem_guarda", como="direcao").status_code == 200
