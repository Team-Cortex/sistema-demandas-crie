from flask import jsonify


class ErroDeNegocio(Exception):
    def __init__(self, mensagem):
        self.mensagem = mensagem
        super().__init__(mensagem)


class PermissaoNegada(Exception):
    def __init__(self, mensagem):
        self.mensagem = mensagem
        super().__init__(mensagem)


def registrar_erros(app):
    @app.errorhandler(ErroDeNegocio)
    def negocio(erro):
        return jsonify({"erro": erro.mensagem}), 400

    @app.errorhandler(PermissaoNegada)
    def permissao(erro):
        return jsonify({"erro": erro.mensagem}), 403

    @app.errorhandler(404)
    def inexistente(_erro):
        return jsonify({"erro": "Recurso inexistente."}), 404

    @app.errorhandler(405)
    def metodo(_erro):
        return jsonify({"erro": "Método não aceito."}), 405

    @app.errorhandler(500)
    def interno(_erro):
        return jsonify({"erro": "Não foi possível concluir a operação."}), 500
