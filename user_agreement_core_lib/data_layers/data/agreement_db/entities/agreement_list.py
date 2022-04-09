from sqlalchemy import Column, VARCHAR, Index, Integer

from core_lib.data_layers.data.db.sqlalchemy.base import Base
from core_lib.data_layers.data.db.sqlalchemy.mixins.soft_delete_mixin import (
    SoftDeleteMixin,
)


class AgreementList(Base, SoftDeleteMixin):
    __tablename__ = 'agreement_list'

    INDEX_LIST_NAME = 'name'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(VARCHAR(length=255), nullable=False)

    __table_args__ = (Index(INDEX_LIST_NAME, name, unique=True),)
