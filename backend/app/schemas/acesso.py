"""Corpo de login e de usuário. Spec 01."""

from marshmallow import EXCLUDE, fields

from app.schemas import Entrada, mensagens, preenchido

INFORME_EMAIL_E_SENHA = "Informe e-mail e senha."


class LoginSchema(Entrada):
    """Qualquer falta vira a mesma mensagem; campo a mais é ignorado."""

    class Meta:
        unknown = EXCLUDE

    error_messages = {"type": INFORME_EMAIL_E_SENHA}

    email = fields.String(
        required=True, validate=preenchido(INFORME_EMAIL_E_SENHA), error_messages=mensagens(INFORME_EMAIL_E_SENHA)
    )
    senha = fields.String(
        required=True, validate=preenchido(INFORME_EMAIL_E_SENHA), error_messages=mensagens(INFORME_EMAIL_E_SENHA)
    )
