from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError, StatementError

from app.models import AssistenteSocial, Direcao, EquipePedagogica, Reuniao, Setor
from app.models.reuniao import reuniao_participante

SENHA = "senha-ficticia-1"


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

def test_reuniao_guarda_lista_de_participantes(db):
    d = Direcao(nome="Diretora", email="d@exemplo.test", senha=SENHA)
    a = AssistenteSocial(nome="Assistente", email="a@exemplo.test", senha=SENHA)
    e = EquipePedagogica(nome="Educadora", email="e@exemplo.test", senha=SENHA)
    reuniao = Reuniao(data=date(2026, 10, 8), setor=Setor.PEDAGOGICO, participantes=[e, d, a])
    db.session.add(reuniao)
    db.session.commit()
    reuniao_id = reuniao.id
    db.session.expunge_all()

    salva = db.session.get(Reuniao, reuniao_id)
    assert [p.nome for p in salva.participantes] == ["Assistente", "Diretora", "Educadora"]
    assert type(salva.participantes[0]) is AssistenteSocial


def test_participante_repetido_vira_uma_linha_so(db):
    a = AssistenteSocial(nome="A", email="a@exemplo.test", senha=SENHA)
    reuniao = Reuniao(data=date(2026, 10, 8), setor=Setor.SAUDE, participantes=[a])
    db.session.add(reuniao)
    db.session.commit()
    reuniao.participantes.append(a)
    db.session.commit()
    assert db.session.query(reuniao_participante).count() == 1

    # A chave primária composta recusa a duplicata mesmo fora do ORM.
    with pytest.raises(IntegrityError):
        db.session.execute(
            reuniao_participante.insert().values(reuniao_id=reuniao.id, usuario_id=a.id)
        )
    db.session.rollback()

def test_ficha_da_reuniao_mostra_demandas_com_estado_atual(db):
    from app.models import Demanda, EstadoDemanda, Prioridade

    a = AssistenteSocial(nome="A", email="a@exemplo.test", senha=SENHA)
    reuniao = Reuniao(data=date(2026, 10, 6), setor=Setor.SAUDE, participantes=[a])
    outra = Reuniao(data=date(2026, 10, 7), setor=Setor.PEDAGOGICO, participantes=[a])
    db.session.add_all([a, reuniao, outra])

    def abrir(texto, origem):
        demanda = Demanda.abrir(a, descricao=texto, prioridade=Prioridade.MEDIA,
                                prazo=date(2026, 11, 1), responsavel=a, reuniao=origem)
        db.session.add(demanda)
        db.session.flush()
        return demanda

    primeira = abrir("primeira", reuniao)
    abrir("segunda", reuniao)
    abrir("de outra reunião", outra)
    primeira.mudar_estado(EstadoDemanda.EM_ANDAMENTO, a)
    db.session.commit()
    reuniao_id = reuniao.id
    db.session.expunge_all()

    ficha = db.session.get(Reuniao, reuniao_id)
    assert [(d.descricao, d.estado) for d in ficha.demandas] == [
        ("primeira", EstadoDemanda.EM_ANDAMENTO),
        ("segunda", EstadoDemanda.ABERTA),
    ]


def test_reuniao_sem_demanda_traz_lista_vazia(db):
    reuniao = Reuniao(data=date(2026, 10, 6), setor=Setor.SAUDE)
    db.session.add(reuniao)
    db.session.commit()
    assert reuniao.demandas == []


def test_trocar_participantes_nao_mexe_nas_demandas(db):
    from app.models import Demanda, Prioridade

    a = AssistenteSocial(nome="A", email="a@exemplo.test", senha=SENHA)
    b = EquipePedagogica(nome="B", email="b@exemplo.test", senha=SENHA)
    reuniao = Reuniao(data=date(2026, 10, 6), setor=Setor.SAUDE, participantes=[a])
    db.session.add_all([a, b, reuniao, Demanda.abrir(a, descricao="x", prioridade=Prioridade.BAIXA,
                                                    prazo=date(2026, 11, 1), responsavel=a,
                                                    reuniao=reuniao)])
    db.session.commit()
    reuniao.participantes = [b]
    reuniao.data = date(2026, 10, 8)
    db.session.commit()
    assert len(reuniao.demandas) == 1
    assert db.session.query(Demanda).count() == 1