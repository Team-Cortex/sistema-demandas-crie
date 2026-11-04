"""cria o modelo de domínio

Tabelas dos cards #49 a #55 e as guardas de imutabilidade (RNF19)
também no banco, para quem escrever SQL direto:

- historico_demanda e evolucao: só INSERT (UPDATE e DELETE recusados);
- demanda e encaminhamento: DELETE recusado.

Revision ID: b0f13416410c
Revises:
Create Date: 2026-11-04 10:08:51.026449

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'b0f13416410c'
down_revision = None
branch_labels = None
depends_on = None


ENUMS = {
    'setor': ('pedagogico', 'saude', 'convivencia'),
    'prioridade': ('baixa', 'media', 'alta'),
    'estado_demanda': ('aberta', 'em_andamento', 'aguardando_terceiros', 'concluida', 'cancelada'),
    'tipo_historico': ('estado', 'anotacao'),
}

# tabela -> operações recusadas
IMUTAVEIS = {
    'historico_demanda': ('UPDATE', 'DELETE'),
    'evolucao': ('UPDATE', 'DELETE'),
    'demanda': ('DELETE',),
    'encaminhamento': ('DELETE',),
}


def _enum(nome):
    """CHECK no SQLite; no PostgreSQL, tipo nativo criado uma vez só em upgrade()."""
    valores = ENUMS[nome]
    return sa.Enum(*valores, name=nome, create_constraint=True).with_variant(
        postgresql.ENUM(*valores, name=nome, create_type=False), 'postgresql'
    )


def _dialeto():
    return op.get_context().dialect.name


def _cria_guardas():
    if _dialeto() == 'postgresql':
        op.execute(
            """
            CREATE FUNCTION recusa_alteracao() RETURNS trigger
            LANGUAGE plpgsql AS $$
            BEGIN
                RAISE EXCEPTION '% não admite %', TG_TABLE_NAME, lower(TG_OP)
                    USING ERRCODE = 'restrict_violation';
            END;
            $$
            """
        )
        for tabela, operacoes in IMUTAVEIS.items():
            op.execute(
                f"CREATE TRIGGER {tabela}_imutavel BEFORE {' OR '.join(operacoes)} "
                f"ON {tabela} FOR EACH ROW EXECUTE FUNCTION recusa_alteracao()"
            )
    elif _dialeto() == 'sqlite':
        for tabela, operacoes in IMUTAVEIS.items():
            for operacao in operacoes:
                op.execute(
                    f"CREATE TRIGGER {tabela}_sem_{operacao.lower()} BEFORE {operacao} ON {tabela} "
                    f"BEGIN SELECT RAISE(ABORT, '{tabela} não admite {operacao.lower()}'); END"
                )


def _remove_guardas():
    if _dialeto() == 'postgresql':
        for tabela in IMUTAVEIS:
            op.execute(f"DROP TRIGGER IF EXISTS {tabela}_imutavel ON {tabela}")
        op.execute("DROP FUNCTION IF EXISTS recusa_alteracao()")
    elif _dialeto() == 'sqlite':
        for tabela, operacoes in IMUTAVEIS.items():
            for operacao in operacoes:
                op.execute(f"DROP TRIGGER IF EXISTS {tabela}_sem_{operacao.lower()}")


def upgrade():
    if _dialeto() == 'postgresql':
        bind = op.get_bind()
        for nome, valores in ENUMS.items():
            postgresql.ENUM(*valores, name=nome).create(bind, checkfirst=False)

    op.create_table('assistido',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome_tratamento', sa.String(length=120), nullable=False),
    sa.Column('ativo', sa.Boolean(), nullable=False),
    sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reuniao',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', sa.Date(), nullable=False),
    sa.Column('setor', _enum('setor'), nullable=False),
    sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('reuniao', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_reuniao_data'), ['data'], unique=False)

    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=120), nullable=False),
    sa.Column('email', sa.String(length=254), nullable=False),
    sa.Column('ativo', sa.Boolean(), nullable=False),
    sa.Column('perfil', sa.String(length=30), nullable=False),
    sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
    sa.Column('senha_hash', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_usuario_email'), ['email'], unique=True)

    op.create_table('assistido_profissional',
    sa.Column('assistido_id', sa.Integer(), nullable=False),
    sa.Column('profissional_id', sa.Integer(), nullable=False),
    sa.Column('data_inicio', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['assistido_id'], ['assistido.id'], ),
    sa.ForeignKeyConstraint(['profissional_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('assistido_id', 'profissional_id')
    )
    op.create_table('demanda',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('descricao', sa.Text(), nullable=False),
    sa.Column('categoria', sa.String(length=80), nullable=True),
    sa.Column('prioridade', _enum('prioridade'), nullable=False),
    sa.Column('prazo', sa.Date(), nullable=False),
    sa.Column('estado', _enum('estado_demanda'), nullable=False),
    sa.Column('responsavel_id', sa.Integer(), nullable=False),
    sa.Column('reuniao_id', sa.Integer(), nullable=False),
    sa.Column('assistido_id', sa.Integer(), nullable=True),
    sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['assistido_id'], ['assistido.id'], ),
    sa.ForeignKeyConstraint(['responsavel_id'], ['usuario.id'], ),
    sa.ForeignKeyConstraint(['reuniao_id'], ['reuniao.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('demanda', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_demanda_assistido_id'), ['assistido_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_demanda_estado'), ['estado'], unique=False)
        batch_op.create_index(batch_op.f('ix_demanda_prazo'), ['prazo'], unique=False)
        batch_op.create_index(batch_op.f('ix_demanda_responsavel_id'), ['responsavel_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_demanda_reuniao_id'), ['reuniao_id'], unique=False)

    op.create_table('evolucao',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('assistido_id', sa.Integer(), nullable=False),
    sa.Column('profissional_id', sa.Integer(), nullable=False),
    sa.Column('data', sa.Date(), nullable=False),
    sa.Column('area_atuacao', sa.String(length=80), nullable=False),
    sa.Column('descricao', sa.Text(), nullable=False),
    sa.Column('autor_id', sa.Integer(), nullable=False),
    sa.Column('ocorrido_em', sa.DateTime(timezone=True), nullable=False),
    sa.Column('retifica_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['assistido_id'], ['assistido.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['autor_id'], ['usuario.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['profissional_id'], ['usuario.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['retifica_id'], ['evolucao.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('retifica_id')
    )
    with op.batch_alter_table('evolucao', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_evolucao_area_atuacao'), ['area_atuacao'], unique=False)
        batch_op.create_index(batch_op.f('ix_evolucao_assistido_id'), ['assistido_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_evolucao_data'), ['data'], unique=False)
        batch_op.create_index(batch_op.f('ix_evolucao_profissional_id'), ['profissional_id'], unique=False)

    op.create_table('reuniao_participante',
    sa.Column('reuniao_id', sa.Integer(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['reuniao_id'], ['reuniao.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('reuniao_id', 'usuario_id')
    )
    op.create_table('encaminhamento',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('destino', sa.String(length=200), nullable=False),
    sa.Column('data', sa.Date(), nullable=False),
    sa.Column('responsavel_id', sa.Integer(), nullable=False),
    sa.Column('observacao', sa.Text(), nullable=True),
    sa.Column('criado_em', sa.DateTime(timezone=True), nullable=False),
    sa.Column('assistido_id', sa.Integer(), nullable=True),
    sa.Column('demanda_id', sa.Integer(), nullable=True),
    sa.Column('desfecho', sa.Text(), nullable=True),
    sa.Column('desfecho_autor_id', sa.Integer(), nullable=True),
    sa.Column('desfecho_em', sa.DateTime(timezone=True), nullable=True),
    sa.CheckConstraint('(desfecho IS NULL AND desfecho_autor_id IS NULL AND desfecho_em IS NULL) OR (desfecho IS NOT NULL AND desfecho_autor_id IS NOT NULL AND desfecho_em IS NOT NULL)', name='ck_encaminhamento_desfecho_completo'),
    sa.CheckConstraint('assistido_id IS NOT NULL OR demanda_id IS NOT NULL', name='ck_encaminhamento_tem_vinculo'),
    sa.ForeignKeyConstraint(['assistido_id'], ['assistido.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['demanda_id'], ['demanda.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['desfecho_autor_id'], ['usuario.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['responsavel_id'], ['usuario.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('encaminhamento', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_encaminhamento_assistido_id'), ['assistido_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_encaminhamento_data'), ['data'], unique=False)
        batch_op.create_index(batch_op.f('ix_encaminhamento_demanda_id'), ['demanda_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_encaminhamento_responsavel_id'), ['responsavel_id'], unique=False)

    op.create_table('historico_demanda',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('demanda_id', sa.Integer(), nullable=False),
    sa.Column('autor_id', sa.Integer(), nullable=False),
    sa.Column('tipo', _enum('tipo_historico'), nullable=False),
    sa.Column('estado_anterior', _enum('estado_demanda'), nullable=True),
    sa.Column('estado_novo', _enum('estado_demanda'), nullable=True),
    sa.Column('texto', sa.Text(), nullable=False),
    sa.Column('ocorrido_em', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['autor_id'], ['usuario.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['demanda_id'], ['demanda.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('historico_demanda', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_historico_demanda_demanda_id'), ['demanda_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_historico_demanda_ocorrido_em'), ['ocorrido_em'], unique=False)

    _cria_guardas()


def downgrade():
    _remove_guardas()

    with op.batch_alter_table('historico_demanda', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_historico_demanda_ocorrido_em'))
        batch_op.drop_index(batch_op.f('ix_historico_demanda_demanda_id'))

    op.drop_table('historico_demanda')
    with op.batch_alter_table('encaminhamento', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_encaminhamento_responsavel_id'))
        batch_op.drop_index(batch_op.f('ix_encaminhamento_demanda_id'))
        batch_op.drop_index(batch_op.f('ix_encaminhamento_data'))
        batch_op.drop_index(batch_op.f('ix_encaminhamento_assistido_id'))

    op.drop_table('encaminhamento')
    op.drop_table('reuniao_participante')
    with op.batch_alter_table('evolucao', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_evolucao_profissional_id'))
        batch_op.drop_index(batch_op.f('ix_evolucao_data'))
        batch_op.drop_index(batch_op.f('ix_evolucao_assistido_id'))
        batch_op.drop_index(batch_op.f('ix_evolucao_area_atuacao'))

    op.drop_table('evolucao')
    with op.batch_alter_table('demanda', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_demanda_reuniao_id'))
        batch_op.drop_index(batch_op.f('ix_demanda_responsavel_id'))
        batch_op.drop_index(batch_op.f('ix_demanda_prazo'))
        batch_op.drop_index(batch_op.f('ix_demanda_estado'))
        batch_op.drop_index(batch_op.f('ix_demanda_assistido_id'))

    op.drop_table('demanda')
    op.drop_table('assistido_profissional')
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_usuario_email'))

    op.drop_table('usuario')
    with op.batch_alter_table('reuniao', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_reuniao_data'))

    op.drop_table('reuniao')
    op.drop_table('assistido')

    if _dialeto() == 'postgresql':
        bind = op.get_bind()
        for nome in reversed(list(ENUMS)):
            postgresql.ENUM(name=nome).drop(bind, checkfirst=False)
