from sqlalchemy import Column, INTEGER, VARCHAR

from core_lib.data_layers.data.db.sqlalchemy.base import Base
from core_lib.data_layers.data.db.sqlalchemy.mixins.soft_delete_mixin import SoftDeleteMixin


class AgreementListItem(Base, SoftDeleteMixin):
    __tablename__ = 'agreement_list_item'

    id = Column(INTEGER, primary_key=True, nullable=False)
    agreement_list_id = Column(INTEGER, nullable=False, default=None)
    label = Column(VARCHAR, nullable=False, default=None)
