# SPDX-License-Identifier: Apache-2.0
from alembic import op
import sqlalchemy as sa

revision = '20250916_0009'
down_revision = '20250916_0008'
branch_labels = None
depends_on = None

def upgrade():
    try:
        op.add_column('decision_logs', sa.Column('chain_hash', sa.String(length=128), nullable=True))
    except Exception:
        pass
    try:
        op.create_table(
            'audit_chain_meta',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('last_hash', sa.String(length=128), nullable=True),
            sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), nullable=False)
        )
    except Exception:
        pass
    try:
        op.create_table(
            'policy_history',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('tenant', sa.String(length=100), nullable=False),
            sa.Column('policy_checksum', sa.String(length=64), nullable=False),
            sa.Column('policy_body', sa.Text, nullable=False),
            sa.Column('actor', sa.String(length=200), nullable=True),
            sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False)
        )
        op.create_index('ix_policy_history_tenant_created', 'policy_history', ['tenant','created_at'])
    except Exception:
        pass

def downgrade():
    try:
        op.drop_index('ix_policy_history_tenant_created', table_name='policy_history')
    except Exception:
        pass
    try:
        op.drop_table('policy_history')
    except Exception:
        pass
    try:
        op.drop_table('audit_chain_meta')
    except Exception:
        pass
    try:
        op.drop_column('decision_logs', 'chain_hash')
    except Exception:
        pass
