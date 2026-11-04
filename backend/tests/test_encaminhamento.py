from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError

from app.models import AssistenteSocial, Encaminhamento

SENHA = "senha-ficticia-1"


@pytest.fixture
def base(db):
    assistente = AssistenteSocial(nome="Assistente", email="a@exemplo.test", senha=SENHA)
    db.session.add(assistente)
    db.session.commit()
    return {"assistente": assistente}


def novo(base, **campos):
    campos.setdefault("destino", "CRAS Centro")
    campos.setdefault("data", date(2026, 10, 16))
    campos.setdefault("responsavel", base["assistente"])
    campos.setdefault("observacao", "Atualização do CadÚnico.")
    return Encaminhamento(**campos)


def test_encaminhamento_grava_os_campos_do_card(db, base):
    encaminhamento = novo(base, destino="  UBS Vila Nova ")
    db.session.add(encaminhamento)
    db.session.commit()
    encaminhamento_id = encaminhamento.id
    db.session.expunge_all()

    salvo = db.session.get(Encaminhamento, encaminhamento_id)
    assert salvo.destino == "UBS Vila Nova"
    assert salvo.data == date(2026, 10, 16)
    assert salvo.responsavel.email == "a@exemplo.test"
    assert salvo.observacao == "Atualização do CadÚnico."
    assert salvo.criado_em is not None


def test_observacao_e_opcional(db, base):
    db.session.add(novo(base, observacao="   "))
    db.session.commit()
    assert db.session.query(Encaminhamento).one().observacao is None


@pytest.mark.parametrize("vazio", ["", "  ", None])
def test_destino_obrigatorio(base, vazio):
    with pytest.raises(ValueError, match="destino"):
        novo(base, destino=vazio)


def test_destino_longo_e_recusado(base):
    with pytest.raises(ValueError, match="200"):
        novo(base, destino="x" * 201)


@pytest.mark.parametrize("campo", ["data", "responsavel"])
def test_data_e_responsavel_obrigatorios(db, base, campo):
    db.session.add(novo(base, **{campo: None}))
    with pytest.raises(IntegrityError):
        db.session.commit()
