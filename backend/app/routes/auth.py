"""POST /api/auth/login e POST /api/auth/logout. Spec 01."""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, verify_jwt_in_request

from app.routes import corpo_json
from app.schemas.acesso import LoginSchema
from app.services.acesso import AcessoService, emitir_token

bp = Blueprint("auth", __name__)


@bp.post("/auth/login")
def login():
    dados = LoginSchema().load(corpo_json())
    usuario = AcessoService.entrar(dados["email"], dados["senha"], request.remote_addr)
    return jsonify(
        {
            "token": emitir_token(usuario),
            "perfil": usuario.perfil,
            "usuario": {"id": usuario.id, "nome": usuario.nome, "perfil": usuario.perfil},
        }
    )


@bp.post("/auth/logout")
def logout():
    # O login é público; o logout não: verifica aqui, não no blueprint.
    verify_jwt_in_request()
    AcessoService.sair(get_jwt())
    return jsonify({"ok": True})
