"""Evolução do assistido. Card #54, RF21 a RF26.

Dado sensível de acompanhamento da pessoa atendida, distinto do
histórico da demanda. Contrato: /api/assistidos/<id>/evolucoes.
"""

from app.extensions import db
from app.models.imutavel import SomenteInsercao
from app.models.usuario import agora

# QA06 em aberto: enquanto a instituição não fecha a lista de áreas,
# o campo é texto curto, como a categoria da demanda (A2).
AREA_MAXIMA = 80


class Evolucao(SomenteInsercao, db.Model):
    """Sem exclusão e sem edição destrutiva (RF26): corrigir é `retificar`."""

    __tablename__ = "evolucao"
    nome_registro = "A evolução"

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

    # RF24 e DER: a versão nova aponta para a que ela retifica.
    # unique: cada versão é retificada no máximo uma vez, a cadeia é linear.
    retifica_id = db.Column(
        db.ForeignKey("evolucao.id", ondelete="RESTRICT"), nullable=True, unique=True
    )

    assistido = db.relationship("Assistido")
    profissional = db.relationship("Usuario", foreign_keys=[profissional_id])
    autor = db.relationship("Usuario", foreign_keys=[autor_id])
    retifica = db.relationship(
        "Evolucao", remote_side=[id], back_populates="retificada_por"
    )
    retificada_por = db.relationship("Evolucao", back_populates="retifica", uselist=False)

    CAMPOS_RETIFICAVEIS = frozenset({"data", "area_atuacao", "descricao"})

    @property
    def vigente(self):
        return self.retificada_por is None

    @classmethod
    def do_assistido(cls, assistido_id, de=None, ate=None, area_atuacao=None, incluir_retificadas=False):
        """Evoluções do assistido em ordem cronológica (RF23), com filtros (RF25).

        `de` e `ate` são inclusivos e comparam a data da evolução.
        Por padrão só traz a versão vigente de cada evolução.
        """
        consulta = db.select(cls).where(cls.assistido_id == assistido_id)
        if de is not None:
            consulta = consulta.where(cls.data >= de)
        if ate is not None:
            consulta = consulta.where(cls.data <= ate)
        if area_atuacao:
            consulta = consulta.where(db.func.lower(cls.area_atuacao) == area_atuacao.strip().lower())
        if not incluir_retificadas:
            retificadas = db.select(cls.retifica_id).where(cls.retifica_id.is_not(None))
            consulta = consulta.where(cls.id.not_in(retificadas))
        consulta = consulta.order_by(cls.data, cls.ocorrido_em, cls.id)
        return db.session.scalars(consulta).all()

    @property
    def versoes_anteriores(self):
        """Da mais recente para a original."""
        versao, anteriores = self.retifica, []
        while versao is not None:
            anteriores.append(versao)
            versao = versao.retifica
        return anteriores

    def retificar(self, autor, **mudancas):
        """Cria a versão nova; esta fica como estava, apontada pela nova."""
        from app.errors import ErroDeNegocio

        if not self.vigente:
            raise ErroDeNegocio("Só a versão vigente da evolução pode ser retificada.")
        fora = set(mudancas) - self.CAMPOS_RETIFICAVEIS
        if fora:
            raise ValueError("Campo não retificável: " + ", ".join(sorted(fora)))
        if not mudancas:
            raise ValueError("Informe o que muda na retificação.")
        campos = {c: getattr(self, c) for c in self.CAMPOS_RETIFICAVEIS}
        campos.update(mudancas)
        return Evolucao.lancar(
            autor,
            assistido=self.assistido,
            profissional=self.profissional,
            retifica=self,
            **campos,
        )

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
