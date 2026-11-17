"""Regras de login, sessão e papéis. Spec 01."""

import threading
import time
from collections import deque
from datetime import datetime, timezone
from functools import lru_cache

from flask import current_app
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

from app.errors import MuitasTentativas, NaoAutenticado
from app.extensions import db

CREDENCIAL_RECUSADA = "E-mail ou senha inválidos."


class LimiteDeTentativas:
    """Falhas de login por par IP + e-mail, numa janela deslizante.

    Guarda só os últimos `maximo` instantes de cada par. Fica na memória
    do processo: reiniciar zera, e cada processo conta o seu (spec 01).
    """

    def __init__(self, maximo=5, janela=60, relogio=time.monotonic):
        self.maximo = maximo
        self.janela = janela
        self._relogio = relogio
        self._falhas = {}
        self._trava = threading.Lock()

    def bloqueado(self, chave):
        with self._trava:
            falhas = self._falhas.get(chave)
            return (
                falhas is not None
                and len(falhas) >= self.maximo
                and self._relogio() - falhas[0] < self.janela
            )

    def registrar_falha(self, chave):
        with self._trava:
            agora = self._relogio()
            self._falhas.setdefault(chave, deque(maxlen=self.maximo)).append(agora)
            if len(self._falhas) > 10_000:
                self._esquecer_antigas(agora)

    def limpar(self, chave):
        with self._trava:
            self._falhas.pop(chave, None)

    def _esquecer_antigas(self, agora):
        for chave in [c for c, f in self._falhas.items() if agora - f[-1] >= self.janela]:
            del self._falhas[chave]


def limite_de_login():
    """Um contador por instância do app (cada teste ganha o seu)."""
    limite = current_app.extensions.get("limite_login")
    if limite is None:
        limite = LimiteDeTentativas(
            maximo=current_app.config.get("LOGIN_MAXIMO_FALHAS", 5),
            janela=current_app.config.get("LOGIN_JANELA_SEGUNDOS", 60),
        )
        current_app.extensions["limite_login"] = limite
    return limite


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
    def sair(dados_do_token):
        """Grava o jti até a expiração original; aproveita e limpa os vencidos."""
        from app.models import TokenRevogado

        TokenRevogado.esquecer_expirados()
        expira_em = datetime.fromtimestamp(dados_do_token["exp"], timezone.utc)
        if not TokenRevogado.revogado(dados_do_token["jti"]):
            db.session.add(TokenRevogado(jti=dados_do_token["jti"], expira_em=expira_em))
        db.session.commit()

    @staticmethod
    def entrar(email, senha, origem):
        """Login com limite: a sexta falha em 60 s do par origem + e-mail dá 429.

        A tentativa travada também conta como falha e não chega a comparar
        a senha, nem a certa.
        """
        limite = limite_de_login()
        chave = (origem or "", email.strip().lower())
        if limite.bloqueado(chave):
            limite.registrar_falha(chave)
            raise MuitasTentativas(CREDENCIAL_RECUSADA)
        try:
            usuario = AcessoService.autenticar(email, senha)
        except NaoAutenticado:
            limite.registrar_falha(chave)
            raise
        limite.limpar(chave)
        return usuario

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
