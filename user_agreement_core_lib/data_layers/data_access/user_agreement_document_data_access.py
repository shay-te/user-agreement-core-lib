from datetime import datetime

from sqlalchemy import desc

from core_lib.connection.sql_alchemy_connection_factory import (
    SqlAlchemyConnectionFactory,
)
from core_lib.data_layers.data_access.data_access import DataAccess
from user_agreement_core_lib.data_layers.data.agreement_db.entities.agreement_document import AgreementDocument

from user_agreement_core_lib.data_layers.data.agreement_db.entities.user_agreement_document import (
    UserAgreementDocument,
)


class UserAgreementDocumentDataAccess(DataAccess):
    def __init__(self, db: SqlAlchemyConnectionFactory):
        self.db_session = db

    def set_agreement(self, user_id: int, document_id: int, is_agreed: bool = False):
        with self.db_session.get() as session:
            agreement = UserAgreementDocument()
            agreement.user_id = user_id
            agreement.agreement_document_id = document_id
            agreement.is_agreed = is_agreed
            agreement.signed_at = datetime.utcnow() if is_agreed else None

            session.add(agreement)
            session.commit()
            return agreement

    def get_agreed_document_by_name(self, user_id: int, document_name: str, language: str):
        with self.db_session.get() as session:
            return (
                session.query(UserAgreementDocument)
                .join(
                    AgreementDocument,
                    UserAgreementDocument.agreement_document_id == AgreementDocument.id
                )
                .filter(
                    UserAgreementDocument.user_id == user_id,
                    AgreementDocument.name == document_name,
                    AgreementDocument.language == language,
                    UserAgreementDocument.deleted_at == None,
                    AgreementDocument.deleted_at == None,
                )
                .order_by(desc(AgreementDocument.version))
                .first()
            )

    def delete(self, user_id: int, document_id: int):
        with self.db_session.get() as session:
            return session.query(UserAgreementDocument).filter(
                UserAgreementDocument.agreement_document_id == document_id,
                UserAgreementDocument.user_id == user_id,
                UserAgreementDocument.deleted_at == None
            ).update({
                UserAgreementDocument.deleted_at: datetime.utcnow(),
                UserAgreementDocument.deleted_at_token: int(datetime.utcnow().timestamp()),
            })