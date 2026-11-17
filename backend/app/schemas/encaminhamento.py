"""Corpo e saída de encaminhamento. Spec 07."""

from marshmallow import Schema, fields

from app.schemas import momento


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
