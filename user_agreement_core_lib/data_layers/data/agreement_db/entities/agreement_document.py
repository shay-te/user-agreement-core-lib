from sqlalchemy import Column, VARCHAR, LargeBinary, TEXT, Index, Integer

from core_lib.data_layers.data.db.sqlalchemy.base import Base
from core_lib.data_layers.data.db.sqlalchemy.mixins.soft_delete_mixin import (
    SoftDeleteMixin,
)


class AgreementDocument(Base, SoftDeleteMixin):
    __tablename__ = 'agreement_document'

    INDEX_DOC_NAME_VERSION = 'name_version'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(VARCHAR(length=255), nullable=False)
    file = Column(LargeBinary, nullable=False)
    file_text = Column(TEXT, nullable=False)
    version = Column(VARCHAR(length=255), nullable=False)

    __table_args__ = (Index(INDEX_DOC_NAME_VERSION, name, version, unique=True),)
