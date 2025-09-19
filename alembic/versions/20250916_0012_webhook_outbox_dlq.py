# SPDX-License-Identifier: Apache-2.0
from alembic import op
import sqlalchemy as sa

revision = '20250916_0012'
down_revision = '20250916_0011'
branch_labels = None
depends_on = None

def upgrade():
    try:
        op.create_table(
            'webhook_outbox',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('callback_url', sa.Text, nullable=False),
            sa.Column('body', sa.Text, nullable=False),
            sa.Column('headers', sa.Text, nullable=True),
            sa.Column('attempts', sa.Integer, server_default='0', nullable=False),
            sa.Column('next_attempt_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
            sa.Column('status', sa.String(length=20), server_default='pending', nullable=False),
            sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False)
        )
    except Exception:
        pass
    try:
        op.create_table(
            'webhook_dlq',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('callback_url', sa.Text, nullable=False),
            sa.Column('body', sa.Text, nullable=False),
            sa.Column('headers', sa.Text, nullable=True),
            sa.Column('last_error', sa.Text, nullable=True),
            sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False)
        )
    except Exception:
        pass

def downgrade():
    try:
        op.drop_table('webhook_dlq')
    except Exception:
        pass
    try:
        op.drop_table('webhook_outbox')
    except Exception:
        pass
