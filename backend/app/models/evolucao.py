"""Evolução do assistido. Card #54, RF21 a RF26.

Dado sensível de acompanhamento da pessoa atendida, distinto do
histórico da demanda. Contrato: /api/assistidos/<id>/evolucoes.
"""

from app.extensions import db
from app.models.usuario import agora

# QA06 em aberto: enquanto a instituição não fecha a lista de áreas,
# o campo é texto curto, como a categoria da demanda (A2).
AREA_MAXIMA = 80


class Evolucao(db.Model):
    __tablename__ = "evolucao"

    id = db.Column(db.Integer, primary_key=True)
    assistido_id = db.Column(
        db.ForeignKey("assistido.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    profissional_id = db.Column(
        db.ForeignKey("usuario.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    data = db.Column(db.Date, nullable=False, index=True)
    area_atuacao = db.Column(db.String(AREA_MAXIMA), nullable=False, index=True)
    descricao = db.Column(db.Text, nullable=False)

    # RF22: quem lançou e quando. Preenchidos pelo servidor, nunca pelo corpo.
    autor_id = db.Column(db.ForeignKey("usuario.id", ondelete="RESTRICT"), nullable=False)
    ocorrido_em = db.Column(db.DateTime(timezone=True), nullable=False, default=agora)

    assistido = db.relationship("Assistido")
    profissional = db.relationship("Usuario", foreign_keys=[profissional_id])
    autor = db.relationship("Usuario", foreign_keys=[autor_id])

    @classmethod
    def lancar(cls, autor, **campos):
        """Lança a evolução com a autoria do usuário logado.

        O profissional responsável, se não vier, é o próprio autor.
        """
        if autor is None:
            raise ValueError("Toda evolução precisa de autor.")
        campos.setdefault("profissional", autor)
        return cls(autor=autor, **campos)

    def __init__(self, **campos):
        if "ocorrido_em" in campos:
            raise ValueError("O momento do lançamento é registrado pelo servidor.")
        for campo, mensagem in (
            ("descricao", "Escreva a descrição da evolução."),
            ("area_atuacao", "Informe a área de atuação."),
        ):
            valor = campos.get(campo)
            if not isinstance(valor, str) or not valor.strip():
                raise ValueError(mensagem)
            campos[campo] = valor.strip()
        if len(campos["area_atuacao"]) > AREA_MAXIMA:
            raise ValueError(f"A área de atuação aceita até {AREA_MAXIMA} caracteres.")
        super().__init__(**campos)

    def __repr__(self):
        # Sem descrição: dado sensível não vai para log.
        return f"<Evolucao {self.id}>"
