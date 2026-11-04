from datetime import date, datetime, timedelta, timezone

import pytest
from sqlalchemy.exc import IntegrityError

from app.errors import ErroDeNegocio
from app.models import Assistido, AssistenteSocial, Direcao, EquipePedagogica, Evolucao

SENHA = "senha-ficticia-1"


@pytest.fixture
def base(db):
    assistente = AssistenteSocial(nome="Assistente", email="a@exemplo.test", senha=SENHA)
    educadora = EquipePedagogica(nome="Educadora", email="e@exemplo.test", senha=SENHA)
    diretora = Direcao(nome="Diretora", email="d@exemplo.test", senha=SENHA)
    assistido = Assistido(nome_tratamento="Fictício F")
    db.session.add_all([assistente, educadora, diretora, assistido])
    db.session.commit()
    return {
        "assistente": assistente,
        "educadora": educadora,
        "diretora": diretora,
        "assistido": assistido,
    }


def nova(base, autor=None, **campos):
    campos.setdefault("assistido", base["assistido"])
    campos.setdefault("profissional", base["educadora"])
    campos.setdefault("data", date(2026, 10, 14))
    campos.setdefault("area_atuacao", "Pedagógica")
    campos.setdefault("descricao", "Participou da atividade em grupo com apoio visual.")
    return Evolucao.lancar(autor or base["educadora"], **campos)


def test_evolucao_grava_os_campos_do_card(db, base):
    evolucao = nova(base, area_atuacao="  Pedagógica ")
    db.session.add(evolucao)
    db.session.commit()
    evolucao_id = evolucao.id
    db.session.expunge_all()

    salva = db.session.get(Evolucao, evolucao_id)
    assert salva.data == date(2026, 10, 14)
    assert salva.profissional.email == "e@exemplo.test"
    assert salva.area_atuacao == "Pedagógica"
    assert salva.descricao.startswith("Participou")
    assert salva.assistido.nome_tratamento == "Fictício F"


@pytest.mark.parametrize("campo", ["descricao", "area_atuacao"])
@pytest.mark.parametrize("vazio", ["", "  ", None])
def test_texto_obrigatorio(base, campo, vazio):
    with pytest.raises(ValueError):
        nova(base, **{campo: vazio})


def test_area_longa_e_recusada(base):
    with pytest.raises(ValueError, match="80"):
        nova(base, area_atuacao="x" * 81)


@pytest.mark.parametrize("campo", ["assistido", "data"])
def test_vinculos_e_data_obrigatorios(db, base, campo):
    db.session.add(nova(base, **{campo: None}))
    with pytest.raises(IntegrityError):
        db.session.commit()


def test_repr_nao_expoe_a_descricao(base):
    assert "atividade" not in repr(nova(base))


def test_lancar_registra_autor_e_momento(db, base):
    antes = datetime.now(timezone.utc) - timedelta(seconds=1)
    evolucao = nova(base, autor=base["assistente"], profissional=base["educadora"])
    db.session.add(evolucao)
    db.session.commit()

    assert evolucao.autor is base["assistente"]
    assert evolucao.profissional is base["educadora"]
    assert evolucao.ocorrido_em.replace(tzinfo=timezone.utc) >= antes


def test_profissional_padrao_e_o_autor(base):
    evolucao = Evolucao.lancar(
        base["assistente"],
        assistido=base["assistido"],
        data=date(2026, 10, 15),
        area_atuacao="Serviço social",
        descricao="Visita domiciliar realizada.",
    )
    assert evolucao.profissional is base["assistente"]


def test_lancar_sem_autor_e_recusado(base):
    with pytest.raises(ValueError, match="autor"):
        Evolucao.lancar(None, assistido=base["assistido"], data=date(2026, 10, 15),
                        area_atuacao="X", descricao="Y")


def test_momento_nao_vem_de_fora(base):
    with pytest.raises(ValueError, match="registrado pelo servidor"):
        nova(base, ocorrido_em=datetime(2020, 1, 1, tzinfo=timezone.utc))

def _gravada(db, base):
    original = nova(base)
    db.session.add(original)
    db.session.commit()
    return original


def test_retificacao_cria_versao_nova_e_preserva_a_anterior(db, base):
    original = _gravada(db, base)
    texto_original = original.descricao

    nova_versao = original.retificar(base["diretora"], descricao="Participou com apoio verbal.")
    db.session.add(nova_versao)
    db.session.commit()
    ids = (original.id, nova_versao.id)
    db.session.expunge_all()

    antiga, atual = (db.session.get(Evolucao, i) for i in ids)
    assert antiga.descricao == texto_original
    assert antiga.vigente is False
    assert atual.vigente is True
    assert atual.descricao == "Participou com apoio verbal."
    assert atual.retifica.id == antiga.id
    # Autor e momento da alteração ficam na versão nova.
    assert atual.autor.email == "d@exemplo.test"
    assert atual.ocorrido_em >= antiga.ocorrido_em
    # O que não mudou é copiado; o profissional responsável é o mesmo.
    assert (atual.data, atual.area_atuacao) == (antiga.data, antiga.area_atuacao)
    assert atual.profissional.email == antiga.profissional.email


def test_cadeia_de_versoes_anteriores(db, base):
    v1 = _gravada(db, base)
    v2 = v1.retificar(base["educadora"], area_atuacao="Psicopedagógica")
    db.session.add(v2)
    v3 = v2.retificar(base["educadora"], data=date(2026, 10, 13))
    db.session.add(v3)
    db.session.commit()

    assert v3.versoes_anteriores == [v2, v1]
    assert [v.vigente for v in (v1, v2, v3)] == [False, False, True]


def test_versao_antiga_nao_pode_ser_retificada_de_novo(db, base):
    v1 = _gravada(db, base)
    db.session.add(v1.retificar(base["educadora"], descricao="Nova."))
    db.session.commit()
    with pytest.raises(ErroDeNegocio, match="versão vigente"):
        v1.retificar(base["educadora"], descricao="Outra.")


def test_banco_recusa_duas_retificacoes_da_mesma_versao(db, base):
    v1 = _gravada(db, base)
    a = Evolucao.lancar(base["educadora"], assistido=base["assistido"], data=v1.data,
                        area_atuacao="X", descricao="a", retifica_id=v1.id)
    b = Evolucao.lancar(base["educadora"], assistido=base["assistido"], data=v1.data,
                        area_atuacao="X", descricao="b", retifica_id=v1.id)
    db.session.add_all([a, b])
    with pytest.raises(IntegrityError):
        db.session.commit()


@pytest.mark.parametrize("mudancas", [{}, {"assistido_id": 99}, {"autor_id": 1}])
def test_retificacao_so_aceita_campos_retificaveis(db, base, mudancas):
    v1 = _gravada(db, base)
    with pytest.raises(ValueError):
        v1.retificar(base["educadora"], **mudancas)


def test_retificacao_com_descricao_vazia_e_recusada(db, base):
    v1 = _gravada(db, base)
    with pytest.raises(ValueError, match="descrição"):
        v1.retificar(base["educadora"], descricao="  ")