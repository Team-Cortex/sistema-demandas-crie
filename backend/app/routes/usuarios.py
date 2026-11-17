"""/api/usuarios. Spec 01, cards #15 e #23."""

from flask import Blueprint, jsonify, request

from app.routes import corpo_json
from app.routes.sessao import exige_permissao, exigir_login, usuario_atual
from app.schemas.acesso import AlterarUsuarioSchema, FiltroUsuarioSchema, NovoUsuarioSchema, UsuarioSchema
from app.services.usuario import UsuarioService

bp = exigir_login(Blueprint("usuarios", __name__))

NAO_CADASTRA = "Você não pode cadastrar usuários."
NAO_ALTERA = "Você não pode alterar usuários."


def _saida(**opcoes):
    """E-mail só para quem gere usuários (spec 01)."""
    if usuario_atual().pode_gerir_usuarios():
        return UsuarioSchema(**opcoes)
    return UsuarioSchema(exclude=("email",), **opcoes)


@bp.get("/usuarios")
def listar():
    filtros = FiltroUsuarioSchema().load(request.args)
    return jsonify(_saida(many=True).dump(UsuarioService.listar(**filtros)))


@bp.get("/usuarios/<int:usuario_id>")
def obter(usuario_id):
    return jsonify(_saida().dump(UsuarioService.obter(usuario_id)))


@bp.post("/usuarios")
@exige_permissao("pode_gerir_usuarios", NAO_CADASTRA)
def cadastrar():
    dados = NovoUsuarioSchema().load(corpo_json())
    usuario = UsuarioService.cadastrar(dados)
    return jsonify(UsuarioSchema().dump(usuario)), 201


# O card pediu PUT; a spec 01 diz PATCH. Os dois só mudam o que veio no corpo.
@bp.route("/usuarios/<int:usuario_id>", methods=["PATCH", "PUT"])
@exige_permissao("pode_gerir_usuarios", NAO_ALTERA)
def alterar(usuario_id):
    dados = AlterarUsuarioSchema().load(corpo_json())
    usuario = UsuarioService.alterar(usuario_id, dados, usuario_atual())
    return jsonify(UsuarioSchema().dump(usuario))
