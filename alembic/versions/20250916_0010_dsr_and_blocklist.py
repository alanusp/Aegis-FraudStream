# SPDX-License-Identifier: Apache-2.0
from alembic import op
import sqlalchemy as sa

revision = '20250916_0010'
down_revision = '20250916_0009'
branch_labels = None
depends_on = None

def upgrade():
    try:
        op.create_table(
            'dsr_requests',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('user_id', sa.String(length=200), nullable=False),
            sa.Column('action', sa.String(length=50), nullable=False),  # export, block
            sa.Column('status', sa.String(length=50), nullable=False, server_default='recorded'),
            sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False)
        )
    except Exception:
        pass
    try:
        op.create_table(
            'pii_blocklist',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('user_hash', sa.String(length=64), nullable=False, unique=True),
            sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False)
        )
    except Exception:
        pass
    try:
        op.create_index('ix_dsr_requests_user_created', 'dsr_requests', ['user_id','created_at'])
    except Exception:
        pass

def downgrade():
    try:
        op.drop_index('ix_dsr_requests_user_created', table_name='dsr_requests')
    except Exception:
        pass
    try:
        op.drop_table('pii_blocklist')
    except Exception:
        pass
    try:
        op.drop_table('dsr_requests')
    except Exception:
        pass
