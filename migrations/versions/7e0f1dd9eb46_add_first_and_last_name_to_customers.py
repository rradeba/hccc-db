"""add first and last name to customers

Revision ID: 7e0f1dd9eb46
Revises: c4e2e529d379
Create Date: 2025-10-31 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e0f1dd9eb46'
down_revision = 'c4e2e529d379'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('customers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('last_name', sa.String(length=120), nullable=True))

    conn = op.get_bind()
    result = conn.execute(sa.text("SELECT id, name FROM customers"))
    rows = result.fetchall()
    for row in rows:
        mapping = row._mapping if hasattr(row, '_mapping') else None
        row_id = mapping['id'] if mapping else row[0]
        full_name = (mapping['name'] if mapping else row[1]) or ''
        full_name = full_name.strip()
        first = None
        last = None
        if full_name:
            parts = full_name.split(' ', 1)
            if parts:
                first = parts[0] or None
            if len(parts) > 1:
                last = parts[1] or None
        conn.execute(
            sa.text("UPDATE customers SET first_name = :first, last_name = :last WHERE id = :id"),
            {"first": first, "last": last, "id": row_id}
        )


def downgrade():
    with op.batch_alter_table('customers', schema=None) as batch_op:
        batch_op.drop_column('last_name')
        batch_op.drop_column('first_name')


