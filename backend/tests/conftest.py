import pytest
from sqlalchemy import event

import app.models  # noqa: F401  registra as tabelas no metadata
from app import create_app
from app.extensions import db as _db
from config import TestingConfig


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


@pytest.fixture
def db(app):
    """Banco SQLite em memória, criado e descartado a cada teste."""
    with app.app_context():
        # O PostgreSQL sempre aplica chave estrangeira; o SQLite só com o pragma.
        event.listen(_db.engine, "connect", _liga_chave_estrangeira)
        _db.engine.dispose()
        _db.create_all()
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
