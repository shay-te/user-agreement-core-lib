"""create_db

Revision ID: 1
Revises: 
Create Date: 2022-04-07 19:14:03.203923

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey

from user_agreement_core_lib.data_layers.data.agreement_db.entities.agreement_document import AgreementDocument
from user_agreement_core_lib.data_layers.data.agreement_db.entities.agreement_list import AgreementList
from user_agreement_core_lib.data_layers.data.agreement_db.entities.agreement_list_item import AgreementListItem
from user_agreement_core_lib.data_layers.data.agreement_db.entities.user_agreement_document import UserAgreementDocument
from user_agreement_core_lib.data_layers.data.agreement_db.entities.user_agreement_list_item import UserAgreementListItem

revision = '1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        AgreementDocument.__tablename__,
        sa.Column(AgreementDocument.id.key, sa.Integer, primary_key=True, nullable=False, autoincrement=True),
        sa.Column(AgreementDocument.name.key, sa.VARCHAR(255), nullable=False),
        sa.Column(AgreementDocument.file.key, sa.LargeBinary, nullable=False,),
        sa.Column(AgreementDocument.file_text.key, sa.TEXT, nullable=False),
        sa.Column(AgreementDocument.version.key, sa.VARCHAR(255), nullable=False),
        sa.Column(AgreementDocument.created_at.key, sa.DateTime, default=datetime.utcnow),
        sa.Column(
            AgreementDocument.updated_at.key, sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,
        ),
        sa.Column(AgreementDocument.deleted_at.key, sa.DateTime, default=None),
        sa.Index(
            AgreementDocument.INDEX_DOC_NAME_VERSION, AgreementDocument.name.key, AgreementDocument.version.key,
            unique=True,
        ),
    )

    op.create_table(
        AgreementList.__tablename__,
        sa.Column(AgreementList.id.key, sa.Integer, primary_key=True, nullable=False, autoincrement=True),
        sa.Column(AgreementList.name.key, sa.VARCHAR(255), nullable=False),
        sa.Column(AgreementList.created_at.key, sa.DateTime, default=datetime.utcnow),
        sa.Column(
            AgreementList.updated_at.key,
            sa.DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
        ),
        sa.Column(AgreementList.deleted_at.key, sa.DateTime, default=None),
        sa.Index(AgreementList.INDEX_LIST_NAME, AgreementList.name.key, unique=True),
    )

    op.create_table(
        AgreementListItem.__tablename__,
        sa.Column(AgreementListItem.id.key, sa.Integer, primary_key=True, nullable=False, autoincrement=True),
        sa.Column(AgreementListItem.agreement_list_id.key, sa.Integer, nullable=False),
        sa.Column(AgreementListItem.label.key, sa.VARCHAR(255), nullable=False),
        sa.Column(AgreementListItem.created_at.key, sa.DateTime, default=datetime.utcnow),
        sa.Column(
            AgreementListItem.updated_at.key,
            sa.DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
        ),
        sa.Column(AgreementListItem.deleted_at.key, sa.DateTime, default=None),
        sa.Index(
            AgreementListItem.INDEX_LABEL_LIST_ID,
            AgreementListItem.label.key,
            AgreementListItem.agreement_list_id.key,
            unique=True,
        ),
    )

    op.create_table(
        UserAgreementDocument.__tablename__,
        sa.Column(UserAgreementDocument.id.key, sa.Integer, primary_key=True, nullable=False, autoincrement=True),
        sa.Column(UserAgreementDocument.user_id.key, sa.Integer, nullable=False),
        sa.Column(
            UserAgreementDocument.agreement_document_id.key,
            sa.Integer,
            ForeignKey('agreement_document.id'),
            nullable=False,
        ),
        sa.Column(UserAgreementDocument.created_at.key, sa.DateTime, default=datetime.utcnow),
        sa.Column(
            UserAgreementDocument.updated_at.key,
            sa.DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
        ),
        sa.Column(UserAgreementDocument.deleted_at.key, sa.DateTime, default=None),
        sa.Column(UserAgreementDocument.deleted_at_token.key, sa.Integer, default=None),
        sa.Index(
            UserAgreementDocument.INDEX_USER_DOCUMENT_ID,
            UserAgreementDocument.user_id.key,
            UserAgreementDocument.agreement_document_id.key,
            UserAgreementDocument.deleted_at_token.key,
            unique=True,
        ),
    )

    op.create_table(
        UserAgreementListItem.__tablename__,
        sa.Column(UserAgreementListItem.id.key, sa.Integer, primary_key=True, nullable=False, autoincrement=True),
        sa.Column(UserAgreementListItem.user_id.key, sa.Integer, nullable=False),
        sa.Column(
            UserAgreementListItem.agreement_list_item_id.key,
            sa.Integer,
            sa.ForeignKey('agreement_list_item.id'),
            nullable=False,
        ),
        sa.Column(UserAgreementListItem.created_at.key, sa.DateTime, default=datetime.utcnow),
        sa.Column(
            UserAgreementListItem.updated_at.key,
            sa.DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
        ),
        sa.Column(UserAgreementListItem.deleted_at.key, sa.DateTime, default=None),
        sa.Column(UserAgreementListItem.deleted_at_token.key, sa.Integer, default=None),
        sa.Index(
            UserAgreementListItem.INDEX_USER_ITEM_ID,
            UserAgreementListItem.user_id.key,
            UserAgreementListItem.agreement_list_item_id.key,
            UserAgreementListItem.deleted_at_token.key,
            unique=True,
        ),
    )


def downgrade():
    op.drop_table(AgreementDocument.__tablename__)
    op.drop_table(AgreementList.__tablename__)
    op.drop_table(AgreementListItem.__tablename__)
    op.drop_table(UserAgreementDocument.__tablename__)
    op.drop_table(UserAgreementListItem.__tablename__)
