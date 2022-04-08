import os
import unittest

from datetime import datetime

from core_lib.error_handling.status_code_exception import StatusCodeException
from tests.test_data.test_utils import sync_create_core_lib_config
from user_agreement_core_lib.user_agreement_core_lib import UserAgreementCoreLib


class TestUACoreLib(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # config = sync_create_core_lib_config('./config')
        config = sync_create_core_lib_config('../../user_agreement_core_lib/config')
        cls.ua_core_lib = UserAgreementCoreLib(config)
        cls.user1_id = 1
        cls.user2_id = 2
        cls.user3_id = 3

    def test_agreement_document(self):
        version1 = str(datetime.utcnow().timestamp())
        version2 = str(datetime.utcnow().timestamp() + 100)
        dummy_md = '**some***basic - markdown'
        file_name = 'file_name'
        self.ua_core_lib.seed_service.seed_document(
            file_name,
            os.path.join(os.path.dirname(__file__), 'test_data/test_doc.txt'),
            dummy_md,
            version1,
        )
        with self.assertRaises(Exception):
            self.ua_core_lib.seed_service.seed_document(
                file_name,
                os.path.join(os.path.dirname(__file__), 'test_data/test_doc.txt'),
                dummy_md,
                version1,
            )
            self.ua_core_lib.seed_service.seed_document(
                file_name,
                os.path.join(os.path.dirname(__file__), 'test_data/test_doc.txt'),
                dummy_md,
                version1,
            )
            self.ua_core_lib.seed_service.seed_document(
                '',
                os.path.join(os.path.dirname(__file__), 'test_data/test_doc.txt'),
                '',
                version1,
            )
        document_data = self.ua_core_lib.seed_service.seed_document(
            'file_name',
            os.path.join(os.path.dirname(__file__), 'test_data/test_doc.txt'),
            '**some***basic - markdown',
            version2,
        )
        self.assertIsInstance(document_data, dict)
        self.assertEqual(len(document_data), 8)
        self.assertEqual(document_data['name'], file_name)
        self.assertEqual(document_data['version'], version2)
        self.assertEqual(document_data['file_text'], dummy_md)

        document_id = document_data.get('id')
        agreed_document = self.ua_core_lib.agreement_service.agree_document(self.user1_id, document_id)
        self.assertIsInstance(agreed_document, dict)
        self.assertEqual(agreed_document['agreement_document_id'], document_id)
        self.assertEqual(agreed_document['user_id'], self.user1_id)

        self.assertTrue(self.ua_core_lib.agreement_service.is_agreed_document(self.user1_id, document_id))
        self.assertFalse(self.ua_core_lib.agreement_service.is_agreed_document(self.user2_id, document_id))

    def _test_lists(self, list_name: str, agreed_user: int, non_agreed_user: int):
        items = ['item1', 'item2', 'item3', 'item4']
        list_data = self.ua_core_lib.seed_service.seed_agreement_list(list_name, items)
        list_id = list_data['id']

        self.assertIsInstance(list_data, dict)
        self.assertEqual(len(list_data), 6)

        for items in list_data['list_items']:
            list_item_data = self.ua_core_lib.agreement_service.agree_item(agreed_user, items['id'])
            self.assertIsInstance(list_item_data, dict)
            self.assertEqual(len(list_item_data), 7)

        with self.assertRaises(Exception):
            self.ua_core_lib.seed_service.seed_agreement_list('', items)
            for items in list_data['list_items']:
                self.ua_core_lib.agreement_service.agree_item(agreed_user, items['id'])

        self.assertTrue(self.ua_core_lib.agreement_service.is_agreed_list(agreed_user, list_id))
        self.assertFalse(self.ua_core_lib.agreement_service.is_agreed_list(non_agreed_user, list_id))

        self.ua_core_lib.agreement_service.disagree_item(agreed_user, list_data['list_items'][0]['id'])
        self.assertFalse(self.ua_core_lib.agreement_service.is_agreed_list(agreed_user, list_id))

        self.ua_core_lib.agreement_service.agree_item(agreed_user, list_data['list_items'][0]['id'])
        self.assertTrue(self.ua_core_lib.agreement_service.is_agreed_list(agreed_user, list_id))

        with self.assertRaises(StatusCodeException):
            self.ua_core_lib.agreement_service.agree_item(agreed_user, -1)
            for items in list_data['list_items']:
                self.ua_core_lib.agreement_service.disagree_item(agreed_user, items['id'])

    def test_agreement_list(self):
        # Randomly generate a name for testing
        list1_name = str(datetime.utcnow().timestamp())
        list2_name = str(datetime.utcnow().timestamp() + 100)

        self._test_lists(list1_name, self.user1_id, self.user2_id)
        self._test_lists(list2_name, self.user2_id, self.user1_id)

    def test_agreement_list_multiple_users(self):
        list_name = str(datetime.utcnow().timestamp() + 200)

        items = ['item1', 'item2', 'item3', 'item4']
        list_data = self.ua_core_lib.seed_service.seed_agreement_list(list_name, items)
        list_id = list_data['id']

        self.assertIsInstance(list_data, dict)
        self.assertEqual(len(list_data), 6)

        for user in [self.user1_id, self.user2_id]:
            for items in list_data['list_items']:
                list_item_data = self.ua_core_lib.agreement_service.agree_item(user, items['id'])
                self.assertIsInstance(list_item_data, dict)
                self.assertEqual(len(list_item_data), 7)

        self.assertTrue(self.ua_core_lib.agreement_service.is_agreed_list(self.user1_id, list_id))
        self.assertTrue(self.ua_core_lib.agreement_service.is_agreed_list(self.user2_id, list_id))
        self.assertFalse(self.ua_core_lib.agreement_service.is_agreed_list(self.user3_id, list_id))

        for items in list_data['list_items']:
            self.ua_core_lib.agreement_service.disagree_item(self.user1_id, items['id'])
        self.assertFalse(self.ua_core_lib.agreement_service.is_agreed_list(self.user1_id, list_id))

        for items in list_data['list_items']:
            self.ua_core_lib.agreement_service.agree_item(self.user1_id, items['id'])
        self.assertTrue(self.ua_core_lib.agreement_service.is_agreed_list(self.user1_id, list_id))

        with self.assertRaises(StatusCodeException):
            self.ua_core_lib.agreement_service.agree_item(self.user2_id, -1)
            for items in list_data['list_items']:
                self.ua_core_lib.agreement_service.disagree_item(self.user2_id, items['id'])
