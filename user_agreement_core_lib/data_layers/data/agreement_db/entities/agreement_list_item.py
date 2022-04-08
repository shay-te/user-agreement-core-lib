from sqlalchemy import Column, INTEGER, VARCHAR, ForeignKey, Index

from core_lib.data_layers.data.db.sqlalchemy.base import Base
from core_lib.data_layers.data.db.sqlalchemy.mixins.soft_delete_mixin import (
    SoftDeleteMixin,
)


class AgreementListItem(Base, SoftDeleteMixin):
    __tablename__ = 'agreement_list_item'

    INDEX_LABEL_LIST_ID = 'label_list_id'

    id = Column(INTEGER, primary_key=True, nullable=False)
    agreement_list_id = Column(INTEGER, ForeignKey('agreement_list.id'), nullable=False, default=None)
    label = Column(VARCHAR, nullable=False, default=None)

    __table_args__ = (Index(INDEX_LABEL_LIST_ID, agreement_list_id, label, unique=True),)
