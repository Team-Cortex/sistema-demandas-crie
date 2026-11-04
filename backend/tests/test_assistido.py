import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError

from app.models import Assistido


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