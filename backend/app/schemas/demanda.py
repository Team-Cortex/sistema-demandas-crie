"""Corpo e saída de demanda, estado e anotação. Spec 02."""

from marshmallow import Schema, ValidationError, fields, post_load, validate, validates_schema

from app.fuso import hoje
from app.models.demanda import CATEGORIA_MAXIMA, EstadoDemanda, Prioridade
from app.schemas import (
    PERIODO_INVERTIDO,
    Entrada,
    Filtro,
    data,
    inteiro,
    mensagens,
    momento,
    preenchido,
    valor_do_enum,
)

INFORME_DESCRICAO = "Informe a descrição da demanda."
INFORME_PRIORIDADE = "Escolha a prioridade: baixa, media ou alta."
INFORME_RESPONSAVEL = "Informe um responsável ativo."
INFORME_PRAZO = "Informe o prazo."
INFORME_REUNIAO = "Informe uma reunião existente."
ASSISTIDO_INEXISTENTE = "Assistido inexistente."
CATEGORIA_LONGA = f"A categoria aceita até {CATEGORIA_MAXIMA} caracteres."
PRIORIDADES = [p.value for p in Prioridade]
ESTADOS = [e.value for e in EstadoDemanda]


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


class MudancaDeEstadoSchema(Entrada):
    """Estado fora da lista passa daqui e o model recusa com 400 (spec 02)."""

    estado = fields.String(required=True, error_messages=mensagens("Informe o novo estado."))


class AnotacaoSchema(Entrada):
    texto = fields.String(
        required=True,
        validate=preenchido("Escreva o texto da anotação."),
        error_messages=mensagens("Escreva o texto da anotação."),
    )


class TrocaDeResponsavelSchema(Entrada):
    responsavel_id = inteiro("Informe o novo responsável.", required=True)


def _estados(valor):
    """`aberta` ou `aberta,em_andamento` → lista; estado desconhecido é 422."""
    partes = [p.strip() for p in valor.split(",") if p.strip()]
    if not partes or any(p not in ESTADOS for p in partes):
        raise ValidationError("Estado desconhecido. Use: " + ", ".join(ESTADOS) + ".")


class FiltroDemandaSchema(Filtro):
    """GET /api/demandas. `q` e `busca` são o mesmo filtro (spec 02)."""

    estado = fields.String(validate=_estados)
    responsavel_id = inteiro("Informe o responsável pelo número.")
    assistido_id = inteiro("Informe o assistido pelo número.")
    reuniao_id = inteiro("Informe a reunião pelo número.")
    categoria = fields.String()
    periodo_inicio = data()
    periodo_fim = data()
    q = fields.String()
    busca = fields.String()

    @validates_schema
    def _periodo_em_ordem(self, dados, **_kwargs):
        inicio, fim = dados.get("periodo_inicio"), dados.get("periodo_fim")
        if inicio and fim and inicio > fim:
            raise ValidationError(PERIODO_INVERTIDO)

    @post_load
    def _normaliza(self, dados, **_kwargs):
        if "estado" in dados:
            dados["estado"] = [p.strip() for p in dados["estado"].split(",") if p.strip()]
        busca = dados.pop("busca", None)
        if busca is not None and dados.get("q") is None:
            dados["q"] = busca
        if dados.get("q") is not None and not dados["q"].strip():
            dados.pop("q")
        return dados


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
