from flask import Blueprint, jsonify

bp = Blueprint("saude", __name__)


@bp.get("/saude")
def saude():
    return jsonify({"ok": True, "status": "ok"})


@bp.get("/teste")
def teste():
    return "Hello World"
