"""Filtro e saída da consulta à auditoria. Spec 05 §3."""

from marshmallow import Schema, fields, validate

from app.models.auditoria import ACOES, RECURSOS
from app.schemas import FiltroPeriodo, Paginacao, inteiro, momento


class FiltroAuditoriaSchema(FiltroPeriodo, Paginacao):
    autor_id = inteiro("Informe o autor pelo número.")
    assistido_id = inteiro("Informe o assistido pelo número.")
    recurso = fields.String(validate=validate.OneOf(sorted(RECURSOS), error="Recurso desconhecido."))
    acao = fields.String(validate=validate.OneOf(sorted(ACOES), error="Ação desconhecida."))


class RegistroAuditoriaSchema(Schema):
    id = fields.Integer()
    autor_id = fields.Integer()
    autor_nome = fields.Function(lambda r: r.autor.nome)
    acao = fields.String()
    recurso = fields.String()
    recurso_id = fields.Integer()
    assistido_id = fields.Integer()
    detalhe = fields.String()
    ocorrido_em = momento("ocorrido_em")
