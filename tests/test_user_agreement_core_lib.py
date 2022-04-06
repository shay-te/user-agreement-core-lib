import unittest

from tests.test_data.test_utils import sync_create_core_lib_config
from user_agreement_core_lib.user_agreement_core_lib import UserAgreementCoreLib


class UACoreLib(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config = sync_create_core_lib_config('../../user_agreement_core_lib/config')
        cls.ua_core_lib = UserAgreementCoreLib(config)

    def test_agreement_document(self):
        print(self.ua_core_lib.agreement_document.create())