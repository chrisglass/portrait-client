import unittest

from portrait.old.message_schemas import RESYNCHRONIZE
from portrait.old.schema import InvalidError


class MessageSchemaTest(unittest.TestCase):

    def test_message_coercion_succeeds(self):
        """
        Coercing a message payload with a schema succeeds when the passed dict
        conforms to the schema. RESYNCHRONIZE is chosen here because it's
        small and simple.
        """
        payload = {"type": "resynchronize"}
        result = RESYNCHRONIZE.coerce(payload)

        self.assertEqual(payload, result)

    def test_message_coercion_fails(self):
        """
        Coercing a message payload with a schema fails when the passed dict
        does not conforms to the schema. RESYNCHRONIZE is chosen here because
        it's small and simple.
        """
        payload = {"blah": "resynchronize"}
        self.assertRaises(InvalidError, RESYNCHRONIZE.coerce, payload)

    def test_message_coercion_fails_on_empty(self):
        """
        Coercing a message payload with a schema fails when the passed dict is
        empty. RESYNCHRONIZE is chosen here because it's small and simple.
        """
        payload = {}
        self.assertRaises(InvalidError, RESYNCHRONIZE.coerce, payload)
