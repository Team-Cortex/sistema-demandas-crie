"""Encaminhamento à rede. Card #55, RF27 a RF29.

Direcionamento de um assistido ou de uma demanda a um serviço.
Enquanto a decisão A1 estiver aberta, o destino é texto livre
(o `destino_livre` do DER); serviço cadastrado e profissional interno
entram quando A1 fechar.
"""

from app.extensions import db
from app.models.usuario import agora

DESTINO_MAXIMO = 200


class Encaminhamento(db.Model):
    __tablename__ = "encaminhamento"

    id = db.Column(db.Integer, primary_key=True)
    destino = db.Column(db.String(DESTINO_MAXIMO), nullable=False)
    data = db.Column(db.Date, nullable=False, index=True)
    responsavel_id = db.Column(
        db.ForeignKey("usuario.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    observacao = db.Column(db.Text)
    criado_em = db.Column(db.DateTime(timezone=True), nullable=False, default=agora)

    # Contrato: `assistido_id` ou `demanda_id`. Pode ter os dois, nunca nenhum.
    assistido_id = db.Column(
        db.ForeignKey("assistido.id", ondelete="RESTRICT"), nullable=True, index=True
    )
    demanda_id = db.Column(
        db.ForeignKey("demanda.id", ondelete="RESTRICT"), nullable=True, index=True
    )

    responsavel = db.relationship("Usuario")
    assistido = db.relationship("Assistido")
    demanda = db.relationship("Demanda")

    __table_args__ = (
        db.CheckConstraint(
            "assistido_id IS NOT NULL OR demanda_id IS NOT NULL",
            name="ck_encaminhamento_tem_vinculo",
        ),
    )

    def __init__(self, **campos):
        tem_assistido = campos.get("assistido") is not None or campos.get("assistido_id") is not None
        tem_demanda = campos.get("demanda") is not None or campos.get("demanda_id") is not None
        if not (tem_assistido or tem_demanda):
            raise ValueError("Informe o assistido ou a demanda do encaminhamento.")
        if campos.get("demanda") is not None and not tem_assistido:
            # Encaminhar a demanda de alguém também encaminha a pessoa.
            campos["assistido"] = campos["demanda"].assistido
        destino = campos.get("destino")
        if not isinstance(destino, str) or not destino.strip():
            raise ValueError("Informe o destino do encaminhamento.")
        campos["destino"] = destino.strip()
        if len(campos["destino"]) > DESTINO_MAXIMO:
            raise ValueError(f"O destino aceita até {DESTINO_MAXIMO} caracteres.")
        observacao = campos.get("observacao")
        if isinstance(observacao, str):
            campos["observacao"] = observacao.strip() or None
        super().__init__(**campos)

    def __repr__(self):
        return f"<Encaminhamento {self.id}>"
