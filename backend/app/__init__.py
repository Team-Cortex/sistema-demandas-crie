"""Servidor HTTP do sistema.

O cliente React conversa com este processo por JSON em /api.
Nenhuma rota daqui abre o banco para o navegador.
"""

import importlib
import os

from flask import Flask
from flask_cors import CORS

from app.errors import registrar_erros
from app.extensions import db, jwt, migrate
from app.routes.auditoria import bp as auditoria_bp
from app.routes.auth import bp as auth_bp
from app.routes.demandas import bp as demandas_bp
from app.routes.reunioes import bp as reunioes_bp
from app.routes.saude import bp as saude_bp
from app.routes.sessao import configurar_sessao
from app.routes.usuarios import bp as usuarios_bp
from config import CONFIGS, DevelopmentConfig, ProductionConfig


def create_app(config_object=None):
    app = Flask(__name__)
    if config_object is None:
        nome = os.environ.get("FLASK_ENV", "development")
        config_object = CONFIGS.get(nome, DevelopmentConfig)
    if config_object is ProductionConfig:
        faltando = [
            nome for nome in ("SECRET_KEY", "JWT_SECRET_KEY", "DATABASE_URL")
            if not os.environ.get(nome)
        ]
        if faltando:
            raise RuntimeError("Produção sem variável: " + ", ".join(faltando))
    app.config.from_object(config_object)

    origens = app.config.get("CORS_ORIGENS") or []
    if origens:
        CORS(app, resources={r"/api/*": {"origins": origens}})

    if app.config.get("SQLALCHEMY_DATABASE_URI"):
        # Registra as tabelas no metadata para o Alembic enxergar.
        importlib.import_module("app.models")

        db.init_app(app)
        migrate.init_app(
            app,
            db,
            directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "migrations"),
            compare_type=True,
            render_as_batch=True,
        )

    if app.config.get("JWT_SECRET_KEY"):
        jwt.init_app(app)
        configurar_sessao(jwt)

    app.register_blueprint(saude_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(usuarios_bp, url_prefix="/api")
    app.register_blueprint(auditoria_bp, url_prefix="/api")
    app.register_blueprint(reunioes_bp, url_prefix="/api")
    app.register_blueprint(demandas_bp, url_prefix="/api")
    registrar_erros(app)
    return app
