"""Acesso rápido de demonstração, para apresentar o sistema sem digitar senha.

Desligado por padrão. Só existe com a variável de ambiente DEMO_ACESSO_RAPIDO=1;
sem ela, as duas rotas respondem 404, como se não existissem.

Com ela ligada:
- GET /api/demo diz que o acesso rápido está disponível e para quais perfis;
- POST /api/demo/entrar com {"perfil": "direcao" | "assistente_social" | "equipe_pedagogica"}
  entra como o usuário fictício daquele perfil. Na primeira vez, cria a carga
  fictícia do seed.py (usuários com e-mail @exemplo.test e um registro de cada tipo).

Nunca ligar com dados reais do CRIE: quem tem o endereço entra como a direção.
"""

import secrets

from flask import Blueprint, abort, current_app, jsonify

from app.extensions import db
from app.routes import corpo_json
from app.services.acesso import emitir_token
from app.services.aviso import AvisoService

bp = Blueprint("demo", __name__)

# E-mails fictícios do seed.py (domínio reservado exemplo.test).
EMAILS = {
    "direcao": "direcao@exemplo.test",
    "assistente_social": "assistente.social@exemplo.test",
    "equipe_pedagogica": "pedagogico@exemplo.test",
}
SEM_CARGA = "A carga de demonstração não está disponível neste banco."


def _ligado():
    return bool(current_app.config.get("DEMO_ACESSO_RAPIDO"))


def _usuario(email):
    from app.models import Usuario

    return db.session.scalars(db.select(Usuario).where(Usuario.email == email)).first()


def _garantir_carga():
    """Cria a direção fictícia e, se o banco não tiver assistido, a carga do seed.py."""
    import seed
    from app.models import Assistido

    senha = secrets.token_urlsafe(24)  # ninguém usa: o acesso é pelo botão
    direcao, _ = seed.garantir_direcao(db, "Direção Fictícia", EMAILS["direcao"], senha)
    if db.session.scalars(db.select(Assistido).limit(1)).first() is None:
        seed.carregar_demonstracao(db, direcao, senha)
    db.session.commit()


@bp.get("/demo")
def estado():
    if not _ligado():
        abort(404)
    return jsonify({"ativo": True, "perfis": list(EMAILS)})


@bp.post("/demo/entrar")
def entrar():
    if not _ligado():
        abort(404)
    perfil = corpo_json().get("perfil")
    if perfil not in EMAILS:
        return jsonify({"erro": "Perfil inválido."}), 422
    usuario = _usuario(EMAILS[perfil])
    if usuario is None:
        _garantir_carga()
        usuario = _usuario(EMAILS[perfil])
    if usuario is None or not usuario.ativo:
        return jsonify({"erro": SEM_CARGA}), 409
    dias = current_app.config.get("AVISO_DIAS_ANTES_DO_PRAZO", 3)
    return jsonify(
        {
            "token": emitir_token(usuario),
            "perfil": usuario.perfil,
            "usuario": {"id": usuario.id, "nome": usuario.nome, "perfil": usuario.perfil},
            "avisos": AvisoService.de_prazo(usuario, dias),
        }
    )
