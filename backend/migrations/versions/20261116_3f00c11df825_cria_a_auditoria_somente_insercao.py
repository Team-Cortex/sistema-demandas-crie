"""cria a auditoria somente inserção

Spec 05, card #17, RNF03. Como o histórico da demanda, a auditoria recusa
UPDATE e DELETE também no banco, para quem escrever SQL direto. No
PostgreSQL o trigger reaproveita a função recusa_alteracao() da migração
inicial (b0f13416410c).

Revision ID: 3f00c11df825
Revises: 3df29fd96f0b
Create Date: 2026-11-16 21:50:29.504003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f00c11df825'
down_revision = '3df29fd96f0b'
branch_labels = None
depends_on = None


OPERACOES_RECUSADAS = ('UPDATE', 'DELETE')


def _dialeto():
    return op.get_context().dialect.name


def _cria_guardas():
    if _dialeto() == 'postgresql':
        op.execute(
            "CREATE TRIGGER auditoria_imutavel BEFORE UPDATE OR DELETE "
            "ON auditoria FOR EACH ROW EXECUTE FUNCTION recusa_alteracao()"
        )
    elif _dialeto() == 'sqlite':
        for operacao in OPERACOES_RECUSADAS:
            op.execute(
                f"CREATE TRIGGER auditoria_sem_{operacao.lower()} BEFORE {operacao} ON auditoria "
                f"BEGIN SELECT RAISE(ABORT, 'auditoria não admite {operacao.lower()}'); END"
            )


def _remove_guardas():
    if _dialeto() == 'postgresql':
        op.execute("DROP TRIGGER IF EXISTS auditoria_imutavel ON auditoria")
    elif _dialeto() == 'sqlite':
        for operacao in OPERACOES_RECUSADAS:
            op.execute(f"DROP TRIGGER IF EXISTS auditoria_sem_{operacao.lower()}")


def upgrade():
    op.create_table('auditoria',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('autor_id', sa.Integer(), nullable=False),
    sa.Column('acao', sa.String(length=30), nullable=False),
    sa.Column('recurso', sa.String(length=30), nullable=False),
    sa.Column('recurso_id', sa.Integer(), nullable=True),
    sa.Column('assistido_id', sa.Integer(), nullable=True),
    sa.Column('detalhe', sa.String(length=200), nullable=True),
    sa.Column('ocorrido_em', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['assistido_id'], ['assistido.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['autor_id'], ['usuario.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('auditoria', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_auditoria_assistido_id'), ['assistido_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_auditoria_autor_id'), ['autor_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_auditoria_ocorrido_em'), ['ocorrido_em'], unique=False)
        batch_op.create_index(batch_op.f('ix_auditoria_recurso'), ['recurso'], unique=False)

    _cria_guardas()


def downgrade():
    _remove_guardas()

    with op.batch_alter_table('auditoria', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_auditoria_recurso'))
        batch_op.drop_index(batch_op.f('ix_auditoria_ocorrido_em'))
        batch_op.drop_index(batch_op.f('ix_auditoria_autor_id'))
        batch_op.drop_index(batch_op.f('ix_auditoria_assistido_id'))

    op.drop_table('auditoria')
