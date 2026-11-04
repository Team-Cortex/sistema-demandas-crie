from datetime import date, datetime, timedelta, timezone

import pytest
from sqlalchemy.exc import IntegrityError

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