"""POST /api/auth/login e POST /api/auth/logout. Spec 01."""

from flask import Blueprint, jsonify

from app.routes import corpo_json
from app.schemas.acesso import LoginSchema
from app.services.acesso import AcessoService, emitir_token

bp = Blueprint("auth", __name__)


@bp.post("/auth/login")
def login():
    dados = LoginSchema().load(corpo_json())
    usuario = AcessoService.autenticar(dados["email"], dados["senha"])
    return jsonify(
        {
            "token": emitir_token(usuario),
            "perfil": usuario.perfil,
            "usuario": {"id": usuario.id, "nome": usuario.nome, "perfil": usuario.perfil},
        }
    )
