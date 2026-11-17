"""Filtros dos relatórios. Spec 08."""

from marshmallow import fields, post_load

from app.schemas import FiltroPeriodo, data, inteiro
from app.schemas.demanda import _estados

PERIODO_OBRIGATORIO = "Informe o período do relatório (de e ate)."


class PeriodoDoRelatorioSchema(FiltroPeriodo):
    de = data(PERIODO_OBRIGATORIO, required=True)
    ate = data(PERIODO_OBRIGATORIO, required=True)


class FiltroRelatorioDemandasSchema(PeriodoDoRelatorioSchema):
    estado = fields.String(validate=_estados)
    categoria = fields.String()
    responsavel_id = inteiro("Informe o responsável pelo número.")

    @post_load
    def _normaliza(self, dados, **_kwargs):
        if "estado" in dados:
            dados["estado"] = [p.strip() for p in dados["estado"].split(",") if p.strip()]
        return dados
