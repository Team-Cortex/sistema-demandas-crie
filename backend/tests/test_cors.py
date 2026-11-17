"""Card #27: CORS só para as origens de CORS_ORIGINS."""

import pytest

from app import create_app
from config import TestingConfig, origens_de

FRONT = "http://front.exemplo.test"


class ConfigComFront(TestingConfig):
    CORS_ORIGINS = [FRONT]


@pytest.fixture
def com_front():
    return create_app(ConfigComFront).test_client()


def test_origem_listada_recebe_o_cabecalho(com_front):
    resposta = com_front.get("/api/saude", headers={"Origin": FRONT})
    assert resposta.headers.get("Access-Control-Allow-Origin") == FRONT


def test_origem_fora_da_lista_nao_recebe(com_front):
    resposta = com_front.get("/api/saude", headers={"Origin": "http://outro.exemplo.test"})
    assert "Access-Control-Allow-Origin" not in resposta.headers


def test_preflight_libera_authorization_em_rota_protegida(com_front):
    resposta = com_front.options(
        "/api/demandas",
        headers={
            "Origin": FRONT,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Authorization, Content-Type",
        },
    )
    assert resposta.status_code == 200
    assert resposta.headers.get("Access-Control-Allow-Origin") == FRONT
    permitidos = resposta.headers.get("Access-Control-Allow-Headers", "").lower()
    assert "authorization" in permitidos and "content-type" in permitidos
    assert "POST" in resposta.headers.get("Access-Control-Allow-Methods", "")


def test_sem_origens_configuradas_nao_ha_cors():
    cliente = create_app(TestingConfig).test_client()
    resposta = cliente.get("/api/saude", headers={"Origin": FRONT})
    assert "Access-Control-Allow-Origin" not in resposta.headers


def test_variavel_de_ambiente_vira_lista_e_asterisco_nao_abre():
    assert origens_de("http://a.exemplo.test, http://b.exemplo.test") == [
        "http://a.exemplo.test",
        "http://b.exemplo.test",
    ]
    assert origens_de("*") == []
    assert origens_de("") == []


def test_development_e_production_leem_cors_origins_do_ambiente():
    # Processo separado: a config lê o ambiente na importação.
    import os
    import subprocess
    import sys

    ambiente = {**os.environ, "CORS_ORIGINS": "http://painel.exemplo.test"}
    saida = subprocess.run(
        [sys.executable, "-c",
         "import config; print(config.DevelopmentConfig.CORS_ORIGINS, config.ProductionConfig.CORS_ORIGINS)"],
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        env=ambiente, capture_output=True, text=True, check=True,
    ).stdout.strip()
    assert saida == "['http://painel.exemplo.test'] ['http://painel.exemplo.test']"
