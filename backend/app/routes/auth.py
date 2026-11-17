"""POST /api/auth/login e POST /api/auth/logout. Spec 01."""

from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import get_jwt, verify_jwt_in_request

from app.routes import corpo_json
from app.schemas.acesso import LoginSchema
from app.services.acesso import AcessoService, emitir_token
from app.services.aviso import AvisoService

bp = Blueprint("auth", __name__)


@bp.post("/auth/login")
def login():
    dados = LoginSchema().load(corpo_json())
    usuario = AcessoService.entrar(dados["email"], dados["senha"], request.remote_addr)
    dias = current_app.config.get("AVISO_DIAS_ANTES_DO_PRAZO", 3)
    return jsonify(
        {
            "token": emitir_token(usuario),
            "perfil": usuario.perfil,
            "usuario": {"id": usuario.id, "nome": usuario.nome, "perfil": usuario.perfil},
            # Spec 09: só id, prazo, estado e vencida; nenhum dado de saúde.
            "avisos": AvisoService.de_prazo(usuario, dias),
        }
    )


@bp.post("/auth/logout")
def logout():
    # O login é público; o logout não: verifica aqui, não no blueprint.
    verify_jwt_in_request()
    AcessoService.sair(get_jwt())
    return jsonify({"ok": True})
