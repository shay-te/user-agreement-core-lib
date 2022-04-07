from datetime import datetime

from core_lib.data_layers.data.handler.sql_alchemy_data_handler_registry import (
    SqlAlchemyDataHandlerRegistry,
)
from core_lib.data_layers.data_access.data_access import DataAccess

from user_agreement_core_lib.data_layers.data.agreement_db.entities.agreement_list import (
    AgreementList,
)


class AgreementListDataAccess(DataAccess):
    def __init__(self, db: SqlAlchemyDataHandlerRegistry):
        self.db_session = db
        self.entity = AgreementList

    def add(self, name: str):
        with self.db_session.get() as session:
            entity = self.entity()
            entity.name = name
            session.add(entity)
        return entity

    def delete(self, list_id: int):
        with self.db_session.get() as session:
            return (
                session.query(self.entity)
                .filter(self.entity.id == list_id)
                .update({self.entity.deleted_at: datetime.utcnow()})
            )
