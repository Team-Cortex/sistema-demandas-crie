from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError, StatementError

from app.models import Reuniao, Setor


def test_reuniao_grava_data_e_setor(db):
    reuniao = Reuniao(data=date(2026, 10, 6), setor=Setor.SAUDE)
    db.session.add(reuniao)
    db.session.commit()
    reuniao_id = reuniao.id
    db.session.expunge_all()

    salva = db.session.get(Reuniao, reuniao_id)
    assert salva.data == date(2026, 10, 6)
    assert salva.setor is Setor.SAUDE


def test_setores_sao_os_tres_da_spec():
    assert {s.value for s in Setor} == {"pedagogico", "saude", "convivencia"}


def test_setor_aceita_o_valor_textual(db):
    db.session.add(Reuniao(data=date(2026, 10, 7), setor="convivencia"))
    db.session.commit()
    assert db.session.query(Reuniao).one().setor is Setor.CONVIVENCIA


def test_setor_desconhecido_e_recusado(db):
    db.session.add(Reuniao(data=date(2026, 10, 7), setor="financeiro"))
    with pytest.raises(StatementError):
        db.session.commit()


def test_reuniao_sem_data_nao_e_gravada(db):
    db.session.add(Reuniao(setor=Setor.PEDAGOGICO))
    with pytest.raises(IntegrityError):
        db.session.commit()