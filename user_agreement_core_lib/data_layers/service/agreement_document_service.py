from core_lib.data_layers.service.service import Service
from core_lib.data_transform.result_to_dict import result_to_dict, ResultToDict
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
    def agree(self, user_id: int, document_id: int):
        return self._user_agreement_document_da.agree(user_id, document_id)

    @ResultToDict()
    def get_document_latest_version(self, name: str):
        return self._agreement_document.get_latest_version(name)

    def is_agreed(self, user_id: int, document_id: int) -> bool:
        return True if self._user_agreement_document_da.get_agreed_document_by_id(user_id, document_id) else False

    def is_agreed_by_name(self, user_id: int, document_name: str) -> bool:
        return True if self._user_agreement_document_da.get_agreed_document_by_name(user_id, document_name) else False
