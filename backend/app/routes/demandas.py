"""/api/demandas. Spec 02, card #19."""

from flask import Blueprint, jsonify, request

from app.routes import corpo_json
from app.routes.sessao import exigir_login, usuario_atual
from app.schemas.demanda import (
    DemandaComHistoricoSchema,
    DemandaSchema,
    FiltroDemandaSchema,
    HistoricoSchema,
    NovaDemandaSchema,
)
from app.services.demanda import DemandaService

bp = exigir_login(Blueprint("demandas", __name__))


@bp.get("/demandas")
def listar():
    filtros = FiltroDemandaSchema().load(request.args)
    return jsonify(DemandaSchema(many=True).dump(DemandaService.listar(**filtros)))


@bp.post("/demandas")
def abrir():
    dados = NovaDemandaSchema().load(corpo_json())
    demanda = DemandaService.abrir(dados, usuario_atual())
    return jsonify(DemandaComHistoricoSchema().dump(demanda)), 201


@bp.get("/demandas/<int:demanda_id>")
def obter(demanda_id):
    return jsonify(DemandaComHistoricoSchema().dump(DemandaService.obter(demanda_id)))


@bp.get("/demandas/<int:demanda_id>/historico")
def historico(demanda_id):
    demanda = DemandaService.obter(demanda_id)
    return jsonify(HistoricoSchema(many=True).dump(demanda.historico))
