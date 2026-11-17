"""/api/usuarios. Spec 01, cards #15 e #23."""

from flask import Blueprint, jsonify

from app.routes import corpo_json
from app.routes.sessao import exige_permissao, exigir_login
from app.schemas.acesso import NovoUsuarioSchema, UsuarioSchema
from app.services.usuario import UsuarioService

bp = exigir_login(Blueprint("usuarios", __name__))

NAO_CADASTRA = "Você não pode cadastrar usuários."


@bp.post("/usuarios")
@exige_permissao("pode_gerir_usuarios", NAO_CADASTRA)
def cadastrar():
    dados = NovoUsuarioSchema().load(corpo_json())
    usuario = UsuarioService.cadastrar(dados)
    return jsonify(UsuarioSchema().dump(usuario)), 201
