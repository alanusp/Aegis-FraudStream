# SPDX-License-Identifier: Apache-2.0
from alembic import op
from sqlalchemy import text

revision = '20250916_0007'
down_revision = '20250916_0006'
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()
    try:
        # check tenant column
        res = conn.execute(text("""
            SELECT 1 FROM information_schema.columns
            WHERE table_name='decision_logs' AND column_name='tenant'
        """)).fetchone()
        if res:
            conn.execute(text("ALTER TABLE decision_logs ENABLE ROW LEVEL SECURITY"))
            conn.execute(text("CREATE POLICY IF NOT EXISTS tenant_isolation ON decision_logs USING (tenant = current_setting('app.tenant', true))"))
    except Exception:
        pass

def downgrade():
    conn = op.get_bind()
    try:
        conn.execute(text("DROP POLICY IF EXISTS tenant_isolation ON decision_logs"))
        conn.execute(text("ALTER TABLE decision_logs DISABLE ROW LEVEL SECURITY"))
    except Exception:
        pass
