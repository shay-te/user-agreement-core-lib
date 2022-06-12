from datetime import datetime

from core_lib.connection.sql_alchemy_connection_registry import (
    SqlAlchemyConnectionRegistry,
)
from core_lib.data_layers.data_access.data_access import DataAccess
from core_lib.error_handling.not_found_decorator import NotFoundErrorHandler

from user_agreement_core_lib.data_layers.data.agreement_db.entities.agreement_list import (
    AgreementList,
)


class AgreementListDataAccess(DataAccess):
    def __init__(self, db: SqlAlchemyConnectionRegistry):
        self.db_session = db

    def add(self, name: str):
        with self.db_session.get() as session:
            entity = AgreementList()
            entity.name = name
            session.add(entity)
        return entity

    def delete(self, list_id: int):
        with self.db_session.get() as session:
            return (
                session.query(AgreementList)
                .filter(AgreementList.id == list_id)
                .update({AgreementList.deleted_at: datetime.utcnow()})
            )

    @NotFoundErrorHandler()
    def get_by_name(self, list_name: str):
        with self.db_session.get() as session:
            return session.query(AgreementList).filter(AgreementList.name == list_name).first()
