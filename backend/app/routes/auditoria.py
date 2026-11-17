"""GET /api/auditoria. Spec 05 §3, card #17. Só a direção."""

from flask import Blueprint, jsonify, request

from app.routes.sessao import exige_permissao, exigir_login
from app.schemas.auditoria import FiltroAuditoriaSchema, RegistroAuditoriaSchema
from app.services.auditoria import AuditoriaService

bp = exigir_login(Blueprint("auditoria", __name__))


@bp.get("/auditoria")
@exige_permissao("pode_consultar_auditoria", "Só a direção consulta a auditoria.")
def consultar():
    filtros = FiltroAuditoriaSchema().load(request.args)
    itens, total = AuditoriaService.consultar(**filtros)
    return jsonify(
        {
            "itens": RegistroAuditoriaSchema(many=True).dump(itens),
            "total": total,
            "pagina": filtros["pagina"],
            "por_pagina": filtros["por_pagina"],
        }
    )
