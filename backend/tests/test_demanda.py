from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError, StatementError

from sqlalchemy import text

from app.errors import ErroDeNegocio
from app.models import (
    Assistido,
    AssistenteSocial,
    Demanda,
    Direcao,
    EstadoDemanda,
    Prioridade,
    Reuniao,
    Setor,
)

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

def test_estados_sao_os_cinco_da_spec():
    assert [e.value for e in EstadoDemanda] == [
        "aberta",
        "em_andamento",
        "aguardando_terceiros",
        "concluida",
        "cancelada",
    ]


def test_demanda_nasce_aberta(db, base):
    demanda = nova(base)
    assert demanda.estado is EstadoDemanda.ABERTA
    db.session.add(demanda)
    db.session.commit()
    assert db.session.query(Demanda).one().estado is EstadoDemanda.ABERTA


def test_estado_em_texto_livre_e_recusado(base):
    with pytest.raises(ErroDeNegocio):
        nova(base, estado="esquecida")


def test_banco_tambem_recusa_texto_livre(db, base):
    db.session.add(nova(base))
    db.session.commit()
    with pytest.raises(IntegrityError):
        db.session.execute(text("UPDATE demanda SET estado = 'esquecida'"))
    db.session.rollback()


def test_banco_guarda_o_valor_do_estado(db, base):
    db.session.add(nova(base))
    db.session.commit()
    assert db.session.execute(text("SELECT estado FROM demanda")).scalar_one() == "aberta"

A = EstadoDemanda
ACEITAS = [
    (A.ABERTA, A.EM_ANDAMENTO),
    (A.ABERTA, A.CANCELADA),
    (A.EM_ANDAMENTO, A.AGUARDANDO_TERCEIROS),
    (A.EM_ANDAMENTO, A.CONCLUIDA),
    (A.EM_ANDAMENTO, A.CANCELADA),
    (A.AGUARDANDO_TERCEIROS, A.EM_ANDAMENTO),
    (A.AGUARDANDO_TERCEIROS, A.CANCELADA),
]
CAMINHO = {
    A.ABERTA: [],
    A.EM_ANDAMENTO: [A.EM_ANDAMENTO],
    A.AGUARDANDO_TERCEIROS: [A.EM_ANDAMENTO, A.AGUARDANDO_TERCEIROS],
    A.CONCLUIDA: [A.EM_ANDAMENTO, A.CONCLUIDA],
    A.CANCELADA: [A.CANCELADA],
}


def _levar_ate(demanda, estado):
    for passo in CAMINHO[estado]:
        demanda.mudar_estado(passo)


@pytest.mark.parametrize("de, para", ACEITAS)
def test_transicao_aceita(base, de, para):
    demanda = nova(base)
    _levar_ate(demanda, de)
    assert demanda.pode_mudar_para(para) is True
    assert demanda.mudar_estado(para) is de
    assert demanda.estado is para


RECUSADAS = [(de, para) for de in A for para in A if (de, para) not in ACEITAS]


@pytest.mark.parametrize("de, para", RECUSADAS)
def test_transicao_recusada(base, de, para):
    demanda = nova(base)
    _levar_ate(demanda, de)
    assert demanda.pode_mudar_para(para) is False
    with pytest.raises(ErroDeNegocio, match="não pode mudar para esse estado"):
        demanda.mudar_estado(para)
    assert demanda.estado is de


def test_concluida_para_aberta_devolve_400_pelo_tratador(app, base):
    demanda = nova(base)
    _levar_ate(demanda, A.CONCLUIDA)

    @app.get("/api/_prova_transicao")
    def _prova():
        demanda.mudar_estado("aberta")

    resposta = app.test_client().get("/api/_prova_transicao")
    assert resposta.status_code == 400
    assert resposta.get_json() == {"erro": "Esta demanda não pode mudar para esse estado."}


def test_demanda_nao_nasce_em_outro_estado(base):
    with pytest.raises(ErroDeNegocio, match="nasce aberta"):
        nova(base, estado=A.CONCLUIDA)


def test_encerrada_so_em_concluida_ou_cancelada(base):
    for estado in A:
        demanda = nova(base)
        _levar_ate(demanda, estado)
        assert demanda.encerrada is (estado in (A.CONCLUIDA, A.CANCELADA))

def test_demanda_sem_assistido_e_valida(db, base):
    db.session.add(nova(base))
    db.session.commit()
    salva = db.session.query(Demanda).one()
    assert salva.assistido_id is None
    assert salva.assistido is None


def test_demanda_ligada_a_um_assistido(db, base):
    assistido = Assistido(nome_tratamento="Fictício E")
    demanda = nova(base, assistido=assistido)
    db.session.add(demanda)
    db.session.commit()
    demanda_id = demanda.id
    db.session.expunge_all()

    salva = db.session.get(Demanda, demanda_id)
    assert salva.assistido.nome_tratamento == "Fictício E"


def test_assistido_inexistente_e_recusado_pelo_banco(db, base):
    db.session.add(nova(base, assistido_id=9999))
    with pytest.raises(IntegrityError):
        db.session.commit()
