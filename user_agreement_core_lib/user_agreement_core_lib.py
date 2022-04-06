from omegaconf import DictConfig
from core_lib.core_lib import CoreLib

# template_cache_handler_imports
from core_lib.data_layers.data.handler.sql_alchemy_data_handler_registry import SqlAlchemyDataHandlerRegistry
# template_mongo_handler_imports
from user_agreement_core_lib.data_layers.data_access.agreement_document_data_access import AgreementDocumentDataAccess
from user_agreement_core_lib.data_layers.data_access.agreement_list_data_access import AgreementListDataAccess
from user_agreement_core_lib.data_layers.data_access.agreement_list_item_data_access import AgreementListItemDataAccess
from user_agreement_core_lib.data_layers.data_access.user_agreement_document_data_access import UserAgreementDocumentDataAccess
from user_agreement_core_lib.data_layers.data_access.user_agreement_list_item_data_access import UserAgreementListItemDataAccess


class UserAgreementCoreLib(CoreLib):
    def __init__(self, conf: DictConfig):
        super().__init__()
        self.config = conf

        agreement_db_session = SqlAlchemyDataHandlerRegistry(self.config.core_lib.user_agreement_core_lib.data.agreement_db)
        self.agreement_document = AgreementDocumentDataAccess(agreement_db_session)
        self.agreement_list = AgreementListDataAccess()
        self.agreement_list_item = AgreementListItemDataAccess()
        self.user_agreement_document = UserAgreementDocumentDataAccess()
        self.user_agreement_list_item = UserAgreementListItemDataAccess()
