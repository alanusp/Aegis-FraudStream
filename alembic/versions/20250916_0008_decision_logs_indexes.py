# SPDX-License-Identifier: Apache-2.0
from alembic import op
import sqlalchemy as sa

revision = '20250916_0008'
down_revision = '20250916_0007'
branch_labels = None
depends_on = None

def upgrade():
    try:
        op.create_index('ix_decision_logs_user_created', 'decision_logs', ['user_id','created_at'])
    except Exception:
        pass
    try:
        op.create_index('ix_decision_logs_created', 'decision_logs', ['created_at'])
    except Exception:
        pass
    try:
        op.create_index('ix_decision_logs_tenant_created', 'decision_logs', ['tenant','created_at'])
    except Exception:
        pass

def downgrade():
    for name in ['ix_decision_logs_tenant_created','ix_decision_logs_created','ix_decision_logs_user_created']:
        try:
            op.drop_index(name)
        except Exception:
            pass
