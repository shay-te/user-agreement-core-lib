import os
import unittest
from datetime import datetime
from unittest.mock import patch

from tests.test_data.test_utils import sync_create_core_lib_config
from user_agreement_core_lib.data_layers.data.agreement_db.entities.user_agreement_document import (
    UserAgreementDocument,
)
from user_agreement_core_lib.data_layers.data.agreement_db.entities.user_agreement_list_item import (
    UserAgreementListItem,
)
from user_agreement_core_lib.user_agreement_core_lib import UserAgreementCoreLib


class TestDeleteByUserId(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config = sync_create_core_lib_config('./config')
        cls.ua_core_lib = UserAgreementCoreLib(config)
        cls.user_id = 9001
        cls.other_user_id = 9002
        cls.list_user_id = 9003
        cls.collision_user_id = 9004

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

    def _seed_doc_and_list(self, suffix):
        doc_name = f'del_doc_{suffix}'
        list_name = f'del_list_{suffix}'
        language = 'en'
        self.ua_core_lib.seed.seed_document(
            doc_name,
            1,
            language,
            os.path.join(os.path.dirname(__file__), 'test_data/test_doc.txt'),
            '**md**',
        )
        list_data = self.ua_core_lib.seed.seed_agreement_list(list_name, ['item1', 'item2'])
        return doc_name, language, list_data

    def test_delete_by_user_id(self):
        suffix = str(datetime.utcnow().timestamp())
        doc_name, language, list_data = self._seed_doc_and_list(suffix)

        self.ua_core_lib.agreement_document.agree(self.user_id, doc_name, language)
        self.ua_core_lib.agreement_document.agree(self.other_user_id, doc_name, language)
        for item in list_data['list_items']:
            self.ua_core_lib.agreement_list.agree_item(self.user_id, item['id'])
            self.ua_core_lib.agreement_list.agree_item(self.other_user_id, item['id'])

        doc_db = self.ua_core_lib.agreement_document._user_agreement_document_da.db_session
        item_db = self.ua_core_lib.agreement_list._user_agreement_list_item_da.db_session

        self.assertGreater(self._active_doc_count(doc_db, self.user_id), 0)
        self.assertGreater(self._active_item_count(item_db, self.user_id), 0)

        self.ua_core_lib.agreement_document.delete_by_user_id(self.user_id)

        self.assertEqual(self._active_doc_count(doc_db, self.user_id), 0)
        self.assertEqual(self._active_item_count(item_db, self.user_id), 0)

        # other user's records are untouched
        self.assertGreater(self._active_doc_count(doc_db, self.other_user_id), 0)
        self.assertGreater(self._active_item_count(item_db, self.other_user_id), 0)

    def test_agreement_list_service_delete_by_user_id(self):
        # Pins the list-item delete path on AgreementListService rather than the document service.
        self.assertTrue(
            hasattr(self.ua_core_lib.agreement_list, 'delete_by_user_id'),
            'AgreementListService must own list-item soft-delete via delete_by_user_id',
        )

        suffix = f'svc_{datetime.utcnow().timestamp()}'
        _, _, list_data = self._seed_doc_and_list(suffix)
        for item in list_data['list_items']:
            self.ua_core_lib.agreement_list.agree_item(self.list_user_id, item['id'])

        item_db = self.ua_core_lib.agreement_list._user_agreement_list_item_da.db_session
        self.assertGreater(self._active_item_count(item_db, self.list_user_id), 0)

        self.ua_core_lib.agreement_list.delete_by_user_id(self.list_user_id)
        self.assertEqual(self._active_item_count(item_db, self.list_user_id), 0)

    def test_delete_by_user_id_token_collision(self):
        # Regression: when a pre-existing soft-deleted row already carries the same
        # second-resolution token, the UPDATE must bump past it to keep the
        # (user_id, agreement_document_id, deleted_at_token) unique index satisfied.
        suffix = f'collide_{datetime.utcnow().timestamp()}'
        doc_name = f'collide_doc_{suffix}'
        language = 'en'
        document = self.ua_core_lib.seed.seed_document(
            doc_name,
            1,
            language,
            os.path.join(os.path.dirname(__file__), 'test_data/test_doc.txt'),
            '**md**',
        )

        doc_da = self.ua_core_lib.agreement_document._user_agreement_document_da
        doc_db = doc_da.db_session

        now = datetime.utcnow()
        token = int(now.timestamp())
        with doc_db.get() as session:
            stale = UserAgreementDocument()
            stale.user_id = self.collision_user_id
            stale.agreement_document_id = document['id']
            stale.is_agreed = True
            stale.signed_at = now
            stale.deleted_at = now
            stale.deleted_at_token = token
            session.add(stale)
            session.commit()

        self.ua_core_lib.agreement_document.agree(self.collision_user_id, doc_name, language)

        frozen = datetime.fromtimestamp(token)

        class _FrozenDatetime(datetime):
            @classmethod
            def utcnow(cls):
                return frozen

        target = 'user_agreement_core_lib.data_layers.data_access.user_agreement_document_data_access.datetime'
        with patch(target, _FrozenDatetime):
            # Must not raise IntegrityError despite the stale row sharing `token`.
            self.ua_core_lib.agreement_document.delete_by_user_id(self.collision_user_id)

        self.assertEqual(self._active_doc_count(doc_db, self.collision_user_id), 0)
        with doc_db.get() as session:
            tokens = [
                row.deleted_at_token
                for row in session.query(UserAgreementDocument)
                .filter(UserAgreementDocument.user_id == self.collision_user_id)
                .all()
            ]
        # Two soft-deleted rows for the same (user_id, doc_id) must hold distinct tokens.
        self.assertEqual(len(tokens), len(set(tokens)))


if __name__ == '__main__':
    unittest.main()
