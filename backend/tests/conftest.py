import pytest

from app import create_app
from config import TestingConfig


@pytest.fixture
def app():
    return create_app(TestingConfig)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def usuario_autenticado(app):
    from flask_jwt_extended import create_access_token

    with app.app_context():
        token = create_access_token(identity="usuario-teste")
    return {"Authorization": f"Bearer {token}"}
