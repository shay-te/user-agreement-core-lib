from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, Index

from core_lib.data_layers.data.db.sqlalchemy.base import Base
from core_lib.data_layers.data.db.sqlalchemy.mixins.soft_delete_mixin import (
    SoftDeleteMixin,
)


class AgreementListItem(Base, SoftDeleteMixin):
    __tablename__ = 'agreement_list_item'

    INDEX_LABEL_LIST_ID = 'label_list_id'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    agreement_list_id = Column(Integer, ForeignKey('agreement_list.id'), nullable=False)
    label = Column(VARCHAR(length=255), nullable=False)

    __table_args__ = (Index(INDEX_LABEL_LIST_ID, agreement_list_id, label, unique=True),)
