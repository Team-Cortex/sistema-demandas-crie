"""Corpo e saída de encaminhamento. Spec 07."""

from marshmallow import Schema, ValidationError, fields, validate, validates_schema

from app.models.encaminhamento import DESTINO_MAXIMO
from app.schemas import Entrada, Filtro, data, inteiro, mensagens, momento, preenchido

INFORME_VINCULO = "Informe o assistido ou a demanda do encaminhamento."
INFORME_DESTINO = "Informe o destino do encaminhamento."
INFORME_DATA = "Informe a data do encaminhamento."
ASSISTIDO_INEXISTENTE = "Assistido inexistente."
DEMANDA_INEXISTENTE = "Demanda inexistente."


class NovoEncaminhamentoSchema(Entrada):
    """O responsável sai do token; o desfecho vem depois (spec 07)."""

    assistido_id = inteiro(ASSISTIDO_INEXISTENTE, allow_none=True)
    demanda_id = inteiro(DEMANDA_INEXISTENTE, allow_none=True)
    destino = fields.String(
        required=True,
        validate=[preenchido(INFORME_DESTINO), validate.Length(max=DESTINO_MAXIMO, error=INFORME_DESTINO)],
        error_messages=mensagens(INFORME_DESTINO),
    )
    data = data(INFORME_DATA, required=True)
    observacao = fields.String(allow_none=True, error_messages={"invalid": "Escreva a observação em texto."})

    @validates_schema
    def _tem_vinculo(self, dados, **_kwargs):
        if dados.get("assistido_id") is None and dados.get("demanda_id") is None:
            raise ValidationError(INFORME_VINCULO)


class DesfechoSchema(Entrada):
    desfecho = fields.String(
        required=True,
        validate=preenchido("Escreva o desfecho do encaminhamento."),
        error_messages=mensagens("Escreva o desfecho do encaminhamento."),
    )


class FiltroEncaminhamentoSchema(Filtro):
    pendentes = fields.Boolean(error_messages=mensagens("Use pendentes=true ou pendentes=false."))
    assistido_id = inteiro("Informe o assistido pelo número.")
    demanda_id = inteiro("Informe a demanda pelo número.")
    responsavel_id = inteiro("Informe o responsável pelo número.")


class EncaminhamentoSchema(Schema):
    id = fields.Integer()
    assistido_id = fields.Integer()
    demanda_id = fields.Integer()
    destino = fields.String()
    data = fields.Date()
    responsavel_id = fields.Integer()
    responsavel_nome = fields.Function(lambda e: e.responsavel.nome)
    observacao = fields.String()
    pendente = fields.Boolean()
    desfecho = fields.String()
    desfecho_autor_id = fields.Integer()
    desfecho_em = momento("desfecho_em")
    criado_em = momento("criado_em")
