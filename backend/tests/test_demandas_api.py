"""Spec 02, cards #19 e #26: /api/demandas."""

from datetime import datetime, timedelta, timezone

import pytest

from app.fuso import hoje
from app.models import (
    Assistido,
    Demanda,
    EstadoDemanda,
    HistoricoDemanda,
    Prioridade,
    Reuniao,
    Setor,
    Usuario,
)


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


# --- GET /api/demandas -------------------------------------------------------------

E = EstadoDemanda
CAMINHO = {
    E.ABERTA: [],
    E.EM_ANDAMENTO: [E.EM_ANDAMENTO],
    E.AGUARDANDO_TERCEIROS: [E.EM_ANDAMENTO, E.AGUARDANDO_TERCEIROS],
    E.CONCLUIDA: [E.EM_ANDAMENTO, E.CONCLUIDA],
    E.CANCELADA: [E.CANCELADA],
}


def _semear(api, *linhas):
    """Cada linha: (descrição, estado, dias até o prazo, responsável, categoria, com assistido, dias atrás)."""
    ids = {}
    with api.banco() as db:
        direcao = db.session.get(Usuario, api.pessoas["direcao"])
        reuniao = db.session.get(Reuniao, api.reuniao_id)
        assistido = db.session.get(Assistido, api.assistido_id)
        for descricao, estado, dias, quem, categoria, com_assistido, atras in linhas:
            demanda = Demanda.abrir(
                direcao,
                descricao=descricao,
                categoria=categoria,
                prioridade=Prioridade.MEDIA,
                prazo=hoje() + timedelta(days=dias),
                responsavel=db.session.get(Usuario, api.pessoas[quem]),
                reuniao=reuniao,
                assistido=assistido if com_assistido else None,
                criado_em=datetime.now(timezone.utc) - timedelta(days=atras),
            )
            for passo in CAMINHO[estado]:
                demanda.mudar_estado(passo, direcao)
            db.session.add(demanda)
            db.session.flush()
            ids[descricao] = demanda.id
        db.session.commit()
    return ids


@pytest.fixture
def varias(cenario):
    cenario.ids = _semear(
        cenario,
        ("Pedir transporte adaptado", E.ABERTA, 5, "assistente", "Transporte", True, 0),
        ("Renovar BPC no INSS", E.EM_ANDAMENTO, -3, "assistente", "Benefício", True, 20),
        ("Vaga na escola estadual", E.CONCLUIDA, -10, "educadora", "Educação", False, 40),
        ("Cesta básica emergencial", E.CANCELADA, -2, "educadora", None, False, 5),
        ("Aguardar CAPSi", E.AGUARDANDO_TERCEIROS, 2, "educadora", "saúde", True, 10),
    )
    return cenario


def _descricoes(resposta):
    assert resposta.status_code == 200, resposta.get_json()
    return [d["descricao"] for d in resposta.get_json()]


def test_sem_filtro_deixa_cancelada_de_fora_e_marca_vencida(varias):
    corpo = varias.get("/api/demandas", como="educadora").get_json()
    assert "Cesta básica emergencial" not in [d["descricao"] for d in corpo]
    vencida = {d["descricao"]: d["vencida"] for d in corpo}
    assert vencida["Renovar BPC no INSS"] is True
    assert vencida["Vaga na escola estadual"] is False  # concluída não vence
    assert vencida["Pedir transporte adaptado"] is False


def test_ordem_e_do_ultimo_movimento(varias):
    with varias.banco() as db:
        demanda = db.session.get(Demanda, varias.ids["Vaga na escola estadual"])
        demanda.anotar("Matrícula confirmada por telefone.", db.session.get(Usuario, varias.pessoas["direcao"]))
        db.session.commit()
    assert _descricoes(varias.get("/api/demandas"))[0] == "Vaga na escola estadual"


@pytest.mark.parametrize(
    "consulta, esperado",
    [
        ("estado=cancelada", {"Cesta básica emergencial"}),
        ("estado=aberta,em_andamento", {"Pedir transporte adaptado", "Renovar BPC no INSS"}),
        ("categoria=SAÚDE", {"Aguardar CAPSi"}),
        ("categoria=transporte", {"Pedir transporte adaptado"}),
        ("q=capsi", {"Aguardar CAPSi"}),
        ("busca=INSS", {"Renovar BPC no INSS"}),
        ("busca=cesta", {"Cesta básica emergencial"}),
        ("q=100%", set()),
    ],
)
def test_filtros_e_busca(varias, consulta, esperado):
    assert set(_descricoes(varias.get(f"/api/demandas?{consulta}"))) == esperado


def test_filtra_por_responsavel_e_assistido(varias):
    da_educadora = _descricoes(varias.get(f"/api/demandas?responsavel_id={varias.pessoas['educadora']}"))
    assert set(da_educadora) == {"Vaga na escola estadual", "Cesta básica emergencial", "Aguardar CAPSi"}
    do_assistido = _descricoes(varias.get(f"/api/demandas?assistido_id={varias.assistido_id}"))
    assert set(do_assistido) == {"Pedir transporte adaptado", "Renovar BPC no INSS", "Aguardar CAPSi"}
    assert len(_descricoes(varias.get(f"/api/demandas?reuniao_id={varias.reuniao_id}"))) == 5


def test_filtra_por_periodo_de_registro(varias):
    inicio = (hoje() - timedelta(days=25)).isoformat()
    fim = (hoje() - timedelta(days=8)).isoformat()
    assert set(_descricoes(varias.get(f"/api/demandas?periodo_inicio={inicio}&periodo_fim={fim}"))) == {
        "Renovar BPC no INSS",
        "Aguardar CAPSi",
    }
    hoje_txt = hoje().isoformat()
    assert _descricoes(varias.get(f"/api/demandas?periodo_inicio={hoje_txt}")) == ["Pedir transporte adaptado"]


@pytest.mark.parametrize(
    "consulta",
    ["estado=esquecida", "estado=aberta,x", "periodo_inicio=ontem", "responsavel_id=abc",
     "periodo_inicio=2026-11-10&periodo_fim=2026-11-01"],
)
def test_filtro_invalido_devolve_422(varias, consulta):
    resposta = varias.get(f"/api/demandas?{consulta}")
    assert resposta.status_code == 422
    assert "erro" in resposta.get_json()


def test_lista_exige_token(varias):
    assert varias.get("/api/demandas", como=None).status_code == 401


# --- PATCH /<id>/estado (card #26: transições, inclusive recusadas) ----------------

ACEITAS = [
    (E.ABERTA, E.EM_ANDAMENTO),
    (E.ABERTA, E.CANCELADA),
    (E.EM_ANDAMENTO, E.AGUARDANDO_TERCEIROS),
    (E.EM_ANDAMENTO, E.CONCLUIDA),
    (E.EM_ANDAMENTO, E.CANCELADA),
    (E.AGUARDANDO_TERCEIROS, E.EM_ANDAMENTO),
    (E.AGUARDANDO_TERCEIROS, E.CANCELADA),
]
RECUSADAS = [(de, para) for de in E for para in E if (de, para) not in ACEITAS]


def _demanda_em(api, estado):
    return _semear(api, ("Demanda de prova", estado, 5, "assistente", None, False, 0))["Demanda de prova"]


def _historico(api, demanda_id):
    with api.banco() as db:
        return db.session.query(HistoricoDemanda).filter_by(demanda_id=demanda_id).count()


@pytest.mark.parametrize("de, para", ACEITAS)
def test_transicao_aceita_grava_historico_com_autor(cenario, de, para):
    demanda_id = _demanda_em(cenario, de)
    antes = _historico(cenario, demanda_id)
    resposta = cenario.patch(f"/api/demandas/{demanda_id}/estado", json={"estado": para.value}, como="educadora")
    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert corpo["estado"] == para.value
    ultimo = corpo["historico"][-1]
    assert (ultimo["estado_anterior"], ultimo["estado_novo"]) == (de.value, para.value)
    assert ultimo["autor_id"] == cenario.pessoas["educadora"]
    assert _historico(cenario, demanda_id) == antes + 1


@pytest.mark.parametrize("de, para", RECUSADAS)
def test_transicao_recusada_devolve_400_sem_gravar(cenario, de, para):
    demanda_id = _demanda_em(cenario, de)
    antes = _historico(cenario, demanda_id)
    resposta = cenario.patch(f"/api/demandas/{demanda_id}/estado", json={"estado": para.value})
    assert resposta.status_code == 400
    assert resposta.get_json() == {"erro": "Esta demanda não pode mudar para esse estado."}
    assert _historico(cenario, demanda_id) == antes
    assert cenario.get(f"/api/demandas/{demanda_id}").get_json()["estado"] == de.value


def test_estado_fora_da_lista_devolve_400(cenario):
    demanda_id = _demanda_em(cenario, E.ABERTA)
    resposta = cenario.patch(f"/api/demandas/{demanda_id}/estado", json={"estado": "esquecida"})
    assert resposta.status_code == 400


def test_sem_estado_devolve_422(cenario):
    demanda_id = _demanda_em(cenario, E.ABERTA)
    resposta = cenario.patch(f"/api/demandas/{demanda_id}/estado", json={})
    assert resposta.status_code == 422
    assert resposta.get_json() == {"erro": "Informe o novo estado."}


def test_mudar_estado_exige_token_e_demanda_existente(cenario):
    demanda_id = _demanda_em(cenario, E.ABERTA)
    assert cenario.patch(f"/api/demandas/{demanda_id}/estado", json={"estado": "em_andamento"}, como=None).status_code == 401
    assert cenario.patch("/api/demandas/9999/estado", json={"estado": "em_andamento"}).status_code == 404


def test_nao_existe_exclusao_de_demanda(cenario):
    demanda_id = _demanda_em(cenario, E.ABERTA)
    assert cenario.delete(f"/api/demandas/{demanda_id}").status_code == 405
    assert cenario.get(f"/api/demandas/{demanda_id}").status_code == 200
