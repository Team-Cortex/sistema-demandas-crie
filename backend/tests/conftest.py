import pytest

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


@pytest.fixture
def db(app):
    """Banco SQLite em memória, criado e descartado a cada teste."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def usuario_autenticado(app):
    from flask_jwt_extended import create_access_token

    with app.app_context():
        token = create_access_token(identity="usuario-teste")
    return {"Authorization": f"Bearer {token}"}
