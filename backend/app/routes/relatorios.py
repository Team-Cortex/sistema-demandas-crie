"""/api/relatorios. Spec 08, card #24. Só a direção."""

from flask import Blueprint, jsonify, request

from app.fuso import no_fuso
from app.routes.sessao import exige_permissao, exigir_login, usuario_atual
from app.schemas.demanda import DemandaSchema
from app.schemas.encaminhamento import EncaminhamentoSchema
from app.schemas.evolucao import EvolucaoSchema
from app.schemas.relatorio import FiltroRelatorioDemandasSchema, PeriodoDoRelatorioSchema
from app.services.relatorio import RelatorioService

bp = exigir_login(Blueprint("relatorios", __name__))

SO_DIRECAO = "Só a direção emite relatórios."


def _emissao(registro):
    return {
        "autor_id": registro.autor_id,
        "autor_nome": registro.autor.nome,
        "ocorrido_em": no_fuso(registro.ocorrido_em),
    }


def _periodo(filtros):
    return {"de": filtros["de"].isoformat(), "ate": filtros["ate"].isoformat()}


@bp.get("/relatorios/demandas")
@exige_permissao("pode_emitir_relatorio", SO_DIRECAO)
def demandas():
    filtros = FiltroRelatorioDemandasSchema().load(request.args)
    registro, itens, totais = RelatorioService.demandas(usuario_atual(), **filtros)
    return jsonify(
        {
            "emissao": _emissao(registro),
            "periodo": _periodo(filtros),
            "filtros": {
                "estado": filtros.get("estado"),
                "categoria": filtros.get("categoria"),
                "responsavel_id": filtros.get("responsavel_id"),
            },
            "totais": totais,
            "itens": DemandaSchema(many=True).dump(itens),
        }
    )


@bp.get("/relatorios/assistidos/<int:assistido_id>")
@exige_permissao("pode_emitir_relatorio", SO_DIRECAO)
def assistido(assistido_id):
    filtros = PeriodoDoRelatorioSchema().load(request.args)
    registro, pessoa, evolucoes, encaminhamentos = RelatorioService.assistido(
        usuario_atual(), assistido_id, filtros["de"], filtros["ate"]
    )
    return jsonify(
        {
            "emissao": _emissao(registro),
            "periodo": _periodo(filtros),
            "assistido": {"id": pessoa.id, "nome_tratamento": pessoa.nome_tratamento},
            "evolucoes": EvolucaoSchema(many=True).dump(evolucoes),
            "encaminhamentos": EncaminhamentoSchema(many=True).dump(encaminhamentos),
        }
    )
