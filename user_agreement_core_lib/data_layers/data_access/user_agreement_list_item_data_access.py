from datetime import datetime

from core_lib.connection.sql_alchemy_connection_factory import SqlAlchemyConnectionFactory
from core_lib.data_layers.data_access.data_access import DataAccess
from core_lib.error_handling.not_found_decorator import NotFoundErrorHandler
from user_agreement_core_lib.data_layers.data.agreement_db.entities.agreement_list_item import AgreementListItem
from user_agreement_core_lib.data_layers.data.agreement_db.entities.user_agreement_list_item import (
    UserAgreementListItem,
)


class UserAgreementListItemDataAccess(DataAccess):
    def __init__(self, db: SqlAlchemyConnectionFactory):
        self.db_session = db

    def agree(self, user_id: int, item_id: int):
        with self.db_session.get() as session:
            entity = UserAgreementListItem()
            entity.user_id = user_id
            entity.agreement_list_item_id = item_id
            session.add(entity)
        return entity

    @NotFoundErrorHandler()
    def agreed_user_item(self, user_id: int, item_id: int):
        with self.db_session.get() as session:
            return (
                session.query(UserAgreementListItem)
                .filter(
                    UserAgreementListItem.user_id == user_id,
                    UserAgreementListItem.agreement_list_item_id == item_id,
                    UserAgreementListItem.deleted_at == None,
                )
                .all()
            )

    def user_agreed_list_items(self, user_id: int, list_id: int):
        with self.db_session.get() as session:
            return (
                session.query(UserAgreementListItem)
                .join(AgreementListItem)
                .filter(
                    UserAgreementListItem.user_id == user_id,
                    AgreementListItem.agreement_list_id == list_id,
                    UserAgreementListItem.deleted_at == None,
                )
                .all()
            )

    def delete(self, user_id: int, item_id: int):
        with self.db_session.get() as session:
            return (
                session.query(UserAgreementListItem)
                .filter(
                    UserAgreementListItem.agreement_list_item_id == item_id,
                    UserAgreementListItem.user_id == user_id,
                    UserAgreementListItem.deleted_at == None,
                )
                .update(
                    {
                        UserAgreementListItem.deleted_at: datetime.utcnow(),
                        UserAgreementListItem.deleted_at_token: int(datetime.utcnow().timestamp()),
                    }
                )
            )
