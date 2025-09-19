# SPDX-License-Identifier: Apache-2.0
from alembic import op
import sqlalchemy as sa

revision = '20250916_0005'
down_revision = '20250916_0004'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('api_keys') as b:
        b.add_column(sa.Column('monthly_quota', sa.Integer, nullable=True))
    op.create_index('ix_decision_logs_user_time', 'decision_logs', ['user_id','created_at'])
    op.create_index('ix_decision_logs_created_at', 'decision_logs', ['created_at'])

def downgrade():
    with op.batch_alter_table('api_keys') as b:
        b.drop_column('monthly_quota')
    op.drop_index('ix_decision_logs_user_time')
    op.drop_index('ix_decision_logs_created_at')
