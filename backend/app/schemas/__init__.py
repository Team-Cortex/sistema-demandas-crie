"""Validação de entrada e serialização de saída.

Toda mensagem de erro aqui é para quem usa o sistema (RNF14): o tratador
de ValidationError devolve a primeira delas, na ordem dos campos.
"""

from marshmallow import EXCLUDE, RAISE, Schema, ValidationError

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
