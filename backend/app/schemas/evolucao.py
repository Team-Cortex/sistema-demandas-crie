"""Corpo e saída de evolução. Spec 06."""

from marshmallow import Schema, fields

from app.schemas import momento


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
