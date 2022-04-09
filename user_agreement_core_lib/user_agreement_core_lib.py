import os
import inspect

from omegaconf import DictConfig

from core_lib.alembic.alembic import Alembic
from core_lib.core_lib import CoreLib

# template_cache_handler_imports
from core_lib.data_layers.data.handler.sql_alchemy_data_handler_registry import (
    SqlAlchemyDataHandlerRegistry,
)

# template_mongo_handler_imports
from user_agreement_core_lib.data_layers.data_access.agreement_document_data_access import (
    AgreementDocumentDataAccess,
)
from user_agreement_core_lib.data_layers.data_access.agreement_list_data_access import (
    AgreementListDataAccess,
)
from user_agreement_core_lib.data_layers.data_access.agreement_list_item_data_access import (
    AgreementListItemDataAccess,
)
from user_agreement_core_lib.data_layers.service.agreement_service import (
    AgreementService,
)
from user_agreement_core_lib.data_layers.service.seed_service import SeedService


class UserAgreementCoreLib(CoreLib):

    def __init__(self, conf: DictConfig):
        super().__init__()
        self.config = conf

        agreement_db_session = SqlAlchemyDataHandlerRegistry(
            self.config.core_lib.user_agreement_core_lib.data.agreement_db
        )
        agreement_document = AgreementDocumentDataAccess(agreement_db_session)
        agreement_list = AgreementListDataAccess(agreement_db_session)
        agreement_list_item = AgreementListItemDataAccess(agreement_db_session)
        self.agreement = AgreementService(agreement_db_session, agreement_list_item)
        self.seed = SeedService(
            agreement_document,
            agreement_list,
            agreement_list_item,
        )

    @staticmethod
    def install(cfg: DictConfig):
        Alembic(os.path.dirname(inspect.getfile(UserAgreementCoreLib)), cfg).upgrade()

    @staticmethod
    def uninstall(cfg: DictConfig):
        Alembic(os.path.dirname(inspect.getfile(UserAgreementCoreLib)), cfg).downgrade()
