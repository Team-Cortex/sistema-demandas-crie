"""Gestão de usuários pela direção. Spec 01, card #23, RF04.

Não existe exclusão: sair do sistema é `ativo = False`.
"""

from sqlalchemy.exc import IntegrityError

from app.errors import ErroDeNegocio, NaoEncontrado
from app.extensions import db

EMAIL_REPETIDO = "Já existe um usuário com este e-mail."
INEXISTENTE = "Usuário inexistente."


class UsuarioService:
    @staticmethod
    def listar(ativo=None, perfil=None):
        from app.models import Usuario

        consulta = db.select(Usuario)
        if ativo is not None:
            consulta = consulta.where(Usuario.ativo.is_(ativo))
        if perfil:
            consulta = consulta.where(Usuario.perfil == perfil)
        return db.session.scalars(consulta.order_by(Usuario.nome, Usuario.id)).all()

    @staticmethod
    def obter(usuario_id):
        from app.models import Usuario

        usuario = db.session.get(Usuario, usuario_id)
        if usuario is None:
            raise NaoEncontrado(INEXISTENTE)
        return usuario

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
