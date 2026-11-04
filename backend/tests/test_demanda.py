from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError, StatementError

from app.models import AssistenteSocial, Demanda, Direcao, Prioridade, Reuniao, Setor

SENHA = "senha-ficticia-1"


@pytest.fixture
def base(db):
    responsavel = AssistenteSocial(nome="Assistente", email="a@exemplo.test", senha=SENHA)
    diretora = Direcao(nome="Diretora", email="d@exemplo.test", senha=SENHA)
    reuniao = Reuniao(data=date(2026, 10, 6), setor=Setor.SAUDE, participantes=[responsavel, diretora])
    db.session.add_all([responsavel, diretora, reuniao])
    db.session.commit()
    return {"responsavel": responsavel, "diretora": diretora, "reuniao": reuniao}


def nova(base, **campos):
    campos.setdefault("descricao", "Solicitar vaga em transporte escolar adaptado")
    campos.setdefault("prioridade", Prioridade.ALTA)
    campos.setdefault("prazo", date(2026, 10, 20))
    campos.setdefault("responsavel", base["responsavel"])
    campos.setdefault("reuniao", base["reuniao"])
    return Demanda(**campos)


def test_demanda_grava_os_campos_do_card(db, base):
    demanda = nova(base, categoria=" Transporte ")
    db.session.add(demanda)
    db.session.commit()
    demanda_id = demanda.id
    db.session.expunge_all()

    salva = db.session.get(Demanda, demanda_id)
    assert salva.descricao == "Solicitar vaga em transporte escolar adaptado"
    assert salva.categoria == "Transporte"
    assert salva.prioridade is Prioridade.ALTA
    assert salva.prazo == date(2026, 10, 20)
    assert salva.responsavel.email == "a@exemplo.test"
    assert salva.reuniao.setor is Setor.SAUDE
    assert salva.criado_em is not None and salva.atualizado_em is not None


def test_categoria_e_opcional(db, base):
    db.session.add(nova(base))
    db.session.commit()
    assert db.session.query(Demanda).one().categoria is None


def test_categoria_acima_de_80_e_recusada(base):
    with pytest.raises(ValueError, match="80"):
        nova(base, categoria="x" * 81)


@pytest.mark.parametrize("vazia", ["", "   ", None])
def test_descricao_vazia_e_recusada(base, vazia):
    with pytest.raises(ValueError, match="descrição"):
        nova(base, descricao=vazia)


def test_prioridade_fora_da_lista_e_recusada(db, base):
    db.session.add(nova(base, prioridade="urgentissima"))
    with pytest.raises(StatementError):
        db.session.commit()


@pytest.mark.parametrize("campo", ["prazo", "responsavel", "reuniao", "prioridade"])
def test_campos_obrigatorios(db, base, campo):
    db.session.add(nova(base, **{campo: None}))
    with pytest.raises(IntegrityError):
        db.session.commit()