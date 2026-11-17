"""Corpo de login e de usuário. Spec 01."""

from marshmallow import EXCLUDE, Schema, fields, pre_load, validate

from app.models.usuario import CLASSE_POR_PERFIL, SENHA_MINIMA
from app.schemas import Entrada, Filtro, mensagens, momento, preenchido

INFORME_EMAIL_E_SENHA = "Informe e-mail e senha."
INFORME_NOME = "Informe o nome."
EMAIL_INVALIDO = "Informe um e-mail válido."
SENHA_CURTA = f"A senha precisa ter no mínimo {SENHA_MINIMA} caracteres."
PERFIL_INVALIDO = "Escolha um perfil válido."
PERFIS = tuple(CLASSE_POR_PERFIL)


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


def _nome(obrigatorio):
    return fields.String(
        required=obrigatorio,
        validate=[preenchido(INFORME_NOME), validate.Length(max=120, error="O nome aceita até 120 caracteres.")],
        error_messages=mensagens(INFORME_NOME),
    )


def _perfil(obrigatorio):
    return fields.String(
        required=obrigatorio,
        validate=validate.OneOf(PERFIS, error=PERFIL_INVALIDO),
        error_messages=mensagens(PERFIL_INVALIDO),
    )


class NovoUsuarioSchema(Entrada):
    """POST /api/usuarios. A senha nunca volta na resposta."""

    nome = _nome(True)
    email = fields.Email(
        required=True,
        validate=validate.Length(max=254, error=EMAIL_INVALIDO),
        error_messages=mensagens(EMAIL_INVALIDO),
    )
    senha = fields.String(
        required=True,
        load_only=True,
        validate=validate.Length(min=SENHA_MINIMA, error=SENHA_CURTA),
        error_messages=mensagens(SENHA_CURTA),
    )
    perfil = _perfil(True)

    @pre_load
    def _email_sem_espaco(self, dados, **_kwargs):
        if isinstance(dados, dict) and isinstance(dados.get("email"), str):
            dados = {**dados, "email": dados["email"].strip()}
        return dados


class FiltroUsuarioSchema(Filtro):
    ativo = fields.Boolean(error_messages=mensagens("Use ativo=true ou ativo=false."))
    perfil = _perfil(False)


class UsuarioSchema(Schema):
    """Saída. Quem não é direção recebe sem o e-mail (spec 01)."""

    id = fields.Integer()
    nome = fields.String()
    email = fields.String()
    perfil = fields.String()
    ativo = fields.Boolean()
    criado_em = momento("criado_em")
