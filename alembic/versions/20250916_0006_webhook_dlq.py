# SPDX-License-Identifier: Apache-2.0
from alembic import op
import sqlalchemy as sa

revision = '20250916_0006'
down_revision = '20250916_0005'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'webhook_failures',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('callback_url', sa.String(512)),
        sa.Column('body', sa.Text()),
        sa.Column('headers', sa.Text()),
        sa.Column('attempts', sa.Integer, server_default=sa.text('0')),
        sa.Column('last_error', sa.String(255), nullable=True),
        sa.Column('next_attempt_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'))
    )

def downgrade():
    op.drop_table('webhook_failures')
