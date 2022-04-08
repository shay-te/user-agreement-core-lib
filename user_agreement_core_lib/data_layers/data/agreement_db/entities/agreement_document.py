from sqlalchemy import Column, INTEGER, VARCHAR, LargeBinary, TEXT, Index

from core_lib.data_layers.data.db.sqlalchemy.base import Base
from core_lib.data_layers.data.db.sqlalchemy.mixins.soft_delete_mixin import (
    SoftDeleteMixin,
)


class AgreementDocument(Base, SoftDeleteMixin):
    __tablename__ = 'agreement_document'

    INDEX_DOC_NAME_VERSION = 'name_version'

    id = Column(INTEGER, primary_key=True, nullable=False)
    name = Column(VARCHAR, nullable=False, default=None)
    file = Column(LargeBinary, nullable=False)
    file_text = Column(TEXT, nullable=False, default=None)
    version = Column(VARCHAR, nullable=False, default=None)

    __table_args__ = (Index(INDEX_DOC_NAME_VERSION, name, version, unique=True),)
