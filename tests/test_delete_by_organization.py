import os
import unittest
from datetime import datetime

from tests.test_data.test_utils import sync_create_core_lib_config
from user_agreement_core_lib.data_layers.data.agreement_db.entities.user_agreement_document import (
    UserAgreementDocument,
)
from user_agreement_core_lib.data_layers.data.agreement_db.entities.user_agreement_list_item import (
    UserAgreementListItem,
)
from user_agreement_core_lib.user_agreement_core_lib import UserAgreementCoreLib


class TestDeleteByUserIds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config = sync_create_core_lib_config('./config')
        cls.ua_core_lib = UserAgreementCoreLib(config)
        cls.user_id = 9001
        cls.other_user_id = 9002

    def _active_doc_count(self, db, user_id):
        with db.get() as session:
            return (
                session.query(UserAgreementDocument)
                .filter(
                    UserAgreementDocument.deleted_at_token == 0,
                    UserAgreementDocument.user_id == user_id,
                )
                .count()
            )

    def _active_item_count(self, db, user_id):
        with db.get() as session:
            return (
                session.query(UserAgreementListItem)
                .filter(
                    UserAgreementListItem.deleted_at_token == 0,
                    UserAgreementListItem.user_id == user_id,
                )
                .count()
            )

    def test_delete_by_user_ids(self):
        suffix = str(datetime.utcnow().timestamp())
        doc_name = f'del_doc_{suffix}'
        list_name = f'del_list_{suffix}'
        language = 'en'

        document = self.ua_core_lib.seed.seed_document(
            doc_name,
            1,
            language,
            os.path.join(os.path.dirname(__file__), 'test_data/test_doc.txt'),
            '**md**',
        )
        list_data = self.ua_core_lib.seed.seed_agreement_list(list_name, ['item1', 'item2'])

        self.ua_core_lib.agreement_document.agree(self.user_id, doc_name, language)
        self.ua_core_lib.agreement_document.agree(self.other_user_id, doc_name, language)
        for item in list_data['list_items']:
            self.ua_core_lib.agreement_list.agree_item(self.user_id, item['id'])
            self.ua_core_lib.agreement_list.agree_item(self.other_user_id, item['id'])

        doc_db = self.ua_core_lib.agreement_document._user_agreement_document_da.db_session
        item_db = self.ua_core_lib.agreement_list._user_agreement_list_item_da.db_session

        self.assertGreater(self._active_doc_count(doc_db, self.user_id), 0)
        self.assertGreater(self._active_item_count(item_db, self.user_id), 0)

        # no-op on empty list
        self.ua_core_lib.agreement_document.delete_by_user_ids([])
        self.assertGreater(self._active_doc_count(doc_db, self.user_id), 0)

        self.ua_core_lib.agreement_document.delete_by_user_ids([self.user_id])

        self.assertEqual(self._active_doc_count(doc_db, self.user_id), 0)
        self.assertEqual(self._active_item_count(item_db, self.user_id), 0)

        # other user's records are untouched
        self.assertGreater(self._active_doc_count(doc_db, self.other_user_id), 0)
        self.assertGreater(self._active_item_count(item_db, self.other_user_id), 0)


if __name__ == '__main__':
    unittest.main()
