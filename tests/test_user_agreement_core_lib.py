import os
import unittest

from datetime import datetime
from time import sleep

from sqlalchemy.exc import DatabaseError

from core_lib.error_handling.status_code_exception import StatusCodeException
from tests.test_data.test_utils import sync_create_core_lib_config
from user_agreement_core_lib.user_agreement_core_lib import UserAgreementCoreLib


class TestUACoreLib(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config = sync_create_core_lib_config('./config')
        # config = sync_create_core_lib_config('../../user_agreement_core_lib/config')  # load real config
        cls.ua_core_lib = UserAgreementCoreLib(config)
        cls.user1_id = 1
        cls.user2_id = 2
        cls.user3_id = 3

    def test_agreement_document(self):
        version1 = 1
        version2 = 2
        dummy_md = '**some***basic - markdown'
        file_name = 'file_name'
        language = 'en'
        self.ua_core_lib.seed.seed_document(
            file_name,
            version1,
            language,
            os.path.join(os.path.dirname(__file__), 'test_data/test_doc.txt'),
            dummy_md,
        )
        self.assertEqual(self.ua_core_lib.agreement_document.get_document_latest_version(file_name, language)['version'], version1)
        with self.assertRaises(Exception):
            self.ua_core_lib.seed.seed_document(
                file_name,
                version1,
                language,
                os.path.join(os.path.dirname(__file__), 'test_data/test_doc.txt'),
                dummy_md,
            )
        with self.assertRaises(Exception):
            self.ua_core_lib.seed.seed_document(
                '',
                version1,
                language,
                os.path.join(os.path.dirname(__file__), 'test_data/test_doc.txt'),
                '',
            )
        document_data = self.ua_core_lib.seed.seed_document(
            'file_name',
            version2,
            language,
            os.path.join(os.path.dirname(__file__), 'test_data/test_doc.txt'),
            '**some***basic - markdown',
        )
        self.assertIsInstance(document_data, dict)
        self.assertEqual(len(document_data), 9)
        self.assertEqual(document_data['name'], file_name)
        self.assertEqual(document_data['version'], version2)
        self.assertEqual(document_data['file_text'], dummy_md)

        document_id = document_data.get('id')
        agreed_document = self.ua_core_lib.agreement_document.agree(self.user2_id, file_name, language)
        self.assertIsInstance(agreed_document, dict)
        self.assertEqual(agreed_document['agreement_document_id'], document_id)
        self.assertEqual(agreed_document['user_id'], self.user2_id)
        self.assertTrue(self.ua_core_lib.agreement_document.is_agreed_by_name(self.user2_id, file_name, language))
        self.ua_core_lib.agreement_document.disagree(self.user1_id, file_name, language)

        with self.assertRaises(AssertionError):
            self.ua_core_lib.agreement_document.disagree(self.user1_id, 'invalid_name', language)

        with self.assertRaises(AssertionError):
            self.ua_core_lib.agreement_document.agree(self.user1_id, 'invalid_name', language)

        with self.assertRaises(AssertionError):
            self.ua_core_lib.agreement_document.disagree(self.user2_id, 'invalid_name', language)

        with self.assertRaises(AssertionError):
            self.ua_core_lib.agreement_document.agree(self.user2_id, 'invalid_name', language)

        self.ua_core_lib.agreement_document.agree(self.user1_id, file_name, language)

        self.assertTrue(self.ua_core_lib.agreement_document.is_agreed_by_name(self.user1_id, file_name, language))
        self.assertTrue(self.ua_core_lib.agreement_document.is_agreed_by_name(self.user2_id, file_name, language))
        self.assertEqual(self.ua_core_lib.agreement_document.get_document_latest_version(file_name, language)['version'], version2)

    def _test_lists(self, list_name: str, agreed_user: int, non_agreed_user: int):
        items_seed = ['item1', 'item2', 'item3', 'item4']
        list_data = self.ua_core_lib.seed.seed_agreement_list(list_name, items_seed)
        self.assertNotEqual(list_data, None)

        list_id = list_data['id']
        list_items = list_data['list_items']

        self.assertIsInstance(list_data, dict)
        self.assertEqual(len(list_data), 6)
        self.assertNotEqual(list_items, None)
        self.assertEqual(len(list_items), len(items_seed))

        for item in list_items:
            list_item_data = self.ua_core_lib.agreement_list.agree_item(agreed_user, item['id'])
            self.assertIsInstance(list_item_data, dict)
            self.assertEqual(len(list_item_data), 7)

        with self.assertRaises(AssertionError):
            self.ua_core_lib.seed.seed_agreement_list('', items_seed)

        for item in list_items:
            with self.assertRaises(DatabaseError):
                self.ua_core_lib.agreement_list.agree_item(agreed_user, item['id'])

        self.assertTrue(self.ua_core_lib.agreement_list.is_agreed_list(agreed_user, list_id))
        self.assertFalse(self.ua_core_lib.agreement_list.is_agreed_list(non_agreed_user, list_id))

        first_item_id = list_items[0]['id']

        self.ua_core_lib.agreement_list.disagree_item(agreed_user, first_item_id)
        self.assertFalse(self.ua_core_lib.agreement_list.is_agreed_list(agreed_user, list_id))

        self.ua_core_lib.agreement_list.agree_item(agreed_user, first_item_id)
        self.assertTrue(self.ua_core_lib.agreement_list.is_agreed_list(agreed_user, list_id))

        with self.assertRaises(StatusCodeException):
            self.ua_core_lib.agreement_list.agree_item(agreed_user, -1)

        sleep(1)
        for item in list_items:
            self.ua_core_lib.agreement_list.disagree_item(agreed_user, item['id'])

    def test_agreement_list(self):
        # Randomly generate a name for testing
        list1_name = f'list_1_{str(datetime.utcnow().timestamp())}'
        list2_name = f'list_2_{str(datetime.utcnow().timestamp())}'

        self._test_lists(list1_name, self.user1_id, self.user2_id)
        self._test_lists(list2_name, self.user2_id, self.user1_id)

    def test_agreement_list_multiple_users(self):
        list_name = f'list_multi_{str(datetime.utcnow().timestamp())}'

        items_seed = ['item1', 'item2', 'item3', 'item4']
        list_data = self.ua_core_lib.seed.seed_agreement_list(list_name, items_seed)
        self.assertNotEqual(list_data, None)

        list_id = list_data['id']
        list_items = list_data['list_items']
        self.assertIsInstance(list_data, dict)
        self.assertEqual(len(list_data), 6)
        self.assertNotEqual(list_items, None)
        self.assertEqual(len(list_items), len(items_seed))

        for user in [self.user1_id, self.user2_id]:
            for item in list_items:
                list_item_data = self.ua_core_lib.agreement_list.agree_item(user, item['id'])
                self.assertIsInstance(list_item_data, dict)
                self.assertEqual(len(list_item_data), 7)

        self.assertTrue(self.ua_core_lib.agreement_list.is_agreed_list(self.user1_id, list_id))
        self.assertTrue(self.ua_core_lib.agreement_list.is_agreed_list(self.user2_id, list_id))
        self.assertFalse(self.ua_core_lib.agreement_list.is_agreed_list(self.user3_id, list_id))

        for item in list_items:
            self.ua_core_lib.agreement_list.disagree_item(self.user1_id, item['id'])
        self.assertFalse(self.ua_core_lib.agreement_list.is_agreed_list(self.user1_id, list_id))

        for item in list_items:
            self.ua_core_lib.agreement_list.agree_item(self.user1_id, item['id'])
        self.assertTrue(self.ua_core_lib.agreement_list.is_agreed_list(self.user1_id, list_id))

        with self.assertRaises(StatusCodeException):
            self.ua_core_lib.agreement_list.agree_item(self.user2_id, -1)

        for item in list_items:
            self.ua_core_lib.agreement_list.disagree_item(self.user2_id, item['id'])
