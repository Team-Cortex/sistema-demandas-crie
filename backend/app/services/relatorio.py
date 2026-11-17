"""Relatórios da direção. Spec 08, card #24, RF35, RF36, RF38 e RF39.

Toda emissão grava auditoria `emitir`; o momento da emissão devolvido é o
mesmo do registro.
"""

from app.extensions import db
from app.fuso import hoje
from app.models.demanda import EstadoDemanda
from app.schemas import descrever_filtros
from app.services.assistido import AssistidoService
from app.services.auditoria import AuditoriaService
from app.services.demanda import DemandaService


class RelatorioService:
    @staticmethod
    def demandas(autor, de, ate, estado=None, categoria=None, responsavel_id=None):
        """Devolve (registro de auditoria, itens, totais)."""
        itens = DemandaService.listar(
            estado=estado,
            categoria=categoria,
            responsavel_id=responsavel_id,
            periodo_inicio=de,
            periodo_fim=ate,
        )
        dia = hoje()
        por_estado = {e.value: 0 for e in EstadoDemanda}
        for demanda in itens:
            por_estado[demanda.estado.value] += 1
        totais = {
            "total": len(itens),
            "por_estado": por_estado,
            "vencidas": sum(1 for demanda in itens if demanda.vencida_em(dia)),
        }
        filtros = {
            "de": de,
            "ate": ate,
            "estado": ",".join(estado) if estado else None,
            "categoria": categoria,
            "responsavel_id": responsavel_id,
        }
        registro = AuditoriaService.registrar_leitura(
            autor, "emitir", "relatorio_demandas", detalhe=descrever_filtros(filtros)
        )
        return registro, itens, totais

    @staticmethod
    def assistido(autor, assistido_id, de, ate):
        """Devolve (registro, assistido, evoluções vigentes, encaminhamentos) do período."""
        from app.models import Encaminhamento, Evolucao

        assistido = AssistidoService.obter(assistido_id)
        evolucoes = Evolucao.do_assistido(assistido.id, de=de, ate=ate)
        encaminhamentos = db.session.scalars(
            db.select(Encaminhamento)
            .where(
                Encaminhamento.assistido_id == assistido.id,
                Encaminhamento.data >= de,
                Encaminhamento.data <= ate,
            )
            .order_by(Encaminhamento.data, Encaminhamento.id)
        ).all()
        registro = AuditoriaService.registrar_leitura(
            autor, "emitir", "relatorio_assistido", assistido_id=assistido.id,
            detalhe=descrever_filtros({"de": de, "ate": ate}),
        )
        return registro, assistido, evolucoes, encaminhamentos
