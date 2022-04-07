from sqlalchemy import Column, INTEGER, ForeignKey

from core_lib.data_layers.data.db.sqlalchemy.base import Base
from core_lib.data_layers.data.db.sqlalchemy.mixins.soft_delete_mixin import (
    SoftDeleteMixin,
)


class UserAgreementListItem(Base, SoftDeleteMixin):
    __tablename__ = 'user_agreement_list_item'

    id = Column(INTEGER, primary_key=True, nullable=False)
    user_id = Column(INTEGER, nullable=False, default=None)
    agreement_list_item_id = Column(INTEGER, ForeignKey('agreement_list_item.id'), nullable=False, default=None)
