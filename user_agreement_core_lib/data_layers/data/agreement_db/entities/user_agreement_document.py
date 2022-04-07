from sqlalchemy import Column, INTEGER

from core_lib.data_layers.data.db.sqlalchemy.base import Base
from core_lib.data_layers.data.db.sqlalchemy.mixins.soft_delete_mixin import (
    SoftDeleteMixin,
)


class UserAgreementDocument(Base, SoftDeleteMixin):
    __tablename__ = 'user_agreement_document'

    id = Column(INTEGER, primary_key=True, nullable=False)
    user_id = Column(INTEGER, nullable=False, default=None)
    agreement_document_id = Column(INTEGER, nullable=False, default=None)
