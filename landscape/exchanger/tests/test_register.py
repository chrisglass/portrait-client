import unittest

from landscape.exchanger.register import Registration

class RegisterTest(unittest.TestCase):

    def test_should_register(self):
        """
        We should only register with the server if the secure-id is not set.
        """
        storage = {"secure-id": None}
        registration = Registration(storage)
        self.assertTrue(registration.should_register())

    def test_should_not_register(self):
        """
        We should only register with the server if the secure-id is not set.
        """
        storage = {"secure-id": "secure!"}
        registration = Registration(storage)
        self.assertFalse(registration.should_register())
