from sqlalchemy import Column, INTEGER, VARCHAR

from core_lib.data_layers.data.db.sqlalchemy.base import Base
from core_lib.data_layers.data.db.sqlalchemy.mixins.soft_delete_mixin import (
    SoftDeleteMixin,
)


class AgreementList(Base, SoftDeleteMixin):
    __tablename__ = 'agreement_list'

    id = Column(INTEGER, primary_key=True, nullable=False)
    name = Column(VARCHAR, nullable=False, default=None, unique=True)
