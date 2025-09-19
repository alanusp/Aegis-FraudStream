# SPDX-License-Identifier: Apache-2.0
from alembic import op
import sqlalchemy as sa

revision = '20250916_0003'
down_revision = '20250916_0002'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'api_keys',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('key_prefix', sa.String(24), unique=True),
        sa.Column('key_hash', sa.String(128)),
        sa.Column('tenant', sa.String(120)),
        sa.Column('scopes', sa.String(255)),
        sa.Column('rate_limit_rpm_override', sa.Integer, nullable=True),
        sa.Column('active', sa.Boolean, server_default=sa.text('1')),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'))
    )
    op.create_index('ix_api_keys_prefix', 'api_keys', ['key_prefix'], unique=True)

def downgrade():
    op.drop_table('api_keys')
