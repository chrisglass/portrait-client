import unittest

from portrait.exchanger.register import Registration

class RegisterTest(unittest.TestCase):

    def test_should_register(self):
        """
        We should only register with the server if the secure-id is not set.
        """
        storage = {"secure-id": None}
        registration = Registration({}, main_store_factory=lambda x: storage)
        self.assertTrue(registration.should_register())

    def test_should_not_register(self):
        """
        We should only register with the server if the secure-id is not set.
        """
        storage = {"secure-id": "secure!"}
        registration = Registration({}, main_store_factory=lambda x: storage)
        self.assertFalse(registration.should_register())
