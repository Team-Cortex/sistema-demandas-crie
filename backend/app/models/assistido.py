"""Assistido. Spec 03.

Pessoa atendida pelo CRIE. Enquanto a decisão A3 estiver aberta, a
identificação é só `nome_tratamento`, sempre fictício no repositório.
Não há documento, data de nascimento, diagnóstico nem contato.
"""

from app.extensions import db
from app.models.usuario import agora


class Assistido(db.Model):
    __tablename__ = "assistido"

    id = db.Column(db.Integer, primary_key=True)
    nome_tratamento = db.Column(db.String(120), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.DateTime(timezone=True), nullable=False, default=agora)

    # Campos que a instituição autorizou guardar. Cresce quando A3 fechar.
    CAMPOS_AUTORIZADOS = frozenset({"nome_tratamento"})

    def __init__(self, **campos):
        campos.setdefault("ativo", True)
        super().__init__(**campos)

    def __repr__(self):
        # Sem o nome: dado de pessoa atendida não vai para log.
        return f"<Assistido {self.id}>"
