import os
import inspect

from omegaconf import DictConfig

from core_lib.alembic.alembic import Alembic
from core_lib.core_lib import CoreLib

# template_cache_handler_imports
from core_lib.connection.sql_alchemy_connection_registry import (
    SqlAlchemyConnectionRegistry,
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
from user_agreement_core_lib.data_layers.data_access.user_agreement_document_data_access import \
    UserAgreementDocumentDataAccess
from user_agreement_core_lib.data_layers.data_access.user_agreement_list_item_data_access import \
    UserAgreementListItemDataAccess
from user_agreement_core_lib.data_layers.service.agreement_document_service import AgreementDocumentService
from user_agreement_core_lib.data_layers.service.agreement_list_service import AgreementListService
from user_agreement_core_lib.data_layers.service.seed_service import SeedService


class UserAgreementCoreLib(CoreLib):

    def __init__(self, conf: DictConfig):
        super().__init__()
        self.config = conf

        agreement_db_session = SqlAlchemyConnectionRegistry(
            self.config.core_lib.data.sqlalchemy
        )
        agreement_document = AgreementDocumentDataAccess(agreement_db_session)
        agreement_list = AgreementListDataAccess(agreement_db_session)
        agreement_list_item = AgreementListItemDataAccess(agreement_db_session)
        user_agreement_document_da = UserAgreementDocumentDataAccess(agreement_db_session)
        user_agreement_list_item_da = UserAgreementListItemDataAccess(agreement_db_session)

        self.agreement_document = AgreementDocumentService(agreement_document, user_agreement_document_da)
        self.agreement_list = AgreementListService(user_agreement_list_item_da, agreement_list_item, agreement_list)
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

    @staticmethod
    def create(cfg: DictConfig, name: str):
        Alembic(os.path.dirname(inspect.getfile(UserAgreementCoreLib)), cfg).create_migration(name)

    @staticmethod
    def downgrade(cfg: DictConfig):
        Alembic(os.path.dirname(inspect.getfile(UserAgreementCoreLib)), cfg).downgrade("-1")
