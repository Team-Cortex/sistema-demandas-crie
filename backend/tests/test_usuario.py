from types import SimpleNamespace

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from app.models import (
    CLASSE_POR_PERFIL,
    AssistenteSocial,
    Direcao,
    EquipePedagogica,
    Profissional,
    Usuario,
)

SENHA = "senha-ficticia-1"


def novo(**campos):
    campos.setdefault("nome", "Pessoa Fictícia")
    campos.setdefault("email", "pessoa@exemplo.test")
    campos.setdefault("senha", SENHA)
    return Direcao(**campos)


def test_usuario_guarda_atributos_comuns(db):
    usuario = novo(nome="Ana Fictícia", email=" Ana@Exemplo.test ")
    db.session.add(usuario)
    db.session.commit()

    salvo = db.session.get(Usuario, usuario.id)
    assert salvo.nome == "Ana Fictícia"
    assert salvo.email == "ana@exemplo.test"
    assert salvo.perfil == "direcao"
    assert salvo.ativo is True
    assert salvo.criado_em is not None


def test_email_repetido_e_recusado_pelo_banco(db):
    db.session.add(novo(email="mesmo@exemplo.test"))
    db.session.commit()
    db.session.add(novo(email="MESMO@exemplo.test"))
    with pytest.raises(IntegrityError):
        db.session.commit()


def test_senha_confere_so_com_a_senha_certa():
    usuario = novo()
    assert usuario.senha_confere(SENHA) is True
    assert usuario.senha_confere("outra-senha-1") is False
    assert usuario.senha_confere("") is False
    assert usuario.senha_confere(None) is False


def test_definir_senha_troca_o_hash():
    usuario = novo()
    usuario.definir_senha("nova-senha-ficticia")
    assert usuario.senha_confere("nova-senha-ficticia") is True
    assert usuario.senha_confere(SENHA) is False


@pytest.mark.parametrize("curta", ["", "1234567", None])
def test_senha_curta_e_recusada(curta):
    usuario = Direcao(nome="X", email="x@exemplo.test")
    with pytest.raises(ValueError, match="no mínimo 8"):
        usuario.definir_senha(curta)


def test_usuario_sem_senha_nao_e_gravado(db):
    db.session.add(Direcao(nome="Sem", email="sem@exemplo.test"))
    with pytest.raises(IntegrityError):
        db.session.commit()


def test_direcao_grava_perfil_e_volta_como_direcao(db):
    db.session.add(novo())
    db.session.commit()
    db.session.expunge_all()

    carregado = db.session.query(Usuario).one()
    assert type(carregado) is Direcao
    assert carregado.perfil == "direcao"


@pytest.mark.parametrize("abstrata", [Usuario, Profissional])
def test_classes_abstratas_nao_viram_linha(abstrata):
    with pytest.raises(InvalidRequestError):
        abstrata(nome="X", email="x@exemplo.test", senha=SENHA)

@pytest.mark.parametrize(
    "perfil, classe",
    [("assistente_social", AssistenteSocial), ("equipe_pedagogica", EquipePedagogica)],
)
def test_profissionais_voltam_na_subclasse_certa(db, perfil, classe):
    db.session.add(classe(nome="P", email=f"{perfil}@exemplo.test", senha=SENHA))
    db.session.commit()
    db.session.expunge_all()

    carregado = db.session.query(Usuario).one()
    assert type(carregado) is classe
    assert isinstance(carregado, Profissional)
    assert carregado.perfil == perfil


def test_consulta_por_profissional_nao_traz_direcao(db):
    db.session.add_all([
        novo(email="d@exemplo.test"),
        AssistenteSocial(nome="A", email="a@exemplo.test", senha=SENHA),
        EquipePedagogica(nome="E", email="e@exemplo.test", senha=SENHA),
    ])
    db.session.commit()
    perfis = sorted(p.perfil for p in db.session.query(Profissional).all())
    assert perfis == ["assistente_social", "equipe_pedagogica"]


def test_mapa_de_perfis_cobre_os_tres_da_spec():
    assert set(CLASSE_POR_PERFIL) == {"direcao", "assistente_social", "equipe_pedagogica"}

def _assistido(*profissionais):
    return SimpleNamespace(profissionais=list(profissionais))


def test_direcao_ativa_ve_evolucao_de_qualquer_assistido():
    assert novo().pode_ver_evolucao(_assistido()) is True


def test_usuario_inativo_nao_ve_evolucao():
    assert novo(ativo=False).pode_ver_evolucao(_assistido()) is False
    inativo = AssistenteSocial(nome="A", email="a@exemplo.test", senha=SENHA, ativo=False)
    assert inativo.pode_ver_evolucao(_assistido(inativo)) is False


@pytest.mark.parametrize("classe", [AssistenteSocial, EquipePedagogica])
def test_acesso_aberto_profissional_ve_mesmo_sem_acompanhar(classe):
    profissional = classe(nome="P", email="p@exemplo.test", senha=SENHA)
    assert profissional.pode_ver_evolucao(_assistido()) is True


def test_acesso_restrito_so_quem_acompanha(monkeypatch):
    monkeypatch.setattr(Profissional, "acesso_restrito", True)
    quem_acompanha = AssistenteSocial(nome="A", email="a@exemplo.test", senha=SENHA)
    outro = EquipePedagogica(nome="E", email="e@exemplo.test", senha=SENHA)
    assistido = _assistido(quem_acompanha)

    assert quem_acompanha.pode_ver_evolucao(assistido) is True
    assert outro.pode_ver_evolucao(assistido) is False
    assert novo().pode_ver_evolucao(assistido) is True


def test_chamada_e_a_mesma_para_todo_perfil():
    usuarios = [
        novo(email="d@exemplo.test"),
        AssistenteSocial(nome="A", email="a@exemplo.test", senha=SENHA),
        EquipePedagogica(nome="E", email="e@exemplo.test", senha=SENHA),
    ]
    assert all(u.pode_ver_evolucao(_assistido()) for u in usuarios)

def test_senha_nunca_e_recuperavel_em_texto_puro(db):
    usuario = novo()
    db.session.add(usuario)
    db.session.commit()

    # Não há atributo público com a senha nem com o hash.
    assert not hasattr(usuario, "senha")
    assert not hasattr(usuario, "senha_hash")
    publicos = {nome: getattr(usuario, nome) for nome in dir(usuario) if not nome.startswith("_")}
    assert SENHA not in [v for v in publicos.values() if isinstance(v, str)]

    # No banco só existe o hash, e ele não contém a senha.
    gravado = db.session.execute(text("SELECT senha_hash FROM usuario")).scalar_one()
    assert gravado != SENHA
    assert SENHA not in gravado
    assert gravado.startswith(("scrypt:", "pbkdf2:"))

    # A representação textual também não vaza nada.
    assert SENHA not in repr(usuario)
    assert gravado not in repr(usuario)


def test_mesma_senha_gera_hashes_diferentes():
    a, b = novo(email="a@exemplo.test"), novo(email="b@exemplo.test")
    assert a._senha_hash != b._senha_hash