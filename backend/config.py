import os
from datetime import timedelta

from dotenv import load_dotenv
from sqlalchemy.pool import StaticPool

load_dotenv()


def origens_de(valor):
    """Lista de origens do CORS. Asterisco não libera ninguém."""
    if not valor or valor.strip() == "*":
        return []
    return [parte.strip() for parte in valor.split(",") if parte.strip() and parte.strip() != "*"]


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", "30"))
    )
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-apenas-local"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "dev-apenas-local"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "")
    CORS_ORIGINS = origens_de(os.environ.get("CORS_ORIGINS", "http://localhost:5173"))


class TestingConfig(Config):
    TESTING = True
    PROPAGATE_EXCEPTIONS = False
    SECRET_KEY = "teste"
    JWT_SECRET_KEY = "teste"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool,
    }
    CORS_ORIGINS = []


class ProductionConfig(Config):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "")
    CORS_ORIGINS = origens_de(os.environ.get("CORS_ORIGINS", ""))


CONFIGS = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
