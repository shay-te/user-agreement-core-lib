from sqlalchemy import Column, INTEGER, VARCHAR, LargeBinary

from core_lib.data_layers.data.db.sqlalchemy.base import Base
from core_lib.data_layers.data.db.sqlalchemy.mixins.soft_delete_mixin import (
    SoftDeleteMixin,
)


class AgreementDocument(Base, SoftDeleteMixin):
    __tablename__ = 'agreement_document'

    id = Column(INTEGER, primary_key=True, nullable=False)
    file_text = Column(LargeBinary, nullable=False)
    file_path = Column(VARCHAR, nullable=False, default=None)
    version = Column(VARCHAR, nullable=False, default='')
