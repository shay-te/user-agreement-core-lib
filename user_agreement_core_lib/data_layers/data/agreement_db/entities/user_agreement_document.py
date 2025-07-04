from sqlalchemy import Column, Integer, Index, ForeignKey, BOOLEAN, DateTime

from core_lib.data_layers.data.db.sqlalchemy.base import Base
from core_lib.data_layers.data.db.sqlalchemy.mixins.soft_delete_mixin import (
    SoftDeleteMixin,
)
from core_lib.data_layers.data.db.sqlalchemy.mixins.soft_delete_token_mixin import SoftDeleteTokenMixin


class UserAgreementDocument(Base, SoftDeleteMixin, SoftDeleteTokenMixin):
    __tablename__ = 'user_agreement_document'

    INDEX_USER_DOCUMENT_ID = 'user_id_agreement_document_id'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # TODO: ask shay if to make column foreignKey
    #   if yes: there is user_id that not exists in admin_user - what is that means?
    # user_id = Column(Integer, ForeignKey('admin_user.id'), nullable=False)
    user_id = Column(Integer, nullable=False)
    agreement_document_id = Column(Integer, ForeignKey('agreement_document.id'), nullable=False)
    is_agreed = Column(BOOLEAN(), nullable=False, default=False)
    signed_at = Column(DateTime)

    __table_args__ = (Index(INDEX_USER_DOCUMENT_ID, user_id, agreement_document_id, 'deleted_at_token', unique=True),)

