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