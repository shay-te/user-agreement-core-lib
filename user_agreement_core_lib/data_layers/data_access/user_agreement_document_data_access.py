from datetime import datetime

from core_lib.data_layers.data.handler.sql_alchemy_data_handler_registry import (
    SqlAlchemyDataHandlerRegistry,
)
from core_lib.data_layers.data_access.data_access import DataAccess

from user_agreement_core_lib.data_layers.data.agreement_db.entities.user_agreement_document import (
    UserAgreementDocument,
)


class UserAgreementDocumentDataAccess(DataAccess):
    def __init__(self, db: SqlAlchemyDataHandlerRegistry):
        self.db_session = db

    def agree(self, user_id: int, document_id: int):
        with self.db_session.get() as session:
            entity = UserAgreementDocument()
            entity.user_id = user_id
            entity.agreement_document_id = document_id
            session.add(entity)
        return entity

    def user_agreed_document(self, user_id: int, doc_id: int):
        with self.db_session.get() as session:
            return (
                session.query(UserAgreementDocument)
                .filter(UserAgreementDocument.user_id == user_id, UserAgreementDocument.agreement_document_id == doc_id)
                .all()
            )

    def delete(self, list_id: int):
        with self.db_session.get() as session:
            return (
                session.query(UserAgreementDocument)
                .filter(UserAgreementDocument.id == list_id)
                .update({UserAgreementDocument.deleted_at: datetime.utcnow()})
            )
