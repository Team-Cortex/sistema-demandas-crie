"""Corpo e saída de demanda, estado e anotação. Spec 02."""

from marshmallow import Schema, fields, validate

from app.fuso import hoje
from app.models.demanda import CATEGORIA_MAXIMA, Prioridade
from app.schemas import Entrada, data, inteiro, mensagens, momento, preenchido, valor_do_enum

INFORME_DESCRICAO = "Informe a descrição da demanda."
INFORME_PRIORIDADE = "Escolha a prioridade: baixa, media ou alta."
INFORME_RESPONSAVEL = "Informe um responsável ativo."
INFORME_PRAZO = "Informe o prazo."
INFORME_REUNIAO = "Informe uma reunião existente."
ASSISTIDO_INEXISTENTE = "Assistido inexistente."
CATEGORIA_LONGA = f"A categoria aceita até {CATEGORIA_MAXIMA} caracteres."
PRIORIDADES = [p.value for p in Prioridade]


class NovaDemandaSchema(Entrada):
    descricao = fields.String(
        required=True, validate=preenchido(INFORME_DESCRICAO), error_messages=mensagens(INFORME_DESCRICAO)
    )
    prioridade = fields.String(
        required=True,
        validate=validate.OneOf(PRIORIDADES, error=INFORME_PRIORIDADE),
        error_messages=mensagens(INFORME_PRIORIDADE),
    )
    responsavel_id = inteiro(INFORME_RESPONSAVEL, required=True)
    prazo = data(INFORME_PRAZO, required=True)
    reuniao_id = inteiro(INFORME_REUNIAO, required=True)
    assistido_id = inteiro(ASSISTIDO_INEXISTENTE, allow_none=True)
    categoria = fields.String(
        allow_none=True,
        validate=validate.Length(max=CATEGORIA_MAXIMA, error=CATEGORIA_LONGA),
        error_messages={"invalid": "Informe a categoria em texto."},
    )


class HistoricoSchema(Schema):
    id = fields.Integer()
    tipo = valor_do_enum("tipo")
    texto = fields.String()
    estado_anterior = valor_do_enum("estado_anterior")
    estado_novo = valor_do_enum("estado_novo")
    autor_id = fields.Integer()
    autor_nome = fields.Function(lambda h: h.autor.nome)
    ocorrido_em = momento("ocorrido_em")


class DemandaSchema(Schema):
    """Sem dado de assistido além do id (spec 02)."""

    id = fields.Integer()
    descricao = fields.String()
    categoria = fields.String()
    prioridade = valor_do_enum("prioridade")
    prazo = fields.Date()
    estado = valor_do_enum("estado")
    vencida = fields.Function(lambda d: d.vencida_em(hoje()))
    responsavel_id = fields.Integer()
    responsavel_nome = fields.Function(lambda d: d.responsavel.nome)
    reuniao_id = fields.Integer()
    assistido_id = fields.Integer()
    criado_em = momento("criado_em")
    atualizado_em = momento("atualizado_em")
    ultimo_movimento = momento("ultimo_movimento")


class DemandaComHistoricoSchema(DemandaSchema):
    historico = fields.List(fields.Nested(HistoricoSchema))
