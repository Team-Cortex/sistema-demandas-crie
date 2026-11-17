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


# --- PATCH / PUT /api/usuarios/<id> ----------------------------------------------


@pytest.mark.parametrize("metodo", ["patch", "put"])
def test_direcao_edita_nome(api, metodo):
    url = f"/api/usuarios/{api.pessoas['educadora']}"
    resposta = getattr(api, metodo)(url, json={"nome": "Carlos Fictício Souza"})
    assert resposta.status_code == 200
    assert resposta.get_json()["nome"] == "Carlos Fictício Souza"
    assert resposta.get_json()["perfil"] == "equipe_pedagogica"


def test_troca_de_perfil_muda_a_classe_e_vale_na_proxima_requisicao(api):
    from app.models import AssistenteSocial

    educadora = api.pessoas["educadora"]
    token = api.token("educadora")
    resposta = api.patch(f"/api/usuarios/{educadora}", json={"perfil": "assistente_social"})
    assert resposta.status_code == 200
    assert resposta.get_json()["perfil"] == "assistente_social"
    with api.banco() as db:
        assert type(db.session.get(Usuario, educadora)) is AssistenteSocial
    # O token antigo continua valendo, mas o perfil lido é o novo.
    corpo = api.client.get(f"/api/usuarios/{educadora}", headers={"Authorization": f"Bearer {token}"})
    assert corpo.get_json()["perfil"] == "assistente_social"


def test_profissional_promovido_a_direcao_passa_a_gerir(api):
    api.patch(f"/api/usuarios/{api.pessoas['assistente']}", json={"perfil": "direcao"})
    assert api.post("/api/usuarios", json=NOVO, como="assistente").status_code == 201


def test_reativar_pela_edicao(api):
    resposta = api.patch(f"/api/usuarios/{api.pessoas['inativa']}", json={"ativo": True})
    assert resposta.get_json()["ativo"] is True
    login = api.client.post("/api/auth/login", json={"email": "inativa@exemplo.test", "senha": "senha-ficticia-1"})
    assert login.status_code == 200


@pytest.mark.parametrize("quem", ["assistente", "educadora"])
def test_profissional_nao_edita(api, quem):
    resposta = api.patch(f"/api/usuarios/{api.pessoas['inativa']}", json={"ativo": True}, como=quem)
    assert resposta.status_code == 403
    assert resposta.get_json() == {"erro": "Você não pode alterar usuários."}


@pytest.mark.parametrize(
    "corpo, mensagem",
    [
        ({}, "Informe o que muda: nome, perfil ou ativo."),
        ({"email": "outro@exemplo.test"}, "Campo não aceito: confira o formulário."),
        ({"senha": "outra-senha-1"}, "Campo não aceito: confira o formulário."),
        ({"perfil": "coordenacao"}, "Escolha um perfil válido."),
        ({"nome": ""}, "Informe o nome."),
        ({"ativo": "talvez"}, "Use ativo true ou false."),
    ],
)
def test_edicao_invalida_devolve_422(api, corpo, mensagem):
    resposta = api.patch(f"/api/usuarios/{api.pessoas['educadora']}", json=corpo)
    assert resposta.status_code == 422
    assert resposta.get_json() == {"erro": mensagem}


@pytest.mark.parametrize("corpo", [{"perfil": "assistente_social"}, {"ativo": False}])
def test_direcao_nao_muda_o_proprio_perfil_nem_se_desativa(api, corpo):
    resposta = api.patch(f"/api/usuarios/{api.pessoas['direcao']}", json=corpo)
    assert resposta.status_code == 400
    assert resposta.get_json() == {"erro": "Você não pode alterar o próprio perfil nem desativar a própria conta."}


def test_direcao_muda_o_proprio_nome(api):
    resposta = api.patch(f"/api/usuarios/{api.pessoas['direcao']}", json={"nome": "Direção Nova", "perfil": "direcao"})
    assert resposta.status_code == 200
    assert resposta.get_json()["nome"] == "Direção Nova"


def test_editar_inexistente_devolve_404(api):
    assert api.patch("/api/usuarios/9999", json={"nome": "X"}).status_code == 404
