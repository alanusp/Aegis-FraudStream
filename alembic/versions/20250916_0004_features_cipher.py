# SPDX-License-Identifier: Apache-2.0
from alembic import op
import sqlalchemy as sa

revision = '20250916_0004'
down_revision = '20250916_0003'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('decision_logs', sa.Column('features_cipher', sa.Text(), nullable=True))

def downgrade():
    op.drop_column('decision_logs', 'features_cipher')
