from core_lib.data_layers.service.service import Service
from core_lib.data_transform.result_to_dict import ResultToDict, result_to_dict
from user_agreement_core_lib.data_layers.data_access.agreement_document_data_access import (
    AgreementDocumentDataAccess,
)
from user_agreement_core_lib.data_layers.data_access.agreement_list_data_access import (
    AgreementListDataAccess,
)
from user_agreement_core_lib.data_layers.data_access.agreement_list_item_data_access import (
    AgreementListItemDataAccess,
)


class SeedService(Service):
    def __init__(
        self,
        agreement_document: AgreementDocumentDataAccess,
        agreement_list: AgreementListDataAccess,
        agreement_list_item: AgreementListItemDataAccess,
    ):
        self._agreement_document = agreement_document
        self._agreement_list = agreement_list
        self._agreement_list_item = agreement_list_item

    @ResultToDict()
    def seed_document(self, name: str, version: str, language: str, file_path: str, file_text_content: str):
        assert name and version and file_path and file_text_content
        with open(file_path, 'rb') as file:
            data_blob = file.read()
            return self._agreement_document.create(
                {
                    'name': name,
                    'version': version,
                    'language': language,
                    'file_text': file_text_content,
                    'file': data_blob,
                }
            )

    def seed_agreement_list(self, agreement_list_name: str, agreement_list_items: list = []):
        assert agreement_list_name
        list_items = []
        list_data = result_to_dict(self._agreement_list.add(agreement_list_name))
        if agreement_list_items and all(isinstance(item, str) for item in agreement_list_items):
            for item in agreement_list_items:
                list_items.append(result_to_dict(self._agreement_list_item.add(list_data['id'], item)))
        list_data.setdefault('list_items', list_items)
        return list_data
