import os
import sqlite3

import pytest
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from flask_migrate import downgrade, upgrade

from app import create_app
from app.extensions import db
from config import TestingConfig

TABELAS = {
    "usuario",
    "assistido",
    "assistido_profissional",
    "reuniao",
    "reuniao_participante",
    "demanda",
    "historico_demanda",
    "evolucao",
    "encaminhamento",
}


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
    assert TABELAS <= set(app.extensions["migrate"].db.metadata.tables)


# --- #56.3: upgrade e downgrade de verdade, num banco em arquivo ---------------


class ConfigMigracao(TestingConfig):
    SQLALCHEMY_ENGINE_OPTIONS = {}


@pytest.fixture
def migravel(tmp_path):
    caminho = tmp_path / "migracao.db"
    config = type("C", (ConfigMigracao,), {"SQLALCHEMY_DATABASE_URI": f"sqlite:///{caminho.as_posix()}"})
    app = create_app(config)
    yield app, caminho
    with app.app_context():
        db.engine.dispose()


def _objetos(caminho, tipo):
    with sqlite3.connect(caminho) as c:
        return {r[0] for r in c.execute("select name from sqlite_master where type = ?", (tipo,))}


def test_upgrade_cria_todas_as_tabelas_e_guardas(migravel):
    app, caminho = migravel
    with app.app_context():
        upgrade()
    assert TABELAS <= _objetos(caminho, "table")
    assert _objetos(caminho, "trigger") == {
        "historico_demanda_sem_update",
        "historico_demanda_sem_delete",
        "evolucao_sem_update",
        "evolucao_sem_delete",
        "demanda_sem_delete",
        "encaminhamento_sem_delete",
    }


def test_migracao_bate_com_os_models(migravel):
    app, _ = migravel
    with app.app_context():
        upgrade()
        with db.engine.connect() as conexao:
            contexto = MigrationContext.configure(conexao, opts={"compare_type": True})
            diferencas = compare_metadata(contexto, db.metadata)
    assert diferencas == [], "rode flask db migrate: os models mudaram sem migração"


def test_downgrade_desfaz_tudo_e_upgrade_refaz(migravel):
    app, caminho = migravel
    with app.app_context():
        upgrade()
        downgrade(revision="base")
        assert _objetos(caminho, "table") == {"alembic_version"}
        assert _objetos(caminho, "trigger") == set()
        upgrade()
    assert TABELAS <= _objetos(caminho, "table")


def test_trigger_recusa_apagar_historico_mesmo_por_sql(migravel):
    app, caminho = migravel
    with app.app_context():
        upgrade()
    with sqlite3.connect(caminho) as c:
        c.executescript(
            """
            INSERT INTO usuario (id, nome, email, ativo, perfil, criado_em, senha_hash)
                VALUES (1, 'U', 'u@exemplo.test', 1, 'direcao', '2026-10-01', 'x');
            INSERT INTO reuniao (id, data, setor, criado_em) VALUES (1, '2026-10-01', 'saude', '2026-10-01');
            INSERT INTO demanda (id, descricao, prioridade, prazo, estado, responsavel_id, reuniao_id,
                                 criado_em, atualizado_em)
                VALUES (1, 'd', 'baixa', '2026-11-01', 'aberta', 1, 1, '2026-10-01', '2026-10-01');
            INSERT INTO historico_demanda (id, demanda_id, autor_id, tipo, texto, ocorrido_em)
                VALUES (1, 1, 1, 'anotacao', 't', '2026-10-01');
            """
        )
        for sql in (
            "DELETE FROM historico_demanda",
            "UPDATE historico_demanda SET texto = 'outro'",
            "DELETE FROM demanda",
        ):
            with pytest.raises(sqlite3.IntegrityError, match="não admite"):
                c.execute(sql)
        # Mudar o estado da demanda continua permitido.
        c.execute("UPDATE demanda SET estado = 'em_andamento'")
