# SPDX-License-Identifier: Apache-2.0
from alembic import op
import sqlalchemy as sa

revision = '20250916_0002'
down_revision = '20250916_0001'
branch_labels = None
depends_on = None

def upgrade():
    op.create_index('ix_decision_logs_created_at', 'decision_logs', ['created_at'])
    op.create_index('ix_decision_logs_user_id', 'decision_logs', ['user_id'])

def downgrade():
    op.drop_index('ix_decision_logs_user_id', table_name='decision_logs')
    op.drop_index('ix_decision_logs_created_at', table_name='decision_logs')
