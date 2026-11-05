from datetime import date

import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError

from app.models import Assistido, AssistidoProfissional, AssistenteSocial, Direcao, EquipePedagogica

SENHA = "senha-ficticia-1"


def test_assistido_grava_so_nome_de_tratamento(db):
    assistido = Assistido(nome_tratamento="Criança Fictícia A")
    db.session.add(assistido)
    db.session.commit()

    salvo = db.session.get(Assistido, assistido.id)
    assert salvo.nome_tratamento == "Criança Fictícia A"
    assert salvo.ativo is True
    assert salvo.criado_em is not None


def test_assistido_sem_nome_nao_e_gravado(db):
    db.session.add(Assistido())
    with pytest.raises(IntegrityError):
        db.session.commit()


def test_tabela_nao_tem_campo_sensivel_alem_do_autorizado(db):
    colunas = {c["name"] for c in inspect(db.engine).get_columns("assistido")}
    assert colunas == {"id", "nome_tratamento", "ativo", "criado_em"}
    assert Assistido.CAMPOS_AUTORIZADOS == {"nome_tratamento"}


def test_repr_nao_expoe_o_nome():
    assert "Fictícia" not in repr(Assistido(nome_tratamento="Pessoa Fictícia"))

def _profissionais(db):
    a = AssistenteSocial(nome="A", email="a@exemplo.test", senha=SENHA)
    e = EquipePedagogica(nome="E", email="e@exemplo.test", senha=SENHA)
    db.session.add_all([a, e])
    return a, e


def test_vincula_profissionais_que_acompanham(db):
    a, e = _profissionais(db)
    assistido = Assistido(nome_tratamento="Fictício B")
    assistido.vincular_profissional(a, date(2026, 3, 1))
    assistido.vincular_profissional(e)
    db.session.add(assistido)
    db.session.commit()
    assistido_id = assistido.id
    db.session.expunge_all()

    salvo = db.session.get(Assistido, assistido_id)
    assert {p.email for p in salvo.profissionais} == {"a@exemplo.test", "e@exemplo.test"}
    inicio = {v.profissional.email: v.data_inicio for v in salvo.acompanhamentos}
    assert inicio["a@exemplo.test"] == date(2026, 3, 1)


def test_vincular_duas_vezes_nao_duplica(db):
    a, _ = _profissionais(db)
    assistido = Assistido(nome_tratamento="Fictício C")
    assistido.vincular_profissional(a)
    assistido.vincular_profissional(a)
    db.session.add(assistido)
    db.session.commit()
    assert db.session.query(AssistidoProfissional).count() == 1


def test_acesso_restrito_usa_o_vinculo(db, monkeypatch):
    from app.models import Profissional

    monkeypatch.setattr(Profissional, "acesso_restrito", True)
    a, e = _profissionais(db)
    assistido = Assistido(nome_tratamento="Fictício D")
    assistido.vincular_profissional(a)
    db.session.add(assistido)
    db.session.commit()

    assert a.pode_ver_evolucao(assistido) is True
    assert e.pode_ver_evolucao(assistido) is False

def test_ficha_traz_demandas_evolucoes_e_encaminhamentos_em_ordem(db):
    from app.models import Demanda, Encaminhamento, Evolucao, Prioridade, Reuniao, Setor

    a = AssistenteSocial(nome="A", email="a@exemplo.test", senha=SENHA)
    assistido = Assistido(nome_tratamento="Fictício I")
    reuniao = Reuniao(data=date(2026, 10, 6), setor=Setor.SAUDE, participantes=[a])
    db.session.add_all([a, assistido, reuniao])
    for texto in ("primeira", "segunda"):
        db.session.add(Demanda.abrir(a, descricao=texto, prioridade=Prioridade.BAIXA,
                                     prazo=date(2026, 11, 1), responsavel=a, reuniao=reuniao,
                                     assistido=assistido))
        db.session.flush()
    for dia in (20, 3):
        db.session.add(Evolucao.lancar(a, assistido=assistido, data=date(2026, 10, dia),
                                       area_atuacao="Social", descricao=f"dia {dia}"))
    for dia in (25, 9):
        db.session.add(Encaminhamento(assistido=assistido, destino=f"dia {dia}",
                                      data=date(2026, 10, dia), responsavel=a))
    db.session.commit()
    assistido_id = assistido.id
    db.session.expunge_all()

    ficha = db.session.get(Assistido, assistido_id)
    assert [d.descricao for d in ficha.demandas] == ["primeira", "segunda"]
    assert [e.descricao for e in ficha.evolucoes] == ["dia 3", "dia 20"]
    assert [e.destino for e in ficha.encaminhamentos] == ["dia 9", "dia 25"]


def test_ficha_sem_registros_traz_listas_vazias(db):
    assistido = Assistido(nome_tratamento="Fictício J")
    db.session.add(assistido)
    db.session.commit()
    assert (assistido.demandas, assistido.evolucoes, assistido.encaminhamentos) == ([], [], [])


def test_ficha_mostra_so_a_evolucao_vigente(db):
    from app.models import Evolucao

    a = AssistenteSocial(nome="A", email="a@exemplo.test", senha=SENHA)
    assistido = Assistido(nome_tratamento="Fictício K")
    v1 = Evolucao.lancar(a, assistido=assistido, data=date(2026, 10, 1),
                         area_atuacao="Social", descricao="original")
    db.session.add_all([a, assistido, v1])
    db.session.commit()
    db.session.add(v1.retificar(a, descricao="corrigida"))
    db.session.commit()

    assert [e.descricao for e in assistido.evolucoes_vigentes] == ["corrigida"]
    assert len(assistido.evolucoes) == 2