"""Token encerrado por logout. Spec 01 §1.

O `jti` fica gravado até a expiração original do token; depois disso o
token já seria recusado por expirado, e a linha pode sair.
"""

from app.extensions import db
from app.models.usuario import agora


class TokenRevogado(db.Model):
    __tablename__ = "token_revogado"

    jti = db.Column(db.String(64), primary_key=True)
    expira_em = db.Column(db.DateTime(timezone=True), nullable=False, index=True)

    @classmethod
    def revogado(cls, jti):
        return db.session.get(cls, jti) is not None

    @classmethod
    def esquecer_expirados(cls, momento=None):
        momento = momento or agora()
        db.session.execute(db.delete(cls).where(cls.expira_em < momento))

    def __repr__(self):
        return "<TokenRevogado>"
