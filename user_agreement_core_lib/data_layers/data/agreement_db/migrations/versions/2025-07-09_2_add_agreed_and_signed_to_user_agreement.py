"""add_agreed_and_signed_to_user_agreement

Revision ID: 2
Revises: 1
Create Date: 2025-07-09 09:36:38.130977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2'
down_revision = '1'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('user_agreement_document', sa.Column('is_agreed', sa.Boolean(), nullable=False, server_default=sa.sql.expression.false()))
    op.add_column('user_agreement_document', sa.Column('signed_at', sa.DateTime(), nullable=True))
    connection = op.get_bind()
    connection.execute(
        sa.text("UPDATE user_agreement_document SET signed_at = created_at WHERE signed_at IS NULL")
    )

def downgrade():
    op.drop_column('user_agreement_document', 'signed_at')
    op.drop_column('user_agreement_document', 'is_agreed')