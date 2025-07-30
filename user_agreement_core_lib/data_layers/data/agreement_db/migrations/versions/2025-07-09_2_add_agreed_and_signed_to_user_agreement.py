"""add_agreed_and_signed_to_user_agreement

Revision ID: 2
Revises: 1
Create Date: 2025-07-09 09:36:38.130977

"""
from alembic import op
import sqlalchemy as sa

from user_agreement_core_lib.data_layers.data.agreement_db.entities.user_agreement_document import UserAgreementDocument

# revision identifiers, used by Alembic.
revision = '2'
down_revision = '1'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column(UserAgreementDocument.__tablename__, sa.Column(UserAgreementDocument.is_agreed.key, sa.Boolean(), nullable=False, server_default=sa.sql.expression.false()))
    op.add_column(UserAgreementDocument.__tablename__, sa.Column(UserAgreementDocument.signed_at.key, sa.DateTime(), nullable=True))
    connection = op.get_bind()
    connection.execute(
        sa.text("UPDATE user_agreement_document SET signed_at = created_at WHERE signed_at IS NULL")
    )

def downgrade():
    op.drop_column(UserAgreementDocument.__tablename__, UserAgreementDocument.signed_at.key)
    op.drop_column(UserAgreementDocument.__tablename__, UserAgreementDocument.is_agreed.key)