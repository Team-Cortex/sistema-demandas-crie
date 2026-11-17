"""Regras de login, sessão e papéis. Spec 01."""

from functools import lru_cache

from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

from app.errors import NaoAutenticado
from app.extensions import db

CREDENCIAL_RECUSADA = "E-mail ou senha inválidos."


@lru_cache(maxsize=1)
def _hash_de_mentira():
    """Hash fixo, no mesmo custo do real, para e-mail que não existe.

    Sem ele, responder "não existe" seria mais rápido que "senha errada",
    e o tempo de resposta revelaria quem tem conta.
    """
    return generate_password_hash("conta-que-nao-existe-no-sistema")


def emitir_token(usuario):
    """JWT de 30 minutos (JWT_ACCESS_TOKEN_EXPIRES). `sub` vai em texto."""
    return create_access_token(identity=str(usuario.id), additional_claims={"perfil": usuario.perfil})


class AcessoService:
    @staticmethod
    def autenticar(email, senha):
        """Devolve o usuário ativo dono do e-mail e da senha, ou recusa com 401.

        A mensagem é a mesma para e-mail inexistente, conta inativa e senha
        errada, e os três casos passam por uma comparação de hash.
        """
        from app.models import Usuario

        email = email.strip().lower()
        usuario = db.session.scalars(db.select(Usuario).where(Usuario.email == email)).first()
        if usuario is None:
            check_password_hash(_hash_de_mentira(), senha)
            raise NaoAutenticado(CREDENCIAL_RECUSADA)
        if not usuario.senha_confere(senha) or not usuario.ativo:
            raise NaoAutenticado(CREDENCIAL_RECUSADA)
        return usuario
