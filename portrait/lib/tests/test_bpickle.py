import unittest

from portrait.lib import bpickle

REAL_ANSWER = (b"ds8:messageslds4:types14:accepted-typess5:typeslu8:register"
               b"u4:test;;ds2:ids9:secure-ids11:insecure-idi999999;s4:types6:"
               b"set-id;;s10:server-apiu3:3.3s11:server-uuids11:server-uuid;")


class BPickleTest(unittest.TestCase):

    def test_int(self):
        self.assertEqual(bpickle.loads(bpickle.dumps(1)), 1)

    def test_float(self):
        self.assertAlmostEquals(bpickle.loads(bpickle.dumps(2.3)), 2.3)

    def test_float_scientific_notation(self):
        number = 0.00005
        self.assertTrue("e" in repr(number))
        self.assertAlmostEquals(bpickle.loads(bpickle.dumps(number)), number)

    def test_string(self):
        self.assertEqual(bpickle.loads(bpickle.dumps('foo')), 'foo')

    def test_list(self):
        self.assertEqual(bpickle.loads(bpickle.dumps([1, 2, 'hello', 3.0])),
                         [1, 2, 'hello', 3.0])

    def test_tuple(self):
        data = bpickle.dumps((1, [], 2, 'hello', 3.0))
        self.assertEqual(bpickle.loads(data),
                         (1, [], 2, 'hello', 3.0))

    def test_none(self):
        self.assertEqual(bpickle.loads(bpickle.dumps(None)), None)

    def test_unicode(self):
        self.assertEqual(bpickle.loads(bpickle.dumps(u'\xc0')), u'\xc0')

    def test_bool(self):
        self.assertEqual(bpickle.loads(bpickle.dumps(True)), True)

    def test_dict(self):
        dumped_tostr = bpickle.dumps({True: "hello"})
        self.assertEqual(bpickle.loads(dumped_tostr),
                         {True: "hello"})
        dumped_tobool = bpickle.dumps({True: False})
        self.assertEqual(bpickle.loads(dumped_tobool),
                         {True: False})

    def test_long(self):
        long = 99999999999999999999999999999
        self.assertEqual(bpickle.loads(bpickle.dumps(long)), long)

    def test_loads_empty_string(self):
        self.assertRaises(ValueError, bpickle.loads, "")

    def test_dumps_unsupported_object(self):
        class something(object):
            pass
        self.assertRaises(ValueError, bpickle.dumps, something())

    def test_loads_unknown_character(self):
        wrong = b'zblah'  # 'z' is not a valid type character.
        self.assertRaises(ValueError, bpickle.loads, wrong)

    def test_ping_result_message_decode(self):
        """
        This is an example message received from an actual ping server. Let's
        try to make sense of it.
        """
        repsonse = b'ds8:messagesb1;'  # As returned by the "requests" lib
        result = bpickle.loads(repsonse)
        expected = {"messages": True}
        self.assertEqual(expected, result)

    def test_ping_result_message_encode(self):
        """Let's ensure the encoding/decoding is symmetric "by hand"."""
        payload = {"messages": True}
        expected = b'ds8:messagesb1;'
        result = bpickle.dumps(payload)
        self.assertEqual(expected, result)

    def test_real_registration_answer_loading(self):
        """ We succeed at decoding a real-world example."""
        expected = {
            'server-api': '3.3',
            'server-uuid': 'server-uuid',
            'messages': [
                {'types': ['register', 'test'], 'type': 'accepted-types'},
                {'id': 'secure-id', 'insecure-id': 999999, 'type': 'set-id'}]}

        result = bpickle.loads(REAL_ANSWER)
        self.assertEqual(expected, result)
