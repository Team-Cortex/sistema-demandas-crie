from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError

from app.models import (
    AssistenteSocial,
    Demanda,
    Direcao,
    EstadoDemanda,
    HistoricoDemanda,
    Prioridade,
    Reuniao,
    Setor,
    TipoHistorico,
)

SENHA = "senha-ficticia-1"


@pytest.fixture
def base(db):
    responsavel = AssistenteSocial(nome="Assistente", email="a@exemplo.test", senha=SENHA)
    diretora = Direcao(nome="Diretora", email="d@exemplo.test", senha=SENHA)
    reuniao = Reuniao(data=date(2026, 10, 6), setor=Setor.SAUDE, participantes=[responsavel])
    demanda = Demanda(
        descricao="Pedir avaliação na UBS",
        prioridade=Prioridade.MEDIA,
        prazo=date(2026, 10, 30),
        responsavel=responsavel,
        reuniao=reuniao,
    )
    db.session.add_all([responsavel, diretora, reuniao, demanda])
    db.session.commit()
    return {"responsavel": responsavel, "diretora": diretora, "demanda": demanda}


def test_historico_fica_vinculado_a_demanda(db, base):
    item = HistoricoDemanda(
        demanda=base["demanda"],
        autor=base["diretora"],
        tipo=TipoHistorico.ANOTACAO,
        texto="Ligar para a UBS na segunda.",
    )
    db.session.add(item)
    db.session.commit()
    demanda_id = base["demanda"].id
    db.session.expunge_all()

    demanda = db.session.get(Demanda, demanda_id)
    assert len(demanda.historico) == 1
    salvo = demanda.historico[0]
    assert salvo.tipo is TipoHistorico.ANOTACAO
    assert salvo.autor.email == "d@exemplo.test"
    assert salvo.ocorrido_em is not None


def test_item_de_estado_guarda_antes_e_depois(db, base):
    db.session.add(
        HistoricoDemanda(
            demanda=base["demanda"],
            autor=base["responsavel"],
            tipo=TipoHistorico.ESTADO,
            estado_anterior=EstadoDemanda.ABERTA,
            estado_novo=EstadoDemanda.EM_ANDAMENTO,
            texto="aberta → em_andamento",
        )
    )
    db.session.commit()
    item = db.session.query(HistoricoDemanda).one()
    assert (item.estado_anterior, item.estado_novo) == (
        EstadoDemanda.ABERTA,
        EstadoDemanda.EM_ANDAMENTO,
    )


@pytest.mark.parametrize("campo", ["demanda", "autor", "tipo", "texto"])
def test_campos_obrigatorios_do_historico(db, base, campo):
    campos = {
        "demanda": base["demanda"],
        "autor": base["diretora"],
        "tipo": TipoHistorico.ANOTACAO,
        "texto": "x",
    }
    campos[campo] = None
    db.session.add(HistoricoDemanda(**campos))
    with pytest.raises(IntegrityError):
        db.session.commit()
