"""Usuario e subclasses. Spec 01.

Tabela única `usuario`. A coluna `perfil` diz qual papel a linha tem.
"""

from datetime import datetime, timezone

from app.extensions import db


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

    def __init__(self, **campos):
        if campos.get("email") is not None:
            campos["email"] = campos["email"].strip().lower()
        campos.setdefault("ativo", True)
        super().__init__(**campos)

    def __repr__(self):
        return f"<Usuario {self.id} {self.perfil}>"
