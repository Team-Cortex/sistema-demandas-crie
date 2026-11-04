from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError

from app.errors import ErroDeNegocio
from app.models import (
    Assistido,
    AssistenteSocial,
    Demanda,
    Encaminhamento,
    EquipePedagogica,
    Prioridade,
    Reuniao,
    Setor,
)

SENHA = "senha-ficticia-1"


@pytest.fixture
def base(db):
    assistente = AssistenteSocial(nome="Assistente", email="a@exemplo.test", senha=SENHA)
    assistido = Assistido(nome_tratamento="Fictício H")
    reuniao = Reuniao(data=date(2026, 10, 6), setor=Setor.CONVIVENCIA, participantes=[assistente])
    demanda = Demanda.abrir(
        assistente,
        descricao="Articular vaga no CRAS",
        prioridade=Prioridade.MEDIA,
        prazo=date(2026, 10, 31),
        responsavel=assistente,
        reuniao=reuniao,
        assistido=assistido,
    )
    demanda_sem_assistido = Demanda.abrir(
        assistente,
        descricao="Pedir ônibus para passeio",
        prioridade=Prioridade.BAIXA,
        prazo=date(2026, 11, 20),
        responsavel=assistente,
        reuniao=reuniao,
    )
    db.session.add_all([assistente, assistido, reuniao, demanda, demanda_sem_assistido])
    db.session.commit()
    return {
        "assistente": assistente,
        "assistido": assistido,
        "demanda": demanda,
        "demanda_sem_assistido": demanda_sem_assistido,
    }


def novo(base, **campos):
    campos.setdefault("destino", "CRAS Centro")
    campos.setdefault("data", date(2026, 10, 16))
    campos.setdefault("responsavel", base["assistente"])
    campos.setdefault("observacao", "Atualização do CadÚnico.")
    if not {"assistido", "assistido_id", "demanda", "demanda_id"} & set(campos):
        campos["assistido"] = base["assistido"]
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


def test_vincula_so_ao_assistido(db, base):
    encaminhamento = novo(base)
    db.session.add(encaminhamento)
    db.session.commit()
    assert encaminhamento.assistido is base["assistido"]
    assert encaminhamento.demanda is None


def test_vincula_a_demanda_e_herda_o_assistido_dela(db, base):
    encaminhamento = novo(base, demanda=base["demanda"])
    db.session.add(encaminhamento)
    db.session.commit()
    assert encaminhamento.demanda is base["demanda"]
    assert encaminhamento.assistido is base["assistido"]


def test_vincula_a_demanda_sem_assistido(db, base):
    encaminhamento = novo(base, demanda=base["demanda_sem_assistido"])
    db.session.add(encaminhamento)
    db.session.commit()
    assert encaminhamento.assistido is None
    assert encaminhamento.demanda is base["demanda_sem_assistido"]


def test_sem_assistido_nem_demanda_e_recusado(base):
    with pytest.raises(ValueError, match="assistido ou a demanda"):
        novo(base, assistido=None)


def test_banco_recusa_encaminhamento_sem_vinculo(db, base):
    from sqlalchemy import text

    with pytest.raises(IntegrityError):
        db.session.execute(
            text(
                "INSERT INTO encaminhamento (destino, data, responsavel_id, criado_em) "
                "VALUES ('CRAS', '2026-10-16', :r, '2026-10-16')"
            ),
            {"r": base["assistente"].id},
        )
    db.session.rollback()

def test_nasce_pendente(base):
    encaminhamento = novo(base)
    assert encaminhamento.pendente is True
    assert encaminhamento.desfecho is None


def test_registra_desfecho_com_autor_e_momento(db, base):
    encaminhamento = novo(base)
    db.session.add(encaminhamento)
    db.session.commit()

    encaminhamento.registrar_desfecho("  Família atendida; CadÚnico atualizado. ", base["assistente"])
    db.session.commit()
    encaminhamento_id = encaminhamento.id
    db.session.expunge_all()

    salvo = db.session.get(Encaminhamento, encaminhamento_id)
    assert salvo.pendente is False
    assert salvo.desfecho == "Família atendida; CadÚnico atualizado."
    assert salvo.desfecho_autor.email == "a@exemplo.test"
    assert salvo.desfecho_em is not None


def test_desfecho_nao_e_sobrescrito(db, base):
    encaminhamento = novo(base)
    encaminhamento.registrar_desfecho("Primeiro.", base["assistente"])
    with pytest.raises(ErroDeNegocio, match="já tem desfecho"):
        encaminhamento.registrar_desfecho("Segundo.", base["assistente"])
    assert encaminhamento.desfecho == "Primeiro."


@pytest.mark.parametrize("vazio", ["", "  ", None])
def test_desfecho_vazio_e_recusado(base, vazio):
    encaminhamento = novo(base)
    with pytest.raises(ValueError, match="desfecho"):
        encaminhamento.registrar_desfecho(vazio, base["assistente"])
    assert encaminhamento.pendente


def test_desfecho_sem_autor_e_recusado(base):
    with pytest.raises(ValueError, match="autor"):
        novo(base).registrar_desfecho("Ok.", None)


def test_desfecho_nao_vem_na_criacao(base):
    with pytest.raises(ValueError, match="registrado depois"):
        novo(base, desfecho="Já resolvido.")


def test_banco_recusa_desfecho_pela_metade(db, base):
    from sqlalchemy import text

    db.session.add(novo(base))
    db.session.commit()
    with pytest.raises(IntegrityError):
        db.session.execute(text("UPDATE encaminhamento SET desfecho = 'sem autor'"))
    db.session.rollback()

def test_pendentes_traz_so_os_sem_desfecho_do_mais_antigo(db, base):
    educadora = EquipePedagogica(nome="Educadora", email="e@exemplo.test", senha=SENHA)
    db.session.add(educadora)
    resolvido = novo(base, destino="CAPS", data=date(2026, 10, 1))
    resolvido.registrar_desfecho("Consulta marcada.", base["assistente"])
    db.session.add_all([
        resolvido,
        novo(base, destino="CRAS", data=date(2026, 10, 20)),
        novo(base, destino="UBS", data=date(2026, 10, 5)),
        novo(base, destino="Escola", data=date(2026, 10, 12), responsavel=educadora,
             demanda=base["demanda_sem_assistido"]),
    ])
    db.session.commit()

    assert [e.destino for e in Encaminhamento.pendentes()] == ["UBS", "Escola", "CRAS"]
    assert [e.destino for e in Encaminhamento.pendentes(responsavel_id=educadora.id)] == ["Escola"]
    assert [e.destino for e in Encaminhamento.pendentes(assistido_id=base["assistido"].id)] == [
        "UBS",
        "CRAS",
    ]


def test_registrar_desfecho_tira_da_lista_de_pendentes(db, base):
    encaminhamento = novo(base)
    db.session.add(encaminhamento)
    db.session.commit()
    assert Encaminhamento.pendentes() == [encaminhamento]

    encaminhamento.registrar_desfecho("Resolvido.", base["assistente"])
    db.session.commit()
    assert Encaminhamento.pendentes() == []