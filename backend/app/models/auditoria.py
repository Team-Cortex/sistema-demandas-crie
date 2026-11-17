"""Registro de auditoria. Spec 05, card #17, RNF03.

Quem fez o quê com dado de assistido, e quando, inclusive leitura.
Somente inserção: a sessão recusa alterar e excluir (SomenteInsercao) e,
no banco, a migração nega UPDATE e DELETE por trigger.
"""

from app.extensions import db
from app.models.imutavel import SomenteInsercao
from app.models.usuario import agora

DETALHE_MAXIMO = 200

ACOES = frozenset({"criar", "alterar", "consultar", "listar", "retificar", "registrar_desfecho", "emitir"})
RECURSOS = frozenset(
    {"assistido", "evolucao", "encaminhamento", "relatorio_demandas", "relatorio_assistido"}
)


class RegistroAuditoria(SomenteInsercao, db.Model):
    __tablename__ = "auditoria"
    nome_registro = "O registro de auditoria"

    id = db.Column(db.Integer, primary_key=True)
    autor_id = db.Column(
        db.ForeignKey("usuario.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    acao = db.Column(db.String(30), nullable=False)
    recurso = db.Column(db.String(30), nullable=False, index=True)
    recurso_id = db.Column(db.Integer)
    assistido_id = db.Column(
        db.ForeignKey("assistido.id", ondelete="RESTRICT"), nullable=True, index=True
    )
    # Filtros e período usados. Nunca texto de evolução nem nome de assistido.
    detalhe = db.Column(db.String(DETALHE_MAXIMO))
    ocorrido_em = db.Column(db.DateTime(timezone=True), nullable=False, default=agora, index=True)

    autor = db.relationship("Usuario")

    def __init__(self, **campos):
        if campos.get("autor") is None and campos.get("autor_id") is None:
            raise ValueError("Todo registro de auditoria precisa de autor.")
        if campos.get("acao") not in ACOES:
            raise ValueError(f"Ação de auditoria desconhecida: {campos.get('acao')}")
        if campos.get("recurso") not in RECURSOS:
            raise ValueError(f"Recurso de auditoria desconhecido: {campos.get('recurso')}")
        if "ocorrido_em" in campos:
            raise ValueError("O momento do registro é do servidor.")
        detalhe = campos.get("detalhe")
        if detalhe is not None:
            campos["detalhe"] = detalhe[:DETALHE_MAXIMO]
        super().__init__(**campos)

    def __repr__(self):
        return f"<RegistroAuditoria {self.id} {self.acao} {self.recurso}>"
