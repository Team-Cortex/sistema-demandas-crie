"""Histórico de demanda. Spec 02, card #53.

Cada mudança de estado e cada anotação vira uma linha nova.
Nada aqui é sobrescrito nem apagado: não existe método de alterar
ou excluir, a sessão recusa os dois (SomenteInsercao) e a demanda,
que é dona do histórico, também não pode ser excluída.
"""

import enum

from app.extensions import db
from app.models.demanda import EstadoDemanda, _enum
from app.models.imutavel import SomenteInsercao
from app.models.usuario import agora


class TipoHistorico(str, enum.Enum):
    ESTADO = "estado"
    ANOTACAO = "anotacao"


class HistoricoDemanda(SomenteInsercao, db.Model):
    __tablename__ = "historico_demanda"
    nome_registro = "O histórico da demanda"

    id = db.Column(db.Integer, primary_key=True)
    demanda_id = db.Column(
        db.ForeignKey("demanda.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    autor_id = db.Column(db.ForeignKey("usuario.id", ondelete="RESTRICT"), nullable=False)
    tipo = db.Column(_enum(TipoHistorico, "tipo_historico"), nullable=False)
    estado_anterior = db.Column(_enum(EstadoDemanda, "estado_demanda"), nullable=True)
    estado_novo = db.Column(_enum(EstadoDemanda, "estado_demanda"), nullable=True)
    texto = db.Column(db.Text, nullable=False)
    ocorrido_em = db.Column(db.DateTime(timezone=True), nullable=False, default=agora, index=True)

    demanda = db.relationship("Demanda", back_populates="historico")
    autor = db.relationship("Usuario")

    def __repr__(self):
        return f"<HistoricoDemanda {self.id} {self.tipo}>"
