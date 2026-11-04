"""Encaminhamento à rede. Card #55, RF27 a RF29.

Direcionamento de um assistido ou de uma demanda a um serviço.
Enquanto a decisão A1 estiver aberta, o destino é texto livre
(o `destino_livre` do DER); serviço cadastrado e profissional interno
entram quando A1 fechar.
"""

from app.extensions import db
from app.models.imutavel import SemExclusao
from app.models.usuario import agora

DESTINO_MAXIMO = 200


class Encaminhamento(SemExclusao, db.Model):
    """Não há exclusão (RNF19). O desfecho é a única escrita posterior."""

    __tablename__ = "encaminhamento"
    nome_registro = "O encaminhamento"

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

    # RF28: o desfecho chega depois, uma vez, com quem registrou e quando.
    desfecho = db.Column(db.Text)
    desfecho_autor_id = db.Column(db.ForeignKey("usuario.id", ondelete="RESTRICT"))
    desfecho_em = db.Column(db.DateTime(timezone=True))

    responsavel = db.relationship("Usuario", foreign_keys=[responsavel_id])
    desfecho_autor = db.relationship("Usuario", foreign_keys=[desfecho_autor_id])
    assistido = db.relationship("Assistido")
    demanda = db.relationship("Demanda")

    @property
    def pendente(self):
        return self.desfecho is None

    @classmethod
    def pendentes(cls, responsavel_id=None, assistido_id=None):
        """Encaminhamentos sem desfecho, do mais antigo para o mais novo (RF29)."""
        consulta = db.select(cls).where(cls.desfecho.is_(None))
        if responsavel_id is not None:
            consulta = consulta.where(cls.responsavel_id == responsavel_id)
        if assistido_id is not None:
            consulta = consulta.where(cls.assistido_id == assistido_id)
        return db.session.scalars(consulta.order_by(cls.data, cls.id)).all()

    def registrar_desfecho(self, texto, autor):
        from app.errors import ErroDeNegocio

        if autor is None:
            raise ValueError("Todo desfecho precisa de autor.")
        if not isinstance(texto, str) or not texto.strip():
            raise ValueError("Escreva o desfecho do encaminhamento.")
        if not self.pendente:
            raise ErroDeNegocio("Este encaminhamento já tem desfecho registrado.")
        self.desfecho = texto.strip()
        self.desfecho_autor = autor
        self.desfecho_em = agora()

    __table_args__ = (
        db.CheckConstraint(
            "assistido_id IS NOT NULL OR demanda_id IS NOT NULL",
            name="ck_encaminhamento_tem_vinculo",
        ),
        db.CheckConstraint(
            "(desfecho IS NULL AND desfecho_autor_id IS NULL AND desfecho_em IS NULL)"
            " OR (desfecho IS NOT NULL AND desfecho_autor_id IS NOT NULL AND desfecho_em IS NOT NULL)",
            name="ck_encaminhamento_desfecho_completo",
        ),
    )

    def __init__(self, **campos):
        if {"desfecho", "desfecho_autor", "desfecho_autor_id", "desfecho_em"} & set(campos):
            raise ValueError("O desfecho é registrado depois, por registrar_desfecho.")
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
