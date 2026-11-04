import pytest
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from app.models import Direcao, Profissional, Usuario

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