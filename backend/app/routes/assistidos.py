"""/api/assistidos. Spec 03, cards #15, #17 e #20."""

from flask import Blueprint, jsonify, request

from app.routes import corpo_json
from app.routes.sessao import exigir_login, usuario_atual
from app.schemas.assistido import (
    AssistidoEntradaSchema,
    AssistidoResumoSchema,
    AssistidoSchema,
    FiltroAssistidoSchema,
)
from app.schemas.demanda import DemandaSchema
from app.schemas.encaminhamento import EncaminhamentoSchema
from app.schemas.evolucao import EvolucaoSchema
from app.services.assistido import AssistidoService

bp = exigir_login(Blueprint("assistidos", __name__))


@bp.get("/assistidos")
def listar():
    filtros = FiltroAssistidoSchema().load(request.args)
    assistidos = AssistidoService.listar(usuario_atual(), **filtros)
    return jsonify(AssistidoResumoSchema(many=True).dump(assistidos))


@bp.get("/assistidos/<int:assistido_id>")
def consultar(assistido_id):
    assistido = AssistidoService.consultar(assistido_id, usuario_atual())
    return jsonify(AssistidoSchema().dump(assistido))


@bp.get("/assistidos/<int:assistido_id>/ficha")
def ficha(assistido_id):
    assistido = AssistidoService.ficha(assistido_id, usuario_atual())
    return jsonify(
        {
            "assistido": {
                "id": assistido.id,
                "nome_tratamento": assistido.nome_tratamento,
                "ativo": assistido.ativo,
            },
            "profissionais": [{"id": p.id, "nome": p.nome} for p in assistido.profissionais],
            "demandas": DemandaSchema(many=True).dump(assistido.demandas),
            "evolucoes": EvolucaoSchema(many=True).dump(assistido.evolucoes_vigentes),
            "encaminhamentos": EncaminhamentoSchema(many=True).dump(assistido.encaminhamentos),
        }
    )


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
