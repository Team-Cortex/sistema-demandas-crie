"""Erros do domínio e o formato único de resposta: {"erro": "mensagem legível"}.

| Exceção           | HTTP |
| ----------------- | ---- |
| ErroDeNegocio     | 400  |
| PermissaoNegada   | 403  |
| NaoEncontrado     | 404  |
| DadoInvalido      | 422  |
| ValidationError   | 422  (marshmallow, nos schemas)
| token ausente, inválido, expirado ou revogado | 401 (app/routes/sessao.py)
"""

from flask import jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException


class ErroDeNegocio(Exception):
    def __init__(self, mensagem):
        self.mensagem = mensagem
        super().__init__(mensagem)


class PermissaoNegada(Exception):
    def __init__(self, mensagem):
        self.mensagem = mensagem
        super().__init__(mensagem)


class NaoEncontrado(Exception):
    def __init__(self, mensagem="Recurso inexistente."):
        self.mensagem = mensagem
        super().__init__(mensagem)


class DadoInvalido(Exception):
    """Corpo ausente ou campo inválido que o schema não pega sozinho (422)."""

    def __init__(self, mensagem):
        self.mensagem = mensagem
        super().__init__(mensagem)


DADO_INVALIDO = "Confira os dados enviados."

# Erros HTTP que não vêm do domínio. Nada de texto do Werkzeug em inglês.
MENSAGEM_HTTP = {
    400: "Requisição inválida.",
    401: "Entre no sistema para continuar.",
    403: "Você não tem acesso a esta operação.",
    404: "Recurso inexistente.",
    405: "Método não aceito.",
    413: "Requisição grande demais.",
    415: "Envie os dados em JSON.",
    429: "Muitas tentativas. Aguarde um pouco e tente de novo.",
}


def primeira_mensagem(mensagens):
    """A primeira mensagem legível de um ValidationError, na ordem dos campos."""
    if isinstance(mensagens, str):
        return mensagens
    if isinstance(mensagens, dict):
        valores = mensagens.values()
    elif isinstance(mensagens, (list, tuple)):
        valores = mensagens
    else:
        return None
    for valor in valores:
        mensagem = primeira_mensagem(valor)
        if mensagem:
            return mensagem
    return None


def registrar_erros(app):
    @app.errorhandler(ErroDeNegocio)
    def negocio(erro):
        return jsonify({"erro": erro.mensagem}), 400

    @app.errorhandler(PermissaoNegada)
    def permissao(erro):
        return jsonify({"erro": erro.mensagem}), 403

    @app.errorhandler(NaoEncontrado)
    def nao_encontrado(erro):
        return jsonify({"erro": erro.mensagem}), 404

    @app.errorhandler(DadoInvalido)
    def dado_invalido(erro):
        return jsonify({"erro": erro.mensagem}), 422

    @app.errorhandler(ValidationError)
    def validacao(erro):
        return jsonify({"erro": primeira_mensagem(erro.messages) or DADO_INVALIDO}), 422

    @app.errorhandler(404)
    def inexistente(_erro):
        return jsonify({"erro": "Recurso inexistente."}), 404

    @app.errorhandler(405)
    def metodo(_erro):
        return jsonify({"erro": "Método não aceito."}), 405

    @app.errorhandler(HTTPException)
    def http(erro):
        codigo = erro.code or 500
        mensagem = MENSAGEM_HTTP.get(codigo, "Não foi possível concluir a operação.")
        return jsonify({"erro": mensagem}), codigo

    @app.errorhandler(500)
    def interno(_erro):
        return jsonify({"erro": "Não foi possível concluir a operação."}), 500
