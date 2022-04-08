from sqlalchemy import Column, INTEGER, ForeignKey, Index

from core_lib.data_layers.data.db.sqlalchemy.base import Base
from core_lib.data_layers.data.db.sqlalchemy.mixins.soft_delete_mixin import (
    SoftDeleteMixin,
)


class UserAgreementListItem(Base, SoftDeleteMixin):
    __tablename__ = 'user_agreement_list_item'

    INDEX_USER_ITEM_ID = 'user_id_agreement_list_item_id'

    id = Column(INTEGER, primary_key=True, nullable=False)
    user_id = Column(INTEGER, nullable=False, default=None)
    agreement_list_item_id = Column(INTEGER, ForeignKey('agreement_list_item.id'), nullable=False, default=None)

    __table_args__ = (Index(INDEX_USER_ITEM_ID, user_id, agreement_list_item_id, unique=True),)
