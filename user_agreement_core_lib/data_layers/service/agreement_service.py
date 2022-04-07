from core_lib.data_layers.data.handler.sql_alchemy_data_handler_registry import (
    SqlAlchemyDataHandlerRegistry,
)
from core_lib.data_layers.service.service import Service
from core_lib.data_transform.result_to_dict import result_to_dict, ResultToDict
from user_agreement_core_lib.data_layers.data_access.agreement_list_item_data_access import (
    AgreementListItemDataAccess,
)
from user_agreement_core_lib.data_layers.data_access.user_agreement_document_data_access import (
    UserAgreementDocumentDataAccess,
)
from user_agreement_core_lib.data_layers.data_access.user_agreement_list_item_data_access import (
    UserAgreementListItemDataAccess,
)


class AgreementService(Service):
    def __init__(
        self,
        db: SqlAlchemyDataHandlerRegistry,
        agreement_list_item: AgreementListItemDataAccess,
    ):
        self._user_agreement_document_da = UserAgreementDocumentDataAccess(db)
        self._user_agreement_list_item_da = UserAgreementListItemDataAccess(db)
        self._agreement_list_item_da = agreement_list_item

    @ResultToDict()
    def agree_document(self, user_id: int, document_id: int):
        return self._user_agreement_document_da.agree(user_id, document_id)

    @ResultToDict()
    def agree_items(self, user_id: int, item_id: int):
        self._agreement_list_item_da.get_item(item_id)  # For verifying if the item exists else will raise an exception
        return self._user_agreement_list_item_da.agree(user_id, item_id)

    @ResultToDict()
    def disagree_items(self, user_id: int, item_id: int):
        self._user_agreement_list_item_da.agreed_user_item(
            user_id, item_id
        )  # For verifying if the user has agreed to the item earlier or not else will raise an exception
        return self._user_agreement_list_item_da.delete(user_id, item_id)

    def is_agreed_document(self, user_id: int, document_id: int) -> bool:
        agreed_docs_list = []
        agreed_docs = self._user_agreement_document_da.agreed_documents(user_id)
        for row in agreed_docs:
            agreed_docs_list.append(row.agreement_document_id)
        return document_id in agreed_docs_list

    def is_agreed_list(self, user_id, list_id: int) -> bool:
        items_list = []
        user_items_list = []
        items = self._agreement_list_item_da.get_list_items(list_id)
        for item in items:
            items_list.append(item.id)
        user_items = self._user_agreement_list_item_da.agreed_list_items(user_id, list_id)
        for item in user_items:
            user_items_list.append(result_to_dict(item)['agreement_list_item_id'])
        if items_list and user_items_list and len(items_list) == len(user_items_list):
            return True if set(items_list) == set(user_items_list) else False
        else:
            return False
