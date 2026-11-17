"""Corpo e saída de assistido. Enquanto a decisão A3 estiver aberta, só nome_tratamento. Spec 03."""

from marshmallow import Schema, ValidationError, fields, pre_load, validate

from app.models.assistido import Assistido
from app.schemas import Entrada, Filtro, mensagens, momento, preenchido

NAO_AUTORIZADO = "Este dado ainda não foi autorizado pela instituição."
INFORME_NOME = "Informe o nome de tratamento."


class AssistidoEntradaSchema(Entrada):
    """POST e PATCH/PUT. Campo fora do autorizado é recusado antes de tudo."""

    nome_tratamento = fields.String(
        required=True,
        validate=[
            preenchido(INFORME_NOME),
            validate.Length(max=120, error="O nome de tratamento aceita até 120 caracteres."),
        ],
        error_messages=mensagens(INFORME_NOME),
    )

    @pre_load
    def _so_o_autorizado(self, dados, **_kwargs):
        if isinstance(dados, dict) and set(dados) - Assistido.CAMPOS_AUTORIZADOS:
            raise ValidationError(NAO_AUTORIZADO)
        return dados


class FiltroAssistidoSchema(Filtro):
    busca = fields.String()


class AssistidoResumoSchema(Schema):
    id = fields.Integer()
    nome_tratamento = fields.String()


class AssistidoSchema(AssistidoResumoSchema):
    """O registro com os ids da ficha, em ordem cronológica (spec 03)."""

    ativo = fields.Boolean()
    criado_em = momento("criado_em")
    demandas = fields.Function(lambda a: [d.id for d in a.demandas])
    evolucoes = fields.Function(lambda a: [e.id for e in a.evolucoes_vigentes])
    encaminhamentos = fields.Function(lambda a: [e.id for e in a.encaminhamentos])
