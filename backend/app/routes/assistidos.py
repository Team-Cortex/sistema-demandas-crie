"""/api/assistidos. Spec 03, cards #15, #17 e #20."""

from flask import Blueprint, jsonify

from app.routes import corpo_json
from app.routes.sessao import exigir_login, usuario_atual
from app.schemas.assistido import AssistidoEntradaSchema, AssistidoSchema
from app.services.assistido import AssistidoService

bp = exigir_login(Blueprint("assistidos", __name__))


@bp.post("/assistidos")
def cadastrar():
    dados = AssistidoEntradaSchema().load(corpo_json())
    assistido = AssistidoService.cadastrar(dados, usuario_atual())
    return jsonify(AssistidoSchema().dump(assistido)), 201


# O card pediu PUT; a spec 03 diz PATCH. Com um campo só, o efeito é o mesmo.
@bp.route("/assistidos/<int:assistido_id>", methods=["PATCH", "PUT"])
def alterar(assistido_id):
    dados = AssistidoEntradaSchema().load(corpo_json())
    assistido = AssistidoService.alterar(assistido_id, dados, usuario_atual())
    return jsonify(AssistidoSchema().dump(assistido))
