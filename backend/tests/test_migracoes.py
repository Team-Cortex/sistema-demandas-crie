import os

from app import create_app
from config import TestingConfig


def test_flask_migrate_aponta_para_backend_migrations():
    app = create_app(TestingConfig)
    migrate = app.extensions["migrate"]
    esperado = os.path.join(os.path.dirname(os.path.dirname(__file__)), "migrations")
    assert os.path.normcase(migrate.directory) == os.path.normcase(esperado)
    assert os.path.isfile(os.path.join(esperado, "env.py"))
    assert migrate.configure_args["compare_type"] is True
    assert migrate.configure_args["render_as_batch"] is True


def test_metadata_tem_todas_as_tabelas_do_dominio():
    app = create_app(TestingConfig)
    tabelas = set(app.extensions["migrate"].db.metadata.tables)
    assert {
        "usuario",
        "assistido",
        "assistido_profissional",
        "reuniao",
        "reuniao_participante",
        "demanda",
        "historico_demanda",
        "evolucao",
        "encaminhamento",
    } <= tabelas