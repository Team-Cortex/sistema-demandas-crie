"""/api/demandas. Spec 02, card #19."""

from flask import Blueprint, jsonify, request

from app.routes import corpo_json
from app.routes.sessao import exigir_login, usuario_atual
from app.schemas.demanda import (
    AnotacaoSchema,
    DemandaComHistoricoSchema,
    DemandaSchema,
    FiltroDemandaSchema,
    FiltroMinhasSchema,
    HistoricoSchema,
    MudancaDeEstadoSchema,
    NovaDemandaSchema,
    TrocaDeResponsavelSchema,
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


@bp.patch("/demandas/<int:demanda_id>/estado")
def mudar_estado(demanda_id):
    dados = MudancaDeEstadoSchema().load(corpo_json())
    demanda = DemandaService.mudar_estado(demanda_id, dados["estado"], usuario_atual())
    return jsonify(DemandaComHistoricoSchema().dump(demanda))


@bp.get("/demandas/painel")
def painel():
    por_estado, vencidas = DemandaService.painel()
    saida = DemandaSchema(many=True)
    return jsonify(
        {
            "por_estado": {estado: saida.dump(lista) for estado, lista in por_estado.items()},
            "totais": {estado: len(lista) for estado, lista in por_estado.items()},
            "total": sum(len(lista) for lista in por_estado.values()),
            "vencidas": vencidas,
        }
    )


@bp.get("/demandas/minhas")
def minhas():
    filtros = FiltroMinhasSchema().load(request.args)
    demandas = DemandaService.do_responsavel(usuario_atual(), **filtros)
    return jsonify(DemandaSchema(many=True).dump(demandas))


@bp.post("/demandas/<int:demanda_id>/anotacoes")
def anotar(demanda_id):
    dados = AnotacaoSchema().load(corpo_json())
    item = DemandaService.anotar(demanda_id, dados["texto"], usuario_atual())
    return jsonify(HistoricoSchema().dump(item)), 201


@bp.patch("/demandas/<int:demanda_id>/responsavel")
def reatribuir(demanda_id):
    dados = TrocaDeResponsavelSchema().load(corpo_json())
    demanda = DemandaService.reatribuir(demanda_id, dados["responsavel_id"], usuario_atual())
    return jsonify(DemandaComHistoricoSchema().dump(demanda))


@bp.get("/demandas/<int:demanda_id>/historico")
def historico(demanda_id):
    demanda = DemandaService.obter(demanda_id)
    return jsonify(HistoricoSchema(many=True).dump(demanda.historico))
