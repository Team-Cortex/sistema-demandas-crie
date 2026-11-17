"""Spec 05, card #17: o registro de auditoria é somente inserção."""

from datetime import date, datetime, timedelta, timezone

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.models import Assistido, AssistenteSocial, Direcao, RegistroAuditoria
from app.models.imutavel import RegistroImutavel
from app.services.auditoria import AuditoriaService

SENHA = "senha-ficticia-1"


@pytest.fixture
def base(db):
    diretora = Direcao(nome="Diretora", email="d@exemplo.test", senha=SENHA)
    assistente = AssistenteSocial(nome="Assistente", email="a@exemplo.test", senha=SENHA)
    assistido = Assistido(nome_tratamento="Fictício Z")
    db.session.add_all([diretora, assistente, assistido])
    db.session.commit()
    return {"diretora": diretora, "assistente": assistente, "assistido": assistido}


def _registro(base, **campos):
    campos.setdefault("autor", base["assistente"])
    campos.setdefault("acao", "consultar")
    campos.setdefault("recurso", "assistido")
    campos.setdefault("recurso_id", base["assistido"].id)
    campos.setdefault("assistido_id", base["assistido"].id)
    return RegistroAuditoria(**campos)


def test_grava_autor_acao_recurso_e_momento_do_servidor(db, base):
    antes = datetime.now(timezone.utc) - timedelta(seconds=1)
    assistido_id = base["assistido"].id
    db.session.add(_registro(base))
    db.session.commit()
    db.session.expunge_all()

    salvo = db.session.scalars(db.select(RegistroAuditoria)).one()
    assert salvo.autor.email == "a@exemplo.test"
    assert (salvo.acao, salvo.recurso) == ("consultar", "assistido")
    assert salvo.assistido_id == assistido_id
    assert salvo.ocorrido_em.replace(tzinfo=timezone.utc) >= antes


def test_sem_autor_e_recusado(base):
    with pytest.raises(ValueError, match="autor"):
        _registro(base, autor=None)


@pytest.mark.parametrize("campo, valor", [("acao", "apagar"), ("recurso", "demanda_qualquer")])
def test_acao_e_recurso_fora_da_lista_sao_recusados(base, campo, valor):
    with pytest.raises(ValueError):
        _registro(base, **{campo: valor})


def test_momento_nao_vem_de_fora(base):
    with pytest.raises(ValueError, match="servidor"):
        _registro(base, ocorrido_em=datetime(2020, 1, 1, tzinfo=timezone.utc))


def test_detalhe_longo_e_cortado_em_200(base):
    assert len(_registro(base, detalhe="x" * 300).detalhe) == 200


def test_sessao_recusa_alterar(db, base):
    registro = _registro(base)
    db.session.add(registro)
    db.session.commit()
    registro.acao = "alterar"
    with pytest.raises(RegistroImutavel, match="não admite alteração"):
        db.session.commit()
    db.session.rollback()


def test_sessao_recusa_excluir(db, base):
    registro = _registro(base)
    db.session.add(registro)
    db.session.commit()
    db.session.delete(registro)
    with pytest.raises(RegistroImutavel, match="não admite exclusão"):
        db.session.commit()
    db.session.rollback()


def test_assistido_com_auditoria_nao_sai_do_banco(db, base):
    db.session.add(_registro(base))
    db.session.commit()
    with pytest.raises(IntegrityError):
        db.session.execute(text("DELETE FROM assistido"))
    db.session.rollback()


def test_registrar_leitura_grava_na_hora(db, base):
    AuditoriaService.registrar_leitura(base["diretora"], "listar", "assistido")
    db.session.rollback()  # nada pendente: já foi gravado
    assert db.session.query(RegistroAuditoria).count() == 1


def test_consulta_filtra_e_pagina_do_mais_recente(db, base):
    for _ in range(3):
        AuditoriaService.registrar_leitura(base["assistente"], "consultar", "assistido", assistido_id=base["assistido"].id)
    AuditoriaService.registrar_leitura(base["diretora"], "listar", "assistido")

    itens, total = AuditoriaService.consultar(autor_id=base["assistente"].id, por_pagina=2)
    assert total == 3 and len(itens) == 2
    assert itens[0].id > itens[1].id
    itens, total = AuditoriaService.consultar(acao="listar")
    assert [i.autor_id for i in itens] == [base["diretora"].id]
    hoje = datetime.now(timezone(timedelta(hours=-3))).date()
    assert AuditoriaService.consultar(de=hoje, ate=hoje)[1] == 4
    assert AuditoriaService.consultar(ate=date(2000, 1, 1))[1] == 0
