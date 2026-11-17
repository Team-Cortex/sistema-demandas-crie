"""Validação de entrada e serialização de saída.

Toda mensagem de erro aqui é para quem usa o sistema (RNF14): o tratador
de ValidationError devolve a primeira delas, na ordem dos campos.
"""

from marshmallow import EXCLUDE, RAISE, Schema, ValidationError, fields, validate, validates_schema

from app.fuso import no_fuso

CAMPO_NAO_ACEITO = "Campo não aceito: confira o formulário."
ENVIE_JSON = "Envie os dados em JSON."
DATA_INVALIDA = "Use datas no formato AAAA-MM-DD."
PERIODO_INVERTIDO = "A data inicial não pode ser depois da final."


class Entrada(Schema):
    """Corpo de requisição. Campo desconhecido é recusado com 422."""

    error_messages = {"unknown": CAMPO_NAO_ACEITO, "type": ENVIE_JSON}

    class Meta:
        unknown = RAISE


class Filtro(Schema):
    """Parâmetros de busca na URL. Parâmetro desconhecido é ignorado."""

    error_messages = {"type": "Filtro inválido."}

    class Meta:
        unknown = EXCLUDE


def mensagens(mensagem):
    """A mesma mensagem para ausente, nulo e formato errado."""
    return {"required": mensagem, "null": mensagem, "invalid": mensagem}


def data(mensagem=DATA_INVALIDA, **opcoes):
    """Data AAAA-MM-DD com mensagem em português."""
    return fields.Date(error_messages=mensagens(mensagem), **opcoes)


def inteiro(mensagem, **opcoes):
    return fields.Integer(strict=False, error_messages=mensagens(mensagem), **opcoes)


class FiltroPeriodo(Filtro):
    """`de` e `ate` inclusivos; `de` depois de `ate` é 422."""

    de = data()
    ate = data()

    @validates_schema
    def _periodo_em_ordem(self, dados, **_kwargs):
        if dados.get("de") and dados.get("ate") and dados["de"] > dados["ate"]:
            raise ValidationError(PERIODO_INVERTIDO)


class Paginacao(Filtro):
    pagina = inteiro(
        "A página começa em 1.", load_default=1, validate=validate.Range(min=1, error="A página começa em 1.")
    )
    por_pagina = inteiro(
        "Use por_pagina de 1 a 200.",
        load_default=50,
        validate=validate.Range(min=1, max=200, error="Use por_pagina de 1 a 200."),
    )


def descrever_filtros(filtros, ocultar=()):
    """Texto curto dos filtros usados, para o `detalhe` da auditoria.

    Valor de campo em `ocultar` (busca por nome, por exemplo) não entra:
    o registro de auditoria não guarda dado de assistido.
    """
    partes = []
    for chave, valor in filtros.items():
        if valor is None or valor == "":
            continue
        partes.append(f"{chave}=*" if chave in ocultar else f"{chave}={getattr(valor, 'value', valor)}")
    return " ".join(partes) or None


def preenchido(mensagem):
    """Validador: texto que não seja só espaço."""

    def validar(valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValidationError(mensagem)

    return validar


def momento(atributo):
    """Campo de saída: data e hora em ISO 8601 com -03:00."""
    return fields.Function(lambda obj: no_fuso(getattr(obj, atributo)))


def valor_do_enum(atributo):
    """Campo de saída: o texto do enum (`aberta`, `saude`...), ou None."""

    def ler(obj):
        valor = getattr(obj, atributo)
        return getattr(valor, "value", valor)

    return fields.Function(ler)
