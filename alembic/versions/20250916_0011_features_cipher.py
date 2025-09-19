# SPDX-License-Identifier: Apache-2.0
from alembic import op
import sqlalchemy as sa

revision = '20250916_0011'
down_revision = '20250916_0010'
branch_labels = None
depends_on = None

def upgrade():
    try:
        op.add_column('decision_logs', sa.Column('features_cipher', sa.Text, nullable=True))
    except Exception:
        pass

def downgrade():
    try:
        op.drop_column('decision_logs', 'features_cipher')
    except Exception:
        pass
