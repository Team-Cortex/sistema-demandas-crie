"""Primeiro acesso administrativo, sem endpoint público. Spec 01 §3.1."""

import click
from flask import current_app
from flask.cli import with_appcontext
from marshmallow import ValidationError
from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError

from app.errors import ErroDeNegocio, primeira_mensagem
from app.extensions import db
from app.models import Usuario
from app.schemas.acesso import NovoUsuarioSchema
from app.services.usuario import UsuarioService


@click.command("criar-primeira-direcao")
@click.option("--nome", required=True, help="Nome da primeira direção.")
@click.option("--email", required=True, help="E-mail do primeiro acesso.")
@with_appcontext
def criar_primeira_direcao(nome, email):
    """Cria apenas a primeira direção, se não houver nenhum usuário."""
    if not current_app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise click.ClickException("Configure o banco antes de criar a primeira direção.")

    senha = click.prompt("Senha", hide_input=True, confirmation_prompt=True)
    try:
        dados = NovoUsuarioSchema().load({
            "nome": nome, "email": email, "senha": senha, "perfil": "direcao",
        })
    except ValidationError as erro:
        raise click.ClickException(primeira_mensagem(erro.messages)) from None

    try:
        # Spec 01 §3.1: serializa também dois cadastros com e-mails diferentes.
        if db.engine.dialect.name == "postgresql":
            db.session.execute(db.text("LOCK TABLE usuario IN EXCLUSIVE MODE"))
        if db.session.scalar(db.select(Usuario.id).limit(1)) is not None:
            raise ErroDeNegocio("Já existem usuários. Use uma direção existente para cadastrar contas.")
        usuario = UsuarioService.cadastrar(dados)
    except ErroDeNegocio as erro:
        db.session.rollback()
        raise click.ClickException(erro.mensagem) from None
    except SQLAlchemyError:
        db.session.rollback()
        raise click.ClickException("Não foi possível criar a direção. Confira o banco e as migrações.") from None

    click.echo(f"Primeira direção criada (id {inspect(usuario).identity[0]}).")
