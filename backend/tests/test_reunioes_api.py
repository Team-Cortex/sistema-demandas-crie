"""Spec 04, card #18: /api/reunioes."""

from datetime import date

import pytest

from app.models import Demanda, EstadoDemanda, Prioridade, Reuniao, Usuario


def _nova(api, como="direcao", **campos):
    corpo = {
        "data": "2026-11-10",
        "setor": "saude",
        "participante_ids": [api.pessoas["assistente"], api.pessoas["direcao"]],
        **campos,
    }
    return api.post("/api/reunioes", json=corpo, como=como)


# --- POST ----------------------------------------------------------------------


def test_registra_com_participantes_e_sem_demanda(api):
    resposta = _nova(api)
    assert resposta.status_code == 201
    corpo = resposta.get_json()
    assert corpo["data"] == "2026-11-10" and corpo["setor"] == "saude"
    assert [p["nome"] for p in corpo["participantes"]] == ["Bruna Fictícia", "Direção Fictícia"]
    assert corpo["demandas"] == []
    with api.banco() as db:
        assert db.session.query(Demanda).count() == 0
        assert db.session.query(Reuniao).count() == 1


def test_qualquer_profissional_registra(api):
    assert _nova(api, participante_ids=[api.pessoas["educadora"]], como="educadora").status_code == 201


def test_id_repetido_conta_uma_vez(api):
    resposta = _nova(api, participante_ids=[api.pessoas["educadora"], api.pessoas["educadora"]])
    assert resposta.status_code == 201
    assert len(resposta.get_json()["participantes"]) == 1


@pytest.mark.parametrize(
    "campos, mensagem",
    [
        ({"setor": "financeiro"}, "Informe o setor da reunião."),
        ({"setor": None}, "Informe o setor da reunião."),
        ({"data": "10/11/2026"}, "Informe a data da reunião."),
        ({"data": None}, "Informe a data da reunião."),
        ({"participante_ids": []}, "Informe participantes ativos."),
        ({"participante_ids": ["um"]}, "Informe participantes ativos."),
        ({"participante_ids": [9999]}, "Informe participantes ativos."),
        ({"ata": "texto"}, "Campo não aceito: confira o formulário."),
    ],
)
def test_corpo_invalido_devolve_422_e_nao_grava(api, campos, mensagem):
    resposta = _nova(api, **campos)
    assert resposta.status_code == 422
    assert resposta.get_json() == {"erro": mensagem}
    with api.banco() as db:
        assert db.session.query(Reuniao).count() == 0


def test_participante_inativo_devolve_422(api):
    resposta = _nova(api, participante_ids=[api.pessoas["direcao"], api.pessoas["inativa"]])
    assert resposta.status_code == 422
    assert resposta.get_json() == {"erro": "Informe participantes ativos."}


def test_sem_token_devolve_401(api):
    assert _nova(api, como=None).status_code == 401
    assert api.get("/api/reunioes", como=None).status_code == 401


# --- GET -----------------------------------------------------------------------


def test_lista_da_mais_recente_para_a_mais_antiga(api):
    for dia, setor in (("2026-10-01", "saude"), ("2026-11-05", "pedagogico"), ("2026-10-20", "convivencia")):
        _nova(api, data=dia, setor=setor)
    corpo = api.get("/api/reunioes", como="educadora").get_json()
    assert [r["data"] for r in corpo] == ["2026-11-05", "2026-10-20", "2026-10-01"]
    assert set(corpo[0]) == {"id", "data", "setor", "participantes", "criado_em"}
    assert corpo[0]["participantes"][0] == {"id": api.pessoas["assistente"], "nome": "Bruna Fictícia"}


def test_filtra_por_setor(api):
    _nova(api, setor="saude")
    _nova(api, setor="pedagogico")
    corpo = api.get("/api/reunioes?setor=pedagogico").get_json()
    assert [r["setor"] for r in corpo] == ["pedagogico"]
    assert api.get("/api/reunioes?setor=x").status_code == 422


def test_ficha_mostra_o_estado_atual_das_demandas(api):
    reuniao_id = _nova(api).get_json()["id"]
    with api.banco() as db:
        autor = db.session.get(Usuario, api.pessoas["direcao"])
        reuniao = db.session.get(Reuniao, reuniao_id)
        for texto in ("primeira", "segunda"):
            demanda = Demanda.abrir(autor, descricao=texto, prioridade=Prioridade.MEDIA,
                                    prazo=date(2026, 12, 1), responsavel=autor, reuniao=reuniao)
            db.session.add(demanda)
            db.session.flush()
        demanda.mudar_estado(EstadoDemanda.EM_ANDAMENTO, autor)
        db.session.commit()

    corpo = api.get(f"/api/reunioes/{reuniao_id}", como="assistente").get_json()
    assert [(d["descricao"], d["estado"]) for d in corpo["demandas"]] == [
        ("primeira", "aberta"),
        ("segunda", "em_andamento"),
    ]


def test_reuniao_inexistente_devolve_404(api):
    resposta = api.get("/api/reunioes/9999")
    assert resposta.status_code == 404
    assert resposta.get_json() == {"erro": "Reunião inexistente."}


# --- PATCH / PUT ---------------------------------------------------------------


@pytest.mark.parametrize("metodo", ["patch", "put"])
def test_altera_data_setor_e_participantes(api, metodo):
    reuniao_id = _nova(api).get_json()["id"]
    resposta = getattr(api, metodo)(
        f"/api/reunioes/{reuniao_id}",
        json={"data": "2026-11-12", "setor": "convivencia", "participante_ids": [api.pessoas["educadora"]]},
        como="assistente",
    )
    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert (corpo["data"], corpo["setor"]) == ("2026-11-12", "convivencia")
    assert [p["nome"] for p in corpo["participantes"]] == ["Carlos Fictício"]


def test_altera_so_o_que_veio(api):
    reuniao_id = _nova(api).get_json()["id"]
    corpo = api.patch(f"/api/reunioes/{reuniao_id}", json={"setor": "pedagogico"}).get_json()
    assert corpo["data"] == "2026-11-10"
    assert len(corpo["participantes"]) == 2


def test_alterar_nao_apaga_demanda_ligada(api):
    reuniao_id = _nova(api).get_json()["id"]
    with api.banco() as db:
        autor = db.session.get(Usuario, api.pessoas["direcao"])
        db.session.add(Demanda.abrir(autor, descricao="ligada", prioridade=Prioridade.BAIXA,
                                     prazo=date(2026, 12, 1), responsavel=autor,
                                     reuniao=db.session.get(Reuniao, reuniao_id)))
        db.session.commit()
    corpo = api.patch(f"/api/reunioes/{reuniao_id}", json={"participante_ids": [api.pessoas["educadora"]]}).get_json()
    assert [d["descricao"] for d in corpo["demandas"]] == ["ligada"]


@pytest.mark.parametrize(
    "corpo, mensagem",
    [
        ({}, "Informe o que muda: data, setor ou participantes."),
        ({"setor": "financeiro"}, "Informe o setor da reunião."),
        ({"participante_ids": [-1]}, "Informe participantes ativos."),
        ({"participante_ids": []}, "Informe participantes ativos."),
    ],
)
def test_alteracao_invalida_devolve_422_e_nao_muda(api, corpo, mensagem):
    reuniao_id = _nova(api).get_json()["id"]
    resposta = api.patch(f"/api/reunioes/{reuniao_id}", json=corpo)
    assert resposta.status_code == 422
    assert resposta.get_json() == {"erro": mensagem}
    assert api.get(f"/api/reunioes/{reuniao_id}").get_json()["setor"] == "saude"


def test_alterar_com_participante_inativo_devolve_422(api):
    reuniao_id = _nova(api).get_json()["id"]
    resposta = api.patch(f"/api/reunioes/{reuniao_id}", json={"participante_ids": [api.pessoas["inativa"]]})
    assert resposta.status_code == 422


def test_alterar_inexistente_devolve_404(api):
    assert api.patch("/api/reunioes/9999", json={"setor": "saude"}).status_code == 404


def test_nao_existe_exclusao_de_reuniao(api):
    reuniao_id = _nova(api).get_json()["id"]
    assert api.delete(f"/api/reunioes/{reuniao_id}").status_code == 405
