"""/api/reunioes. Spec 04, card #18."""

from flask import Blueprint, jsonify, request

from app.routes import corpo_json
from app.routes.sessao import exigir_login
from app.schemas.reuniao import (
    FiltroReuniaoSchema,
    NovaReuniaoSchema,
    ReuniaoComDemandasSchema,
    ReuniaoSchema,
)
from app.services.reuniao import ReuniaoService

bp = exigir_login(Blueprint("reunioes", __name__))


@bp.post("/reunioes")
def registrar():
    dados = NovaReuniaoSchema().load(corpo_json())
    reuniao = ReuniaoService.registrar(dados)
    return jsonify(ReuniaoComDemandasSchema().dump(reuniao)), 201


@bp.get("/reunioes")
def listar():
    filtros = FiltroReuniaoSchema().load(request.args)
    return jsonify(ReuniaoSchema(many=True).dump(ReuniaoService.listar(**filtros)))


@bp.get("/reunioes/<int:reuniao_id>")
def obter(reuniao_id):
    return jsonify(ReuniaoComDemandasSchema().dump(ReuniaoService.obter(reuniao_id)))
