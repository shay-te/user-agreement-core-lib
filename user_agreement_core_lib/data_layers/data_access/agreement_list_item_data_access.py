from datetime import datetime

from core_lib.data_layers.data.handler.sql_alchemy_data_handler_registry import (
    SqlAlchemyDataHandlerRegistry,
)
from core_lib.data_layers.data_access.data_access import DataAccess
from core_lib.error_handling.not_found_decorator import NotFoundErrorHandler

from user_agreement_core_lib.data_layers.data.agreement_db.entities.agreement_list_item import (
    AgreementListItem,
)


class AgreementListItemDataAccess(DataAccess):
    def __init__(self, db: SqlAlchemyDataHandlerRegistry):
        self.db_session = db

    def add(self, list_id: int, label: str):
        with self.db_session.get() as session:
            entity = AgreementListItem()
            entity.agreement_list_id = list_id
            entity.label = label
            session.add(entity)
        return entity

    @NotFoundErrorHandler()
    def get_item(self, item_id: int):
        with self.db_session.get() as session:
            return session.query(AgreementListItem).filter(AgreementListItem.id == item_id).all()

    def get_list_items(self, list_id: int):
        with self.db_session.get() as session:
            return session.query(AgreementListItem).filter(AgreementListItem.agreement_list_id == list_id).all()

    def delete(self, item_id: int):
        with self.db_session.get() as session:
            return (
                session.query(AgreementListItem)
                .filter(AgreementListItem.id == item_id)
                .update({AgreementListItem.deleted_at: datetime.utcnow()})
            )
