"""Demanda e histórico imutável. Spec 02.

Núcleo do sistema: o que precisa ser feito, por quem, até quando,
e em qual reunião nasceu.
"""

import enum

from app.extensions import db
from app.models.usuario import agora

CATEGORIA_MAXIMA = 80  # decisão A2: texto curto, sem catálogo


class Prioridade(str, enum.Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"


def _enum(classe, nome):
    return db.Enum(
        classe,
        name=nome,
        values_callable=lambda e: [m.value for m in e],
        validate_strings=True,
    )


class Demanda(db.Model):
    __tablename__ = "demanda"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(CATEGORIA_MAXIMA))
    prioridade = db.Column(_enum(Prioridade, "prioridade"), nullable=False)
    prazo = db.Column(db.Date, nullable=False, index=True)

    responsavel_id = db.Column(db.ForeignKey("usuario.id"), nullable=False, index=True)
    reuniao_id = db.Column(db.ForeignKey("reuniao.id"), nullable=False, index=True)

    criado_em = db.Column(db.DateTime(timezone=True), nullable=False, default=agora)
    atualizado_em = db.Column(
        db.DateTime(timezone=True), nullable=False, default=agora, onupdate=agora
    )

    responsavel = db.relationship("Usuario")
    reuniao = db.relationship("Reuniao")

    def __init__(self, **campos):
        descricao = campos.get("descricao")
        if not isinstance(descricao, str) or not descricao.strip():
            raise ValueError("Informe a descrição da demanda.")
        campos["descricao"] = descricao.strip()
        categoria = campos.get("categoria")
        if categoria is not None:
            categoria = categoria.strip() or None
            if categoria and len(categoria) > CATEGORIA_MAXIMA:
                raise ValueError(f"A categoria aceita até {CATEGORIA_MAXIMA} caracteres.")
            campos["categoria"] = categoria
        super().__init__(**campos)

    def __repr__(self):
        return f"<Demanda {self.id}>"
