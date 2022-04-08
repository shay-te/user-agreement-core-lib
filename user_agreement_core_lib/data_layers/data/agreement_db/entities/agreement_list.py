from sqlalchemy import Column, INTEGER, VARCHAR, Index

from core_lib.data_layers.data.db.sqlalchemy.base import Base
from core_lib.data_layers.data.db.sqlalchemy.mixins.soft_delete_mixin import (
    SoftDeleteMixin,
)


class AgreementList(Base, SoftDeleteMixin):
    __tablename__ = 'agreement_list'

    INDEX_LIST_NAME = 'name'

    id = Column(INTEGER, primary_key=True, nullable=False)
    name = Column(VARCHAR(255), nullable=False)

    __table_args__ = (Index(INDEX_LIST_NAME, name, unique=True),)
