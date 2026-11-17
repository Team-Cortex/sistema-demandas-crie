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


# --- GET /api/usuarios ----------------------------------------------------------


def test_lista_por_nome_com_email_para_a_direcao(api):
    corpo = api.get("/api/usuarios").get_json()
    assert [u["nome"] for u in corpo] == ["Bruna Fictícia", "Carlos Fictício", "Direção Fictícia", "Dora Fictícia"]
    assert corpo[0]["email"] == "assistente@exemplo.test"


def test_profissional_lista_sem_ver_email(api):
    resposta = api.get("/api/usuarios", como="educadora")
    assert resposta.status_code == 200
    assert all("email" not in u for u in resposta.get_json())
    assert set(resposta.get_json()[0]) == {"id", "nome", "perfil", "ativo", "criado_em"}


def test_filtra_por_ativo_e_perfil(api):
    ativos = api.get("/api/usuarios?ativo=true").get_json()
    assert "Dora Fictícia" not in [u["nome"] for u in ativos]
    inativos = api.get("/api/usuarios?ativo=false").get_json()
    assert [u["nome"] for u in inativos] == ["Dora Fictícia"]
    pedagogicos = api.get("/api/usuarios?perfil=equipe_pedagogica&ativo=true").get_json()
    assert [u["nome"] for u in pedagogicos] == ["Carlos Fictício"]


def test_filtro_invalido_devolve_422(api):
    resposta = api.get("/api/usuarios?perfil=coordenacao")
    assert resposta.status_code == 422
    assert resposta.get_json() == {"erro": "Escolha um perfil válido."}


def test_consulta_um_usuario(api):
    resposta = api.get(f"/api/usuarios/{api.pessoas['assistente']}", como="assistente")
    assert resposta.status_code == 200
    assert resposta.get_json()["nome"] == "Bruna Fictícia"
    assert "email" not in resposta.get_json()


def test_usuario_inexistente_devolve_404(api):
    resposta = api.get("/api/usuarios/9999")
    assert resposta.status_code == 404
    assert resposta.get_json() == {"erro": "Usuário inexistente."}


def test_lista_exige_token(api):
    assert api.get("/api/usuarios", como=None).status_code == 401
