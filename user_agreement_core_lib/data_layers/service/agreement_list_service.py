from core_lib.data_layers.service.service import Service
from core_lib.data_transform.result_to_dict import result_to_dict, ResultToDict
from user_agreement_core_lib.data_layers.data_access.agreement_list_data_access import AgreementListDataAccess
from user_agreement_core_lib.data_layers.data_access.agreement_list_item_data_access import (
    AgreementListItemDataAccess,
)
from user_agreement_core_lib.data_layers.data_access.user_agreement_list_item_data_access import (
    UserAgreementListItemDataAccess,
)


class AgreementListService(Service):
    def __init__(
        self,
        user_agreement_list_item_da: UserAgreementListItemDataAccess,
        agreement_list_item: AgreementListItemDataAccess,
        agreement_list: AgreementListDataAccess
    ):
        self._user_agreement_list_item_da = user_agreement_list_item_da
        self._agreement_list_item_da = agreement_list_item
        self._agreement_list = agreement_list

    @ResultToDict()
    def agree_item(self, user_id: int, item_id: int):
        assert self._agreement_list_item_da.get_item(item_id)  # raise 404 when not found
        return self._user_agreement_list_item_da.agree(user_id, item_id)

    @ResultToDict()
    def disagree_item(self, user_id: int, item_id: int):
        assert self._user_agreement_list_item_da.agreed_user_item(user_id, item_id)  # raise 404 when not found
        return self._user_agreement_list_item_da.delete(user_id, item_id)

    @ResultToDict()
    def agreed_items(self, user_id: int, list_id: int):
        return self._user_agreement_list_item_da.user_agreed_list_items(user_id, list_id)

    @ResultToDict()
    def list_items(self, list_id: int):
        return self._agreement_list_item_da.get_list_items(list_id)

    @ResultToDict()
    def list_by_name(self, list_name: str):
        return self._agreement_list.get_by_name(list_name)

    def is_agreed_list(self, user_id, list_id: int) -> bool:
        items_list = set()
        user_items_list = set()
        items = self._agreement_list_item_da.get_list_items(list_id)
        for item in items:
            items_list.add(item.id)
        user_items = self._user_agreement_list_item_da.user_agreed_list_items(user_id, list_id)
        for item in user_items:
            user_items_list.add(result_to_dict(item)['agreement_list_item_id'])
        if items_list and user_items_list and len(items_list) == len(user_items_list):
            return True if items_list == user_items_list else False
        else:
            return False
