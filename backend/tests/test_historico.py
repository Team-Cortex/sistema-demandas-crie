from datetime import date, datetime, timedelta, timezone

import pytest
from sqlalchemy.exc import IntegrityError

from app.errors import ErroDeNegocio
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


def _nova(base, autor):
    return Demanda.abrir(
        autor,
        descricao="Solicitar laudo no CAPS",
        prioridade=Prioridade.ALTA,
        prazo=date(2026, 11, 10),
        responsavel=base["responsavel"],
        reuniao=base["demanda"].reuniao,
    )


def test_abrir_grava_o_primeiro_item(db, base):
    antes = datetime.now(timezone.utc) - timedelta(seconds=1)
    demanda = _nova(base, base["diretora"])
    db.session.add(demanda)
    db.session.commit()

    (item,) = demanda.historico
    assert item.tipo is TipoHistorico.ESTADO
    assert item.estado_anterior is None
    assert item.estado_novo is EstadoDemanda.ABERTA
    assert item.autor is base["diretora"]
    assert item.ocorrido_em.replace(tzinfo=timezone.utc) >= antes


def test_cada_mudanca_aceita_gera_um_item_com_autor_e_o_que_mudou(db, base):
    demanda = _nova(base, base["diretora"])
    db.session.add(demanda)
    demanda.mudar_estado(EstadoDemanda.EM_ANDAMENTO, base["responsavel"])
    demanda.mudar_estado(EstadoDemanda.AGUARDANDO_TERCEIROS, base["responsavel"])
    db.session.commit()
    demanda_id = demanda.id
    db.session.expunge_all()

    itens = db.session.get(Demanda, demanda_id).historico
    assert [(i.estado_anterior, i.estado_novo) for i in itens] == [
        (None, EstadoDemanda.ABERTA),
        (EstadoDemanda.ABERTA, EstadoDemanda.EM_ANDAMENTO),
        (EstadoDemanda.EM_ANDAMENTO, EstadoDemanda.AGUARDANDO_TERCEIROS),
    ]
    assert [i.autor.email for i in itens] == ["d@exemplo.test", "a@exemplo.test", "a@exemplo.test"]
    assert itens[1].texto == "aberta → em_andamento"
    assert all(i.ocorrido_em is not None for i in itens)


def test_transicao_recusada_nao_grava_historico(db, base):
    demanda = _nova(base, base["diretora"])
    demanda.mudar_estado(EstadoDemanda.EM_ANDAMENTO, base["responsavel"])
    demanda.mudar_estado(EstadoDemanda.CONCLUIDA, base["responsavel"])
    db.session.add(demanda)
    db.session.commit()

    with pytest.raises(ErroDeNegocio):
        demanda.mudar_estado(EstadoDemanda.ABERTA, base["responsavel"])
    db.session.commit()
    assert len(demanda.historico) == 3
    assert demanda.estado is EstadoDemanda.CONCLUIDA


def test_mudanca_sem_autor_e_recusada(base):
    demanda = _nova(base, base["diretora"])
    with pytest.raises(ValueError, match="autor"):
        demanda.mudar_estado(EstadoDemanda.EM_ANDAMENTO, None)
    # Sem autor, o estado não muda: não existe mudança sem rastro.
    assert demanda.estado is EstadoDemanda.ABERTA
    assert len(demanda.historico) == 1

def test_anotacao_vira_item_sem_mudar_estado(db, base):
    demanda = _nova(base, base["diretora"])
    db.session.add(demanda)
    item = demanda.anotar("  Família pediu retorno por telefone.  ", base["responsavel"])
    db.session.commit()

    assert demanda.estado is EstadoDemanda.ABERTA
    assert item.tipo is TipoHistorico.ANOTACAO
    assert item.texto == "Família pediu retorno por telefone."
    assert item.autor is base["responsavel"]
    assert item.estado_anterior is None and item.estado_novo is None
    assert [i.tipo for i in demanda.historico] == [TipoHistorico.ESTADO, TipoHistorico.ANOTACAO]


@pytest.mark.parametrize("vazio", ["", "   ", None])
def test_anotacao_vazia_e_recusada(base, vazio):
    demanda = _nova(base, base["diretora"])
    with pytest.raises(ValueError, match="texto da anotação"):
        demanda.anotar(vazio, base["responsavel"])
    assert len(demanda.historico) == 1


def test_anotacao_sem_autor_e_recusada(base):
    demanda = _nova(base, base["diretora"])
    with pytest.raises(ValueError, match="autor"):
        demanda.anotar("algo", None)


def test_anotacao_em_demanda_encerrada_continua_permitida(db, base):
    demanda = _nova(base, base["diretora"])
    demanda.mudar_estado(EstadoDemanda.CANCELADA, base["diretora"])
    demanda.anotar("Cancelada porque a família mudou de cidade.", base["diretora"])
    db.session.add(demanda)
    db.session.commit()
    assert demanda.historico[-1].tipo is TipoHistorico.ANOTACAO