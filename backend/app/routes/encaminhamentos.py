"""/api/encaminhamentos. Spec 07, card #22. Sem DELETE."""

from flask import Blueprint, jsonify, request

from app.routes import corpo_json
from app.routes.sessao import exigir_login, usuario_atual
from app.schemas.encaminhamento import (
    EncaminhamentoSchema,
    FiltroEncaminhamentoSchema,
    NovoEncaminhamentoSchema,
)
from app.services.encaminhamento import EncaminhamentoService

bp = exigir_login(Blueprint("encaminhamentos", __name__))


@bp.post("/encaminhamentos")
def registrar():
    dados = NovoEncaminhamentoSchema().load(corpo_json())
    encaminhamento = EncaminhamentoService.registrar(dados, usuario_atual())
    return jsonify(EncaminhamentoSchema().dump(encaminhamento)), 201


@bp.get("/encaminhamentos")
def listar():
    filtros = FiltroEncaminhamentoSchema().load(request.args)
    itens = EncaminhamentoService.listar(usuario_atual(), **filtros)
    return jsonify(EncaminhamentoSchema(many=True).dump(itens))


# O card pediu a rota; o contrato, o parâmetro pendentes=true. Os dois valem.
@bp.get("/encaminhamentos/pendentes")
def pendentes():
    filtros = FiltroEncaminhamentoSchema().load(request.args)
    filtros["pendentes"] = True
    itens = EncaminhamentoService.listar(usuario_atual(), **filtros)
    return jsonify(EncaminhamentoSchema(many=True).dump(itens))


@bp.get("/encaminhamentos/<int:encaminhamento_id>")
def consultar(encaminhamento_id):
    encaminhamento = EncaminhamentoService.consultar(encaminhamento_id, usuario_atual())
    return jsonify(EncaminhamentoSchema().dump(encaminhamento))
