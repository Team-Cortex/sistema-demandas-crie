"""Gestão de usuários pela direção. Spec 01, card #23, RF04.

Não existe exclusão: sair do sistema é `ativo = False`.
"""

from sqlalchemy.exc import IntegrityError

from app.errors import ErroDeNegocio
from app.extensions import db

EMAIL_REPETIDO = "Já existe um usuário com este e-mail."


class UsuarioService:
    @staticmethod
    def cadastrar(dados):
        from app.models import CLASSE_POR_PERFIL, Usuario

        email = dados["email"].strip().lower()
        if db.session.scalars(db.select(Usuario.id).where(Usuario.email == email)).first() is not None:
            raise ErroDeNegocio(EMAIL_REPETIDO)
        classe = CLASSE_POR_PERFIL[dados["perfil"]]
        usuario = classe(nome=dados["nome"].strip(), email=email, senha=dados["senha"])
        db.session.add(usuario)
        try:
            db.session.commit()
        except IntegrityError:
            # Duas direções cadastrando o mesmo e-mail ao mesmo tempo.
            db.session.rollback()
            raise ErroDeNegocio(EMAIL_REPETIDO) from None
        return usuario
