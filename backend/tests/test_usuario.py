import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Usuario


def test_usuario_guarda_atributos_comuns(db):
    usuario = Usuario(nome="Ana Fictícia", email=" Ana@Exemplo.test ", perfil="direcao")
    db.session.add(usuario)
    db.session.commit()

    salvo = db.session.get(Usuario, usuario.id)
    assert salvo.nome == "Ana Fictícia"
    assert salvo.email == "ana@exemplo.test"
    assert salvo.perfil == "direcao"
    assert salvo.ativo is True
    assert salvo.criado_em is not None


def test_email_repetido_e_recusado_pelo_banco(db):
    db.session.add(Usuario(nome="Um", email="mesmo@exemplo.test", perfil="direcao"))
    db.session.commit()
    db.session.add(Usuario(nome="Dois", email="MESMO@exemplo.test", perfil="direcao"))
    with pytest.raises(IntegrityError):
        db.session.commit()
