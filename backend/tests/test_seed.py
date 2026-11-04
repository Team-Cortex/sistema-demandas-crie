import pytest

import seed
from app.models import (
    Assistido,
    Demanda,
    Direcao,
    Encaminhamento,
    Evolucao,
    HistoricoDemanda,
    Reuniao,
    Usuario,
)

AMBIENTE = {
    "FLASK_ENV": "development",
    "SEED_DIRECAO_NOME": "Direção Fictícia",
    "SEED_DIRECAO_EMAIL": "direcao@exemplo.test",
    "SEED_DIRECAO_SENHA": "senha-da-direcao-1",
    "SEED_SENHA_PADRAO": "senha-padrao-ficticia",
}


def test_recusa_producao():
    with pytest.raises(seed.SeedRecusado, match="production"):
        seed.ler_ambiente({**AMBIENTE, "FLASK_ENV": "production"})


@pytest.mark.parametrize("faltando", seed.VARIAVEIS)
def test_exige_as_variaveis_do_ambiente(faltando):
    ambiente = {k: v for k, v in AMBIENTE.items() if k != faltando}
    with pytest.raises(seed.SeedRecusado, match=faltando):
        seed.ler_ambiente(ambiente)


def test_cria_um_de_cada_tipo(db):
    resultado = seed.semear(db, seed.ler_ambiente(AMBIENTE))

    assert resultado["direcao_criada"] and resultado["demonstracao_criada"]
    direcao = db.session.scalars(db.select(Direcao)).one()
    assert direcao.email == "direcao@exemplo.test"
    assert direcao.senha_confere("senha-da-direcao-1")
    perfis = {u.perfil for u in db.session.scalars(db.select(Usuario))}
    assert perfis == {"direcao", "assistente_social", "equipe_pedagogica"}
    for model in (Assistido, Reuniao, Demanda, Evolucao, Encaminhamento, HistoricoDemanda):
        assert db.session.query(model).count() >= 1, model.__name__


def test_rodar_de_novo_nao_duplica(db):
    variaveis = seed.ler_ambiente(AMBIENTE)
    seed.semear(db, variaveis)
    contagem = {m: db.session.query(m).count() for m in (Usuario, Assistido, Demanda)}

    segunda = seed.semear(db, variaveis)
    assert segunda["direcao_criada"] is False
    assert segunda["demonstracao_criada"] is False
    assert {m: db.session.query(m).count() for m in contagem} == contagem


def test_dados_sao_ficticios(db):
    seed.semear(db, seed.ler_ambiente(AMBIENTE))
    emails = [u.email for u in db.session.scalars(db.select(Usuario))]
    assert all(e.endswith("@exemplo.test") for e in emails)
    nomes = [a.nome_tratamento for a in db.session.scalars(db.select(Assistido))]
    assert all("Fictício" in n for n in nomes)


def test_seed_nao_tem_senha_escrita_no_arquivo():
    with open(seed.__file__, encoding="utf-8") as arquivo:
        fonte = arquivo.read()
    assert "senha=\"" not in fonte and "senha='" not in fonte
    assert AMBIENTE["SEED_DIRECAO_SENHA"] not in fonte
