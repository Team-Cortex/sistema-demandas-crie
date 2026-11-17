"""Tradução HTTP. Cada blueprint novo entra por create_app, sob /api."""

from flask import request


def corpo_json():
    """O corpo JSON da requisição. Ausente ou malformado vira {}.

    Assim o schema responde 422 com a mensagem do primeiro campo que falta,
    em vez de um 400 genérico do Flask.
    """
    dados = request.get_json(silent=True)
    return {} if dados is None else dados
