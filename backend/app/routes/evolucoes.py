"""/api/assistidos/<id>/evolucoes e /api/evolucoes/<id>. Spec 06, card #21.

Sem DELETE (RF26): a rota não existe e o Flask responde 405.
"""

from flask import Blueprint, jsonify, request

from app.routes import corpo_json
from app.routes.sessao import exigir_login, usuario_atual
from app.schemas.evolucao import (
    EvolucaoComVersoesSchema,
    EvolucaoSchema,
    FiltroEvolucaoSchema,
    NovaEvolucaoSchema,
    RetificacaoSchema,
)
from app.services.evolucao import EvolucaoService

bp = exigir_login(Blueprint("evolucoes", __name__))


@bp.post("/assistidos/<int:assistido_id>/evolucoes")
def lancar(assistido_id):
    dados = NovaEvolucaoSchema().load(corpo_json())
    evolucao = EvolucaoService.lancar(assistido_id, dados, usuario_atual())
    return jsonify(EvolucaoSchema().dump(evolucao)), 201


@bp.get("/assistidos/<int:assistido_id>/evolucoes")
def listar(assistido_id):
    filtros = FiltroEvolucaoSchema().load(request.args)
    evolucoes = EvolucaoService.listar(assistido_id, usuario_atual(), **filtros)
    return jsonify(EvolucaoSchema(many=True).dump(evolucoes))


@bp.get("/evolucoes/<int:evolucao_id>")
def consultar(evolucao_id):
    evolucao = EvolucaoService.consultar(evolucao_id, usuario_atual())
    return jsonify(EvolucaoComVersoesSchema().dump(evolucao))


@bp.patch("/evolucoes/<int:evolucao_id>")
def retificar(evolucao_id):
    dados = RetificacaoSchema().load(corpo_json())
    nova = EvolucaoService.retificar(evolucao_id, dados, usuario_atual())
    return jsonify(EvolucaoSchema().dump(nova)), 201
