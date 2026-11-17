"""Validação de entrada e serialização de saída.

Toda mensagem de erro aqui é para quem usa o sistema (RNF14): o tratador
de ValidationError devolve a primeira delas, na ordem dos campos.
"""

from marshmallow import EXCLUDE, RAISE, Schema, ValidationError, fields

from app.fuso import no_fuso

CAMPO_NAO_ACEITO = "Campo não aceito: confira o formulário."
ENVIE_JSON = "Envie os dados em JSON."


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
