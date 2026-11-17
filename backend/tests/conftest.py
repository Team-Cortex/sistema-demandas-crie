from contextlib import contextmanager

import pytest
from sqlalchemy import event

import app.models  # noqa: F401  registra as tabelas no metadata
from app import create_app
from app.extensions import db as _db
from config import TestingConfig

SENHA_TESTE = "senha-ficticia-1"


@pytest.fixture
def app():
    return create_app(TestingConfig)


@pytest.fixture
def client(app):
    return app.test_client()


def _liga_chave_estrangeira(conexao, _registro):
    cursor = conexao.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.close()


def _criar_tabelas():
    # O PostgreSQL sempre aplica chave estrangeira; o SQLite só com o pragma.
    event.listen(_db.engine, "connect", _liga_chave_estrangeira)
    _db.engine.dispose()
    _db.create_all()


@pytest.fixture
def db(app):
    """Banco SQLite em memória, criado e descartado a cada teste."""
    with app.app_context():
        _criar_tabelas()
        yield _db
        _db.session.remove()
        # Em memória: fechar a conexão descarta o banco. drop_all esbarraria
        # na chave estrangeira das tabelas que se referenciam (retificação).
        _db.engine.dispose()


@pytest.fixture
def usuario_autenticado(app):
    from flask_jwt_extended import create_access_token

    with app.app_context():
        token = create_access_token(identity="usuario-teste")
    return {"Authorization": f"Bearer {token}"}


# --- Testes de rota -----------------------------------------------------------


@pytest.fixture(scope="session")
def hash_de_teste():
    """Um hash real de SENHA_TESTE, calculado uma vez: cada hash custa ~0,3 s."""
    from werkzeug.security import generate_password_hash

    return generate_password_hash(SENHA_TESTE)


class Api:
    """Cliente de teste que fala como uma das pessoas fictícias do banco.

    Cada requisição abre e fecha o próprio contexto, como no servidor: nada
    da sessão do teste vaza para a rota. Para conferir o banco, use
    `with api.banco(): ...`.
    """

    def __init__(self, app, pessoas):
        self.app = app
        self.client = app.test_client()
        self.pessoas = pessoas  # nome → id

    def token(self, quem, **opcoes):
        from flask_jwt_extended import create_access_token

        from app.models import Usuario

        with self.app.app_context():
            usuario = _db.session.get(Usuario, self.pessoas[quem])
            return create_access_token(
                identity=str(usuario.id), additional_claims={"perfil": usuario.perfil}, **opcoes
            )

    def headers(self, quem):
        if quem is None:
            return {}
        return {"Authorization": f"Bearer {self.token(quem)}"}

    def _pedir(self, metodo, url, como, **kwargs):
        headers = {**self.headers(como), **kwargs.pop("headers", {})}
        return getattr(self.client, metodo)(url, headers=headers, **kwargs)

    def get(self, url, como="direcao", **kwargs):
        return self._pedir("get", url, como, **kwargs)

    def post(self, url, como="direcao", **kwargs):
        return self._pedir("post", url, como, **kwargs)

    def put(self, url, como="direcao", **kwargs):
        return self._pedir("put", url, como, **kwargs)

    def patch(self, url, como="direcao", **kwargs):
        return self._pedir("patch", url, como, **kwargs)

    def delete(self, url, como="direcao", **kwargs):
        return self._pedir("delete", url, como, **kwargs)

    @contextmanager
    def banco(self):
        with self.app.app_context():
            yield _db


@pytest.fixture
def api(app, hash_de_teste):
    """Banco com uma pessoa fictícia de cada perfil, mais uma inativa."""
    from app.models import AssistenteSocial, Direcao, EquipePedagogica

    with app.app_context():
        _criar_tabelas()
        pessoas = {
            "direcao": Direcao(nome="Direção Fictícia", email="direcao@exemplo.test"),
            "assistente": AssistenteSocial(nome="Bruna Fictícia", email="assistente@exemplo.test"),
            "educadora": EquipePedagogica(nome="Carlos Fictício", email="educadora@exemplo.test"),
            "inativa": EquipePedagogica(nome="Dora Fictícia", email="inativa@exemplo.test", ativo=False),
        }
        for usuario in pessoas.values():
            usuario._senha_hash = hash_de_teste
        _db.session.add_all(pessoas.values())
        _db.session.commit()
        ids = {nome: usuario.id for nome, usuario in pessoas.items()}
        _db.session.remove()
    yield Api(app, ids)
    with app.app_context():
        _db.session.remove()
        _db.engine.dispose()
