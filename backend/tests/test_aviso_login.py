"""Spec 09, card #25: o login avisa das demandas vencidas ou perto do prazo."""

from datetime import timedelta

from app.fuso import hoje
from app.models import Assistido, Demanda, EstadoDemanda, Prioridade, Reuniao, Setor, Usuario

SENHA = "senha-ficticia-1"  # a mesma da fixture api (conftest)


def _entrar(api, email):
    resposta = api.client.post("/api/auth/login", json={"email": email, "senha": SENHA})
    assert resposta.status_code == 200
    return resposta.get_json()["avisos"]


def _semear(api):
    with api.banco() as db:
        direcao = db.session.get(Usuario, api.pessoas["direcao"])
        assistente = db.session.get(Usuario, api.pessoas["assistente"])
        educadora = db.session.get(Usuario, api.pessoas["educadora"])
        assistido = Assistido(nome_tratamento="Assistido Fictício K")
        reuniao = Reuniao(data=hoje(), setor=Setor.SAUDE, participantes=[direcao])
        db.session.add_all([assistido, reuniao])
        ids = {}
        for nome, dias, quem, caminho in (
            ("vencida", -2, assistente, [EstadoDemanda.EM_ANDAMENTO]),
            ("hoje", 0, assistente, []),
            ("em_tres_dias", 3, assistente, []),
            ("longe", 4, assistente, []),
            ("vencida_concluida", -5, assistente, [EstadoDemanda.EM_ANDAMENTO, EstadoDemanda.CONCLUIDA]),
            ("de_outra_pessoa", -1, educadora, []),
        ):
            demanda = Demanda.abrir(
                direcao,
                descricao=f"Avaliação fonoaudiológica {nome} (fictício).",
                categoria="Saúde",
                prioridade=Prioridade.ALTA,
                prazo=hoje() + timedelta(days=dias),
                responsavel=quem,
                reuniao=reuniao,
                assistido=assistido,
            )
            for passo in caminho:
                demanda.mudar_estado(passo, direcao)
            db.session.add(demanda)
            db.session.flush()
            ids[nome] = demanda.id
        db.session.commit()
    return ids


def test_login_avisa_vencidas_e_perto_do_prazo_de_quem_entrou(api):
    ids = _semear(api)
    avisos = _entrar(api, "assistente@exemplo.test")
    assert avisos["vencidas"] == 1
    assert avisos["perto_do_prazo"] == 2
    assert avisos["dias_de_antecedencia"] == 3
    assert [d["id"] for d in avisos["demandas"]] == [ids["vencida"], ids["hoje"], ids["em_tres_dias"]]
    assert avisos["demandas"][0] == {
        "id": ids["vencida"],
        "prazo": (hoje() - timedelta(days=2)).isoformat(),
        "estado": "em_andamento",
        "vencida": True,
    }


def test_aviso_nao_leva_descricao_categoria_nem_assistido(api):
    _semear(api)
    avisos = _entrar(api, "assistente@exemplo.test")
    for item in avisos["demandas"]:
        assert set(item) == {"id", "prazo", "estado", "vencida"}
    texto = str(avisos)
    assert "fonoaudiológica" not in texto and "Saúde" not in texto and "Fictício K" not in texto


def test_sem_pendencia_vem_vazio(api):
    _semear(api)
    assert _entrar(api, "direcao@exemplo.test") == {
        "vencidas": 0,
        "perto_do_prazo": 0,
        "dias_de_antecedencia": 3,
        "demandas": [],
    }


def test_dias_de_antecedencia_vem_da_configuracao(api):
    ids = _semear(api)
    api.app.config["AVISO_DIAS_ANTES_DO_PRAZO"] = 5
    avisos = _entrar(api, "assistente@exemplo.test")
    assert avisos["dias_de_antecedencia"] == 5
    assert ids["longe"] in [d["id"] for d in avisos["demandas"]]
