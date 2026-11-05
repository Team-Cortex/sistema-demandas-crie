"""Assistido. Spec 03.

Pessoa atendida pelo CRIE. Enquanto a decisão A3 estiver aberta, a
identificação é só `nome_tratamento`, sempre fictício no repositório.
Não há documento, data de nascimento, diagnóstico nem contato.
"""

from datetime import date

from app.extensions import db
from app.models.usuario import agora


class AssistidoProfissional(db.Model):
    """Quem acompanha quem. `data_inicio` vem do DER (acompanha N:N)."""

    __tablename__ = "assistido_profissional"

    assistido_id = db.Column(db.ForeignKey("assistido.id"), primary_key=True)
    profissional_id = db.Column(db.ForeignKey("usuario.id"), primary_key=True)
    data_inicio = db.Column(db.Date, nullable=False, default=date.today)

    assistido = db.relationship("Assistido", back_populates="acompanhamentos")
    profissional = db.relationship("Profissional")


class Assistido(db.Model):
    __tablename__ = "assistido"

    id = db.Column(db.Integer, primary_key=True)
    nome_tratamento = db.Column(db.String(120), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.DateTime(timezone=True), nullable=False, default=agora)

    # Campos que a instituição autorizou guardar. Cresce quando A3 fechar.
    CAMPOS_AUTORIZADOS = frozenset({"nome_tratamento"})

    acompanhamentos = db.relationship(
        "AssistidoProfissional",
        back_populates="assistido",
        cascade="all, delete-orphan",
    )

    # Ficha do assistido (spec 03, RF20): as três listas em ordem cronológica.
    # Sem cascade de exclusão: esses registros nunca saem com o assistido.
    demandas = db.relationship(
        "Demanda",
        back_populates="assistido",
        order_by="(Demanda.criado_em, Demanda.id)",
        passive_deletes="all",
    )
    evolucoes = db.relationship(
        "Evolucao",
        back_populates="assistido",
        order_by="(Evolucao.data, Evolucao.ocorrido_em, Evolucao.id)",
        passive_deletes="all",
    )
    encaminhamentos = db.relationship(
        "Encaminhamento",
        back_populates="assistido",
        order_by="(Encaminhamento.data, Encaminhamento.id)",
        passive_deletes="all",
    )

    @property
    def evolucoes_vigentes(self):
        return [e for e in self.evolucoes if e.vigente]

    @property
    def profissionais(self):
        return [a.profissional for a in self.acompanhamentos]

    def vincular_profissional(self, profissional, data_inicio=None):
        if profissional in self.profissionais:
            return
        self.acompanhamentos.append(
            AssistidoProfissional(profissional=profissional, data_inicio=data_inicio or date.today())
        )

    def __init__(self, **campos):
        campos.setdefault("ativo", True)
        super().__init__(**campos)

    def __repr__(self):
        # Sem o nome: dado de pessoa atendida não vai para log.
        return f"<Assistido {self.id}>"
