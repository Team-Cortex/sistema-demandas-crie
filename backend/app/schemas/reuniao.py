"""Corpo e saída de reunião. Spec 04."""

from marshmallow import Schema, fields, validate

from app.models.reuniao import Setor
from app.schemas import Entrada, Filtro, data, mensagens, momento, valor_do_enum

INFORME_DATA = "Informe a data da reunião."
INFORME_SETOR = "Informe o setor da reunião."
INFORME_PARTICIPANTES = "Informe participantes ativos."
SETORES = [s.value for s in Setor]


def _setor(obrigatorio):
    return fields.String(
        required=obrigatorio,
        validate=validate.OneOf(SETORES, error=INFORME_SETOR),
        error_messages=mensagens(INFORME_SETOR),
    )


def _participantes(obrigatorio):
    return fields.List(
        fields.Integer(strict=True, error_messages=mensagens(INFORME_PARTICIPANTES)),
        required=obrigatorio,
        validate=validate.Length(min=1, error=INFORME_PARTICIPANTES),
        error_messages=mensagens(INFORME_PARTICIPANTES),
    )


class NovaReuniaoSchema(Entrada):
    data = data(INFORME_DATA, required=True)
    setor = _setor(True)
    participante_ids = _participantes(True)


class FiltroReuniaoSchema(Filtro):
    setor = _setor(False)


class PessoaSchema(Schema):
    id = fields.Integer()
    nome = fields.String()


class DemandaDaReuniaoSchema(Schema):
    id = fields.Integer()
    descricao = fields.String()
    estado = valor_do_enum("estado")


class ReuniaoSchema(Schema):
    id = fields.Integer()
    data = fields.Date()
    setor = valor_do_enum("setor")
    participantes = fields.List(fields.Nested(PessoaSchema))
    criado_em = momento("criado_em")


class ReuniaoComDemandasSchema(ReuniaoSchema):
    demandas = fields.List(fields.Nested(DemandaDaReuniaoSchema))
