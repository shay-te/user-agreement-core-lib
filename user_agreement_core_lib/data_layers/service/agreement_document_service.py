from core_lib.data_layers.service.service import Service
from core_lib.data_transform.result_to_dict import ResultToDict
from user_agreement_core_lib.data_layers.data.agreement_db.entities.user_agreement_document import UserAgreementDocument
from user_agreement_core_lib.data_layers.data_access.agreement_document_data_access import AgreementDocumentDataAccess
from user_agreement_core_lib.data_layers.data_access.user_agreement_document_data_access import (
    UserAgreementDocumentDataAccess,
)


class AgreementDocumentService(Service):
    def __init__(
        self,
        agreement_document: AgreementDocumentDataAccess,
        user_agreement_document_da: UserAgreementDocumentDataAccess,
    ):
        self._agreement_document = agreement_document
        self._user_agreement_document_da = user_agreement_document_da

    @ResultToDict()
    def agree(self, user_id: int, document_name: str, language: str, document_id: int):
        assert self._agreement_document.get(document_id)  # raise 404 when not found

        existing = self._user_agreement_document_da.get_agreed_document_by_name(user_id=user_id,document_name= document_name, language=language)

        if existing and existing.is_agreed:
            return existing

        if existing:
            self._user_agreement_document_da.delete(user_id, document_id)

        return self._user_agreement_document_da.set_agreement(user_id, document_id, True)

    @ResultToDict()
    def disagree(self, user_id: int, document_name: str, language: str, document_id: int):
        assert self._agreement_document.get(document_id)  # raise 404 when not found

        existing = self._user_agreement_document_da.get_agreed_document_by_name(user_id=user_id, document_name=document_name, language=language)

        if existing and not existing.is_agreed:
            return existing

        if existing:
            self._user_agreement_document_da.delete(user_id, document_id)

        return self._user_agreement_document_da.set_agreement(user_id, document_id, False)

    @ResultToDict()
    def get_document_latest_version(self, name: str, language: str):
        return self._agreement_document.get_latest_version(name, language)

    def is_agreed_by_name(self, user_id: int, document_name: str, language: str) -> bool:
        user_agreement_doc = self._user_agreement_document_da.get_agreed_document_by_name(user_id, document_name, language)
        return bool(user_agreement_doc and user_agreement_doc.is_agreed)
