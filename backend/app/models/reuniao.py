"""Reunião de setor. Spec 04.

Há três reuniões semanais, uma por setor. A demanda nasce numa delas.
"""

import enum

from app.extensions import db
from app.models.usuario import agora


class Setor(str, enum.Enum):
    PEDAGOGICO = "pedagogico"
    SAUDE = "saude"
    CONVIVENCIA = "convivencia"


reuniao_participante = db.Table(
    "reuniao_participante",
    db.Column("reuniao_id", db.ForeignKey("reuniao.id"), primary_key=True),
    db.Column("usuario_id", db.ForeignKey("usuario.id"), primary_key=True),
)


class Reuniao(db.Model):
    __tablename__ = "reuniao"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False, index=True)
    setor = db.Column(
        db.Enum(Setor, name="setor", values_callable=lambda e: [m.value for m in e], validate_strings=True),
        nullable=False,
    )
    criado_em = db.Column(db.DateTime(timezone=True), nullable=False, default=agora)

    participantes = db.relationship(
        "Usuario",
        secondary=reuniao_participante,
        order_by="Usuario.nome",
    )

    # Spec 04: a ficha da reunião mostra as demandas nascidas nela, com o estado atual.
    # Alterar a reunião não apaga demanda já ligada.
    demandas = db.relationship(
        "Demanda",
        back_populates="reuniao",
        order_by="(Demanda.criado_em, Demanda.id)",
        passive_deletes="all",
    )

    def __repr__(self):
        return f"<Reuniao {self.id} {self.setor.value if self.setor else None} {self.data}>"
