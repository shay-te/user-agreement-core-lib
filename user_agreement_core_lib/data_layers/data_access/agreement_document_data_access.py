from core_lib.data_layers.data.handler.sql_alchemy_data_handler_registry import (
    SqlAlchemyDataHandlerRegistry,
)
from core_lib.data_layers.data_access.db.crud.crud import CRUD
from core_lib.data_layers.data_access.db.crud.crud_soft_data_access import (
    CRUDSoftDeleteDataAccess,
)
from core_lib.rule_validator.rule_validator import RuleValidator

from user_agreement_core_lib.data_layers.data.agreement_db.entities.agreement_document import (
    AgreementDocument,
)


class AgreementDocumentDataAccess(CRUDSoftDeleteDataAccess):
    def __init__(self, db: SqlAlchemyDataHandlerRegistry, rule_validator: RuleValidator = None):
        CRUD.__init__(self, AgreementDocument, db, rule_validator)
