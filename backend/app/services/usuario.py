"""Gestão de usuários pela direção. Spec 01, card #23, RF04.

Não existe exclusão: sair do sistema é `ativo = False`.
"""

from sqlalchemy.exc import IntegrityError

from app.errors import ErroDeNegocio, NaoEncontrado
from app.extensions import db

EMAIL_REPETIDO = "Já existe um usuário com este e-mail."
INEXISTENTE = "Usuário inexistente."
PROPRIA_CONTA = "Você não pode alterar o próprio perfil nem desativar a própria conta."


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
    def alterar(usuario_id, dados, autor):
        """Muda nome, perfil e ativo. Não apaga a linha.

        Quem opera não muda o próprio perfil nem se desativa: assim sempre
        resta ao menos uma direção ativa para gerir os usuários.
        """
        from app.models import Usuario

        usuario = UsuarioService.obter(usuario_id)
        novo_perfil = dados.get("perfil")
        troca_perfil = novo_perfil is not None and novo_perfil != usuario.perfil
        if usuario.id == autor.id and (troca_perfil or dados.get("ativo") is False):
            raise ErroDeNegocio(PROPRIA_CONTA)

        if "nome" in dados:
            usuario.nome = dados["nome"].strip()
        if "ativo" in dados:
            usuario.ativo = dados["ativo"]
        if troca_perfil:
            # `perfil` escolhe a subclasse (herança de tabela única). O objeto
            # carregado não muda de classe; grava direto na tabela e recarrega.
            db.session.flush()
            tabela = Usuario.__table__
            db.session.execute(tabela.update().where(tabela.c.id == usuario.id).values(perfil=novo_perfil))
        db.session.commit()
        if troca_perfil:
            db.session.expunge(usuario)
            usuario = db.session.get(Usuario, usuario_id)
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
