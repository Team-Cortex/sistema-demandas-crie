"""guarda o token revogado no logout

Spec 01 §1: o jti do token encerrado fica até a expiração original.
Não é registro de auditoria: linha expirada pode sair.

Revision ID: 3df29fd96f0b
Revises: b0f13416410c
Create Date: 2026-11-16 21:37:46.453457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3df29fd96f0b'
down_revision = 'b0f13416410c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('token_revogado',
    sa.Column('jti', sa.String(length=64), nullable=False),
    sa.Column('expira_em', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('jti')
    )
    with op.batch_alter_table('token_revogado', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_token_revogado_expira_em'), ['expira_em'], unique=False)


def downgrade():
    with op.batch_alter_table('token_revogado', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_token_revogado_expira_em'))

    op.drop_table('token_revogado')
