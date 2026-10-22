from app.errors import ErroDeNegocio, PermissaoNegada
from config import origens_de


def test_usuario_autenticado_entrega_bearer(usuario_autenticado):
    assert usuario_autenticado["Authorization"].startswith("Bearer ")


def test_rota_de_teste_responde_hello_world(client):
    resposta = client.get("/api/teste")
    assert resposta.status_code == 200
    assert resposta.get_data(as_text=True) == "Hello World"


def test_saude_publica_so_com_ok_e_status(client):
    resposta = client.get("/api/saude")
    assert resposta.status_code == 200
    assert resposta.get_json() == {"ok": True, "status": "ok"}


def test_rota_inexistente_nao_descreve_o_servidor(client):
    resposta = client.get("/api/nao-existe")
    assert resposta.status_code == 404
    assert resposta.get_json() == {"erro": "Recurso inexistente."}


def test_erro_de_negocio_vira_400(app, client):
    @app.get("/api/_prova_regra")
    def _prova():
        raise ErroDeNegocio("Transição inválida.")

    resposta = client.get("/api/_prova_regra")
    assert resposta.status_code == 400
    assert resposta.get_json() == {"erro": "Transição inválida."}


def test_permissao_negada_vira_403(app, client):
    @app.get("/api/_prova_permissao")
    def _prova():
        raise PermissaoNegada("Você não pode cadastrar usuários.")

    resposta = client.get("/api/_prova_permissao")
    assert resposta.status_code == 403
    assert resposta.get_json() == {"erro": "Você não pode cadastrar usuários."}


def test_asterisco_nao_libera_origem():
    assert origens_de("*") == []
    assert origens_de(" *, http://localhost:5173 ") == ["http://localhost:5173"]
