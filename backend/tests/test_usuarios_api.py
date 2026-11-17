"""Spec 01, cards #15 e #23: gestão de usuários pela direção."""

import pytest

from app.models import Usuario

NOVO = {
    "nome": "Elisa Fictícia",
    "email": "elisa@exemplo.test",
    "senha": "senha-nova-ficticia",
    "perfil": "assistente_social",
}


def _usuario(api, email):
    with api.banco() as db:
        usuario = db.session.scalars(db.select(Usuario).where(Usuario.email == email)).first()
        if usuario is not None:
            db.session.expunge(usuario)
        return usuario


# --- POST /api/usuarios -------------------------------------------------------


def test_direcao_cadastra_e_a_senha_nao_volta(api):
    resposta = api.post("/api/usuarios", json=NOVO)
    assert resposta.status_code == 201
    corpo = resposta.get_json()
    assert {k: corpo[k] for k in ("nome", "email", "perfil", "ativo")} == {
        "nome": "Elisa Fictícia",
        "email": "elisa@exemplo.test",
        "perfil": "assistente_social",
        "ativo": True,
    }
    assert corpo["criado_em"].endswith("-03:00")
    assert "senha" not in corpo and NOVO["senha"] not in resposta.get_data(as_text=True)

    salvo = _usuario(api, "elisa@exemplo.test")
    assert type(salvo).__name__ == "AssistenteSocial"
    assert salvo.senha_confere(NOVO["senha"])


def test_cadastrado_consegue_entrar(api):
    api.post("/api/usuarios", json=NOVO)
    resposta = api.client.post("/api/auth/login", json={"email": NOVO["email"], "senha": NOVO["senha"]})
    assert resposta.status_code == 200
    assert resposta.get_json()["perfil"] == "assistente_social"


@pytest.mark.parametrize("quem", ["assistente", "educadora"])
def test_profissional_nao_cadastra(api, quem):
    resposta = api.post("/api/usuarios", json=NOVO, como=quem)
    assert resposta.status_code == 403
    assert resposta.get_json() == {"erro": "Você não pode cadastrar usuários."}
    assert _usuario(api, NOVO["email"]) is None


def test_sem_token_devolve_401(api):
    assert api.post("/api/usuarios", json=NOVO, como=None).status_code == 401


@pytest.mark.parametrize("email", ["assistente@exemplo.test", " ASSISTENTE@exemplo.test ", "inativa@exemplo.test"])
def test_email_repetido_mesmo_de_conta_inativa_devolve_400(api, email):
    resposta = api.post("/api/usuarios", json={**NOVO, "email": email})
    assert resposta.status_code == 400
    assert resposta.get_json() == {"erro": "Já existe um usuário com este e-mail."}


@pytest.mark.parametrize(
    "mudanca, mensagem",
    [
        ({"senha": "1234567"}, "A senha precisa ter no mínimo 8 caracteres."),
        ({"senha": None}, "A senha precisa ter no mínimo 8 caracteres."),
        ({"perfil": "coordenacao"}, "Escolha um perfil válido."),
        ({"perfil": None}, "Escolha um perfil válido."),
        ({"nome": "   "}, "Informe o nome."),
        ({"email": "sem-arroba"}, "Informe um e-mail válido."),
        ({"cpf": "000"}, "Campo não aceito: confira o formulário."),
    ],
)
def test_dado_invalido_devolve_422_e_nao_grava(api, mudanca, mensagem):
    resposta = api.post("/api/usuarios", json={**NOVO, **mudanca})
    assert resposta.status_code == 422
    assert resposta.get_json() == {"erro": mensagem}
    assert _usuario(api, NOVO["email"]) is None


def test_corpo_vazio_devolve_422(api):
    assert api.post("/api/usuarios", json={}).status_code == 422
