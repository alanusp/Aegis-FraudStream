# SPDX-License-Identifier: Apache-2.0
from alembic import op
import sqlalchemy as sa

revision = '20250916_0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'decision_logs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.String(120)),
        sa.Column('decision', sa.String(32)),
        sa.Column('reason', sa.String(255)),
        sa.Column('score', sa.Float),
        sa.Column('features', sa.JSON),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'))
    )

def downgrade():
    op.drop_table('decision_logs')
