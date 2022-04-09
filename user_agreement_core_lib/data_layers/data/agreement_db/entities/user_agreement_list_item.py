from sqlalchemy import Column, ForeignKey, Index, Integer

from core_lib.data_layers.data.db.sqlalchemy.base import Base
from core_lib.data_layers.data.db.sqlalchemy.mixins.soft_delete_mixin import SoftDeleteMixin
from core_lib.data_layers.data.db.sqlalchemy.mixins.soft_delete_token_mixin import SoftDeleteTokenMixin


class UserAgreementListItem(Base, SoftDeleteMixin, SoftDeleteTokenMixin):
    __tablename__ = 'user_agreement_list_item'

    INDEX_USER_ITEM_ID = 'user_id_agreement_list_item_id'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    agreement_list_item_id = Column(Integer, ForeignKey('agreement_list_item.id'), nullable=False)

    __table_args__ = (Index(INDEX_USER_ITEM_ID, user_id, agreement_list_item_id, 'deleted_at_token', unique=True),)
