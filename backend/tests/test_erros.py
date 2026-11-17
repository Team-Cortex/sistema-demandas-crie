"""Card #16: todo erro sai como {"erro": "mensagem legível"} com o código certo."""

import pytest
from marshmallow import Schema, ValidationError, fields
from werkzeug.exceptions import BadRequest, UnsupportedMediaType

from app.errors import DadoInvalido, NaoEncontrado, primeira_mensagem


class _Prova(Schema):
    nome = fields.String(required=True, error_messages={"required": "Informe o nome."})
    idade = fields.Integer(required=True, error_messages={"required": "Informe a idade."})


def _rota(app, caminho, erro):
    def levantar():
        raise erro

    app.add_url_rule(caminho, caminho, levantar)


def test_validation_error_vira_422_com_a_primeira_mensagem(app, client):
    @app.post("/api/_prova_schema")
    def _prova():
        _Prova().load({})

    resposta = client.post("/api/_prova_schema", json={})
    assert resposta.status_code == 422
    assert resposta.get_json() == {"erro": "Informe o nome."}


def test_dado_invalido_vira_422(app, client):
    _rota(app, "/api/_prova_dado", DadoInvalido("Informe participantes ativos."))
    resposta = client.get("/api/_prova_dado")
    assert resposta.status_code == 422
    assert resposta.get_json() == {"erro": "Informe participantes ativos."}


def test_nao_encontrado_vira_404(app, client):
    _rota(app, "/api/_prova_404", NaoEncontrado("Demanda inexistente."))
    resposta = client.get("/api/_prova_404")
    assert resposta.status_code == 404
    assert resposta.get_json() == {"erro": "Demanda inexistente."}


@pytest.mark.parametrize(
    "erro, codigo, mensagem",
    [
        (BadRequest(), 400, "Requisição inválida."),
        (UnsupportedMediaType(), 415, "Envie os dados em JSON."),
    ],
)
def test_erro_http_sai_em_portugues_no_formato_unico(app, client, erro, codigo, mensagem):
    _rota(app, f"/api/_prova_http_{codigo}", erro)
    resposta = client.get(f"/api/_prova_http_{codigo}")
    assert resposta.status_code == codigo
    assert resposta.get_json() == {"erro": mensagem}


def test_metodo_nao_aceito_vira_405(client):
    resposta = client.delete("/api/saude")
    assert resposta.status_code == 405
    assert resposta.get_json() == {"erro": "Método não aceito."}


def test_excecao_inesperada_vira_500_sem_detalhe_interno(app, client):
    _rota(app, "/api/_prova_500", RuntimeError("senha do banco: segredo"))
    resposta = client.get("/api/_prova_500")
    assert resposta.status_code == 500
    assert resposta.get_json() == {"erro": "Não foi possível concluir a operação."}


def test_primeira_mensagem_percorre_dict_e_lista():
    assert primeira_mensagem({"a": ["Primeira."], "b": ["Segunda."]}) == "Primeira."
    assert primeira_mensagem({"_schema": {"x": ["Funda."]}}) == "Funda."
    assert primeira_mensagem([]) is None


def test_erro_do_banco_nao_carrega_os_valores_do_sql(db):
    """O log de um erro de banco não pode levar texto de evolução nem nome de assistido."""
    from sqlalchemy import text
    from sqlalchemy.exc import IntegrityError

    db.session.execute(text("INSERT INTO assistido (id, nome_tratamento, ativo, criado_em) "
                            "VALUES (1, 'x', 1, '2026-11-01')"))
    with pytest.raises(IntegrityError) as erro:
        db.session.execute(
            text("INSERT INTO assistido (id, nome_tratamento, ativo, criado_em) VALUES (:id, :nome, 1, '2026-11-01')"),
            {"id": 1, "nome": "Nome Sigiloso Fictício"},
        )
    assert "Nome Sigiloso Fictício" not in str(erro.value)
    db.session.rollback()


def test_validation_error_sem_mensagem_usa_texto_padrao(app, client):
    _rota(app, "/api/_prova_vazio", ValidationError({}))
    resposta = client.get("/api/_prova_vazio")
    assert resposta.status_code == 422
    assert resposta.get_json() == {"erro": "Confira os dados enviados."}
