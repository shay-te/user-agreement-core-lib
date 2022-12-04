from sqlalchemy import desc

from core_lib.connection.sql_alchemy_connection_registry import (
    SqlAlchemyConnectionRegistry,
)
from core_lib.data_layers.data_access.db.crud.crud import CRUD
from core_lib.data_layers.data_access.db.crud.crud_soft_data_access import (
    CRUDSoftDeleteDataAccess,
)
from core_lib.error_handling.not_found_decorator import NotFoundErrorHandler
from core_lib.rule_validator.rule_validator import RuleValidator

from user_agreement_core_lib.data_layers.data.agreement_db.entities.agreement_document import (
    AgreementDocument,
)


class AgreementDocumentDataAccess(CRUDSoftDeleteDataAccess):
    def __init__(self, db: SqlAlchemyConnectionRegistry, rule_validator: RuleValidator = None):
        CRUD.__init__(self, AgreementDocument, db, rule_validator)

    @NotFoundErrorHandler()
    def get_latest_version(self, document_name: str, language: str):
        with self._db.get() as session:
            return session.query(AgreementDocument) \
                          .filter(AgreementDocument.name == document_name, AgreementDocument.language == language) \
                          .order_by(desc(AgreementDocument.version)) \
                          .first()
