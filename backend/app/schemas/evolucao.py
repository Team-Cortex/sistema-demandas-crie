"""Corpo e saída de evolução. Spec 06."""

from marshmallow import Schema, ValidationError, fields, validate, validates_schema

from app.models.evolucao import AREA_MAXIMA
from app.schemas import Entrada, FiltroPeriodo, data, mensagens, momento, preenchido

INFORME_DATA = "Informe a data da evolução."
INFORME_AREA = "Informe a área de atuação."
INFORME_DESCRICAO = "Escreva a descrição da evolução."
AREA_LONGA = f"A área de atuação aceita até {AREA_MAXIMA} caracteres."


def _area(obrigatoria):
    return fields.String(
        required=obrigatoria,
        validate=[preenchido(INFORME_AREA), validate.Length(max=AREA_MAXIMA, error=AREA_LONGA)],
        error_messages=mensagens(INFORME_AREA),
    )


def _descricao(obrigatoria):
    return fields.String(
        required=obrigatoria, validate=preenchido(INFORME_DESCRICAO), error_messages=mensagens(INFORME_DESCRICAO)
    )


class NovaEvolucaoSchema(Entrada):
    """Autor, profissional e momento saem do token e do servidor (RF22)."""

    data = data(INFORME_DATA, required=True)
    area_atuacao = _area(True)
    descricao = _descricao(True)


class RetificacaoSchema(Entrada):
    data = data(INFORME_DATA)
    area_atuacao = _area(False)
    descricao = _descricao(False)

    @validates_schema
    def _algo_muda(self, dados, **_kwargs):
        if not dados:
            raise ValidationError("Informe o que muda na retificação.")


class FiltroEvolucaoSchema(FiltroPeriodo):
    area_atuacao = fields.String()


class EvolucaoSchema(Schema):
    id = fields.Integer()
    assistido_id = fields.Integer()
    data = fields.Date()
    area_atuacao = fields.String()
    descricao = fields.String()
    profissional_id = fields.Integer()
    profissional_nome = fields.Function(lambda e: e.profissional.nome)
    autor_id = fields.Integer()
    autor_nome = fields.Function(lambda e: e.autor.nome)
    ocorrido_em = momento("ocorrido_em")
    retifica_id = fields.Integer()
    vigente = fields.Boolean()


class EvolucaoComVersoesSchema(EvolucaoSchema):
    """GET /api/evolucoes/<id>: o que foi corrigido fica à vista (RF24)."""

    retificada_por_id = fields.Function(lambda e: e.retificada_por.id if e.retificada_por else None)
    versoes_anteriores = fields.Function(lambda e: EvolucaoSchema(many=True).dump(e.versoes_anteriores))
