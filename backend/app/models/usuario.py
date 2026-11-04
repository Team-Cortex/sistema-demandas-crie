"""Usuario e subclasses. Spec 01.

Tabela única `usuario`. A coluna `perfil` diz qual papel a linha tem.
"""

from datetime import datetime, timezone

from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db

SENHA_MINIMA = 8


def agora():
    return datetime.now(timezone.utc)


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(254), nullable=False, unique=True, index=True)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    perfil = db.Column(db.String(30), nullable=False)
    criado_em = db.Column(db.DateTime(timezone=True), nullable=False, default=agora)
    # Encapsulamento: o hash só é lido e escrito por definir_senha e senha_confere.
    _senha_hash = db.Column("senha_hash", db.String(255), nullable=False)

    def __init__(self, senha=None, **campos):
        if campos.get("email") is not None:
            campos["email"] = campos["email"].strip().lower()
        campos.setdefault("ativo", True)
        super().__init__(**campos)
        if senha is not None:
            self.definir_senha(senha)

    def definir_senha(self, senha):
        if not isinstance(senha, str) or len(senha) < SENHA_MINIMA:
            raise ValueError(f"A senha precisa ter no mínimo {SENHA_MINIMA} caracteres.")
        self._senha_hash = generate_password_hash(senha)

    def senha_confere(self, senha):
        if not self._senha_hash or not isinstance(senha, str):
            return False
        return check_password_hash(self._senha_hash, senha)

    def __repr__(self):
        return f"<Usuario {self.id} {self.perfil}>"
