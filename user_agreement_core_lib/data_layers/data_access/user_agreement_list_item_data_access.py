from datetime import datetime

from core_lib.data_layers.data.handler.sql_alchemy_data_handler_registry import (
    SqlAlchemyDataHandlerRegistry,
)
from core_lib.data_layers.data_access.data_access import DataAccess
from core_lib.error_handling.not_found_decorator import NotFoundErrorHandler
from user_agreement_core_lib.data_layers.data.agreement_db.entities.agreement_list_item import (
    AgreementListItem,
)

from user_agreement_core_lib.data_layers.data.agreement_db.entities.user_agreement_list_item import (
    UserAgreementListItem,
)


class UserAgreementListItemDataAccess(DataAccess):
    def __init__(self, db: SqlAlchemyDataHandlerRegistry):
        self.db_session = db
        self.entity = UserAgreementListItem
        self.agreement_list_item_entity = AgreementListItem

    def agree(self, user_id: int, item_id: int):
        with self.db_session.get() as session:
            entity = self.entity()
            entity.user_id = user_id
            entity.agreement_list_item_id = item_id
            session.add(entity)
        return entity

    @NotFoundErrorHandler()
    def agreed_user_item(self, user_id: int, item_id: int):
        with self.db_session.get() as session:
            return (
                session.query(self.entity)
                .filter(self.entity.user_id == user_id)
                .filter(self.entity.agreement_list_item_id == item_id)
                .filter(self.entity.deleted_at == None)
                .all()
            )

    def agreed_list_items(self, user_id: int, list_id: int):
        with self.db_session.get() as session:
            return (
                session.query(self.entity)
                .join(self.agreement_list_item_entity)
                .filter(self.entity.user_id == user_id)
                .filter(self.agreement_list_item_entity.agreement_list_id == list_id)
                .filter(self.entity.deleted_at == None)
                .all()
            )

    def delete(self, user_id: int, item_id: int):
        with self.db_session.get() as session:
            return (
                session.query(self.entity)
                .filter(self.entity.id == item_id)
                .filter(self.entity.user_id == user_id)
                .update({self.entity.deleted_at: datetime.utcnow()})
            )
