"""Spec 02, cards #19 e #26: /api/demandas."""

from datetime import timedelta

import pytest

from app.fuso import hoje
from app.models import Assistido, Demanda, HistoricoDemanda, Reuniao, Setor, Usuario


@pytest.fixture
def cenario(api):
    with api.banco() as db:
        direcao = db.session.get(Usuario, api.pessoas["direcao"])
        reuniao = Reuniao(data=hoje() - timedelta(days=7), setor=Setor.SAUDE, participantes=[direcao])
        assistido = Assistido(nome_tratamento="Assistido Fictício Q")
        db.session.add_all([reuniao, assistido])
        db.session.commit()
        api.reuniao_id, api.assistido_id = reuniao.id, assistido.id
    return api


def _abrir(api, como="direcao", **campos):
    corpo = {
        "descricao": "Agendar visita domiciliar com o CRAS (fictício).",
        "prioridade": "media",
        "responsavel_id": api.pessoas["assistente"],
        "prazo": (hoje() + timedelta(days=10)).isoformat(),
        "reuniao_id": api.reuniao_id,
        **campos,
    }
    return api.post("/api/demandas", json=corpo, como=como)


# --- POST e GET /<id> ------------------------------------------------------------


def test_abre_aberta_com_historico_do_autor(cenario):
    resposta = _abrir(cenario, como="educadora", categoria=" Assistência social ", assistido_id=cenario.assistido_id)
    assert resposta.status_code == 201
    corpo = resposta.get_json()
    assert corpo["estado"] == "aberta" and corpo["vencida"] is False
    assert corpo["categoria"] == "Assistência social"
    assert corpo["responsavel_nome"] == "Bruna Fictícia"
    assert corpo["assistido_id"] == cenario.assistido_id
    assert "nome_tratamento" not in resposta.get_data(as_text=True)
    [item] = corpo["historico"]
    assert item["tipo"] == "estado" and item["estado_novo"] == "aberta"
    assert item["autor_id"] == cenario.pessoas["educadora"]
    assert item["ocorrido_em"] == corpo["ultimo_movimento"]


@pytest.mark.parametrize(
    "campos, mensagem",
    [
        ({"descricao": "  "}, "Informe a descrição da demanda."),
        ({"descricao": None}, "Informe a descrição da demanda."),
        ({"prioridade": "urgentissima"}, "Escolha a prioridade: baixa, media ou alta."),
        ({"prazo": "amanhã"}, "Informe o prazo."),
        ({"responsavel_id": 9999}, "Informe um responsável ativo."),
        ({"responsavel_id": "x"}, "Informe um responsável ativo."),
        ({"reuniao_id": 9999}, "Informe uma reunião existente."),
        ({"assistido_id": 9999}, "Assistido inexistente."),
        ({"categoria": "x" * 81}, "A categoria aceita até 80 caracteres."),
        ({"estado": "concluida"}, "Campo não aceito: confira o formulário."),
    ],
)
def test_corpo_invalido_devolve_422_e_nao_grava(cenario, campos, mensagem):
    resposta = _abrir(cenario, **campos)
    assert resposta.status_code == 422
    assert resposta.get_json() == {"erro": mensagem}
    with cenario.banco() as db:
        assert db.session.query(Demanda).count() == 0


def test_responsavel_inativo_devolve_422(cenario):
    resposta = _abrir(cenario, responsavel_id=cenario.pessoas["inativa"])
    assert resposta.status_code == 422
    assert resposta.get_json() == {"erro": "Informe um responsável ativo."}


def test_consulta_a_demanda_e_o_historico(cenario):
    demanda_id = _abrir(cenario).get_json()["id"]
    detalhe = cenario.get(f"/api/demandas/{demanda_id}", como="educadora")
    assert detalhe.status_code == 200
    assert len(detalhe.get_json()["historico"]) == 1
    historico = cenario.get(f"/api/demandas/{demanda_id}/historico").get_json()
    assert historico[0]["autor_nome"] == "Direção Fictícia"
    assert set(historico[0]) == {
        "id", "tipo", "texto", "estado_anterior", "estado_novo", "autor_id", "autor_nome", "ocorrido_em",
    }


def test_demanda_inexistente_devolve_404(cenario):
    for url in ("/api/demandas/9999", "/api/demandas/9999/historico"):
        resposta = cenario.get(url)
        assert resposta.status_code == 404
        assert resposta.get_json() == {"erro": "Demanda inexistente."}


def test_sem_token_devolve_401(cenario):
    assert _abrir(cenario, como=None).status_code == 401
    with cenario.banco() as db:
        assert db.session.query(HistoricoDemanda).count() == 0
