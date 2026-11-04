"""Demanda e histórico imutável. Spec 02.

Núcleo do sistema: o que precisa ser feito, por quem, até quando,
e em qual reunião nasceu.
"""

import enum

from sqlalchemy.orm import validates

from app.errors import ErroDeNegocio, NaoEncontrado
from app.extensions import db
from app.models.usuario import agora

CATEGORIA_MAXIMA = 80  # decisão A2: texto curto, sem catálogo


class Prioridade(str, enum.Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"


class EstadoDemanda(str, enum.Enum):
    ABERTA = "aberta"
    EM_ANDAMENTO = "em_andamento"
    AGUARDANDO_TERCEIROS = "aguardando_terceiros"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"


# Spec 02, decisão de 13/10/2026. Concluída e cancelada são finais.
TRANSICOES = {
    EstadoDemanda.ABERTA: {EstadoDemanda.EM_ANDAMENTO, EstadoDemanda.CANCELADA},
    EstadoDemanda.EM_ANDAMENTO: {
        EstadoDemanda.AGUARDANDO_TERCEIROS,
        EstadoDemanda.CONCLUIDA,
        EstadoDemanda.CANCELADA,
    },
    EstadoDemanda.AGUARDANDO_TERCEIROS: {EstadoDemanda.EM_ANDAMENTO, EstadoDemanda.CANCELADA},
    EstadoDemanda.CONCLUIDA: set(),
    EstadoDemanda.CANCELADA: set(),
}

TRANSICAO_RECUSADA = "Esta demanda não pode mudar para esse estado."
RESPONSAVEL_INVALIDO = "Responsável inexistente ou inativo."


def _enum(classe, nome):
    return db.Enum(
        classe,
        name=nome,
        values_callable=lambda e: [m.value for m in e],
        validate_strings=True,
        create_constraint=True,
    )


class Demanda(db.Model):
    __tablename__ = "demanda"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(CATEGORIA_MAXIMA))
    prioridade = db.Column(_enum(Prioridade, "prioridade"), nullable=False)
    prazo = db.Column(db.Date, nullable=False, index=True)
    # Enumeração fechada: o banco não aceita estado fora da lista.
    estado = db.Column(
        _enum(EstadoDemanda, "estado_demanda"),
        nullable=False,
        default=EstadoDemanda.ABERTA,
        index=True,
    )

    responsavel_id = db.Column(db.ForeignKey("usuario.id"), nullable=False, index=True)
    reuniao_id = db.Column(db.ForeignKey("reuniao.id"), nullable=False, index=True)
    # Opcional: nem toda demanda é sobre uma pessoa atendida (RF11).
    assistido_id = db.Column(db.ForeignKey("assistido.id"), nullable=True, index=True)

    criado_em = db.Column(db.DateTime(timezone=True), nullable=False, default=agora)
    atualizado_em = db.Column(
        db.DateTime(timezone=True), nullable=False, default=agora, onupdate=agora
    )

    responsavel = db.relationship("Usuario")
    reuniao = db.relationship("Reuniao")
    assistido = db.relationship("Assistido")

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
        campos.setdefault("estado", EstadoDemanda.ABERTA)
        super().__init__(**campos)

    @validates("estado")
    def _valida_estado(self, _chave, novo):
        try:
            novo = EstadoDemanda(novo)
        except ValueError:
            raise ErroDeNegocio(TRANSICAO_RECUSADA) from None
        atual = self.estado
        if atual is None:
            if novo is not EstadoDemanda.ABERTA:
                raise ErroDeNegocio("Toda demanda nasce aberta.")
            return novo
        if novo not in TRANSICOES[EstadoDemanda(atual)]:
            raise ErroDeNegocio(TRANSICAO_RECUSADA)
        return novo

    def pode_mudar_para(self, novo):
        try:
            return EstadoDemanda(novo) in TRANSICOES[self.estado]
        except ValueError:
            return False

    def mudar_estado(self, novo):
        """Aplica a transição e devolve o estado anterior."""
        anterior = self.estado
        self.estado = novo
        return anterior

    def reatribuir(self, novo_responsavel):
        """Troca o responsável e devolve o anterior. Spec 02: inexistente ou inativo → 404."""
        from app.models.usuario import Usuario

        if not isinstance(novo_responsavel, Usuario) or not novo_responsavel.ativo:
            raise NaoEncontrado(RESPONSAVEL_INVALIDO)
        anterior = self.responsavel
        self.responsavel = novo_responsavel
        return anterior

    @property
    def encerrada(self):
        return self.estado in (EstadoDemanda.CONCLUIDA, EstadoDemanda.CANCELADA)

    def __repr__(self):
        return f"<Demanda {self.id}>"
