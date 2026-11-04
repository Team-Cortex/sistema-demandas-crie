"""Histórico de demanda. Spec 02, card #53.

Cada mudança de estado e cada anotação vira uma linha nova.
Nada aqui é sobrescrito.
"""

import enum

from app.extensions import db
from app.models.demanda import EstadoDemanda, _enum
from app.models.usuario import agora


class TipoHistorico(str, enum.Enum):
    ESTADO = "estado"
    ANOTACAO = "anotacao"


class HistoricoDemanda(db.Model):
    __tablename__ = "historico_demanda"

    id = db.Column(db.Integer, primary_key=True)
    demanda_id = db.Column(db.ForeignKey("demanda.id"), nullable=False, index=True)
    autor_id = db.Column(db.ForeignKey("usuario.id"), nullable=False)
    tipo = db.Column(_enum(TipoHistorico, "tipo_historico"), nullable=False)
    estado_anterior = db.Column(_enum(EstadoDemanda, "estado_demanda"), nullable=True)
    estado_novo = db.Column(_enum(EstadoDemanda, "estado_demanda"), nullable=True)
    texto = db.Column(db.Text, nullable=False)
    ocorrido_em = db.Column(db.DateTime(timezone=True), nullable=False, default=agora, index=True)

    demanda = db.relationship("Demanda", back_populates="historico")
    autor = db.relationship("Usuario")

    def __repr__(self):
        return f"<HistoricoDemanda {self.id} {self.tipo}>"
