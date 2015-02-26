import unittest

from collections import namedtuple

from landscape.lib import bpickle
from landscape.exchanger.exchange import Exchanger


class FauxStorage(object):

    def __init__(self, messages=None):
        self.messages = messages
        self.contents = {}

    def set(self, key, value):
        self.contents[key] = value

    def pop_all_pending_messages(self):
        return self.messages


class ExchangerTest(unittest.TestCase):

    def test_exchanger_run_no_answer_processing(self):
        """
        Call the exchanger's run() method in-thread, and ensure the post method
        is called. this test does not worry about processing the answer, and
        just stubs the call.
        """
        post_calls = []
        process_calls = []

        def stub_post(url, **kwargs):
            post_calls.append((url, kwargs))

        def stub_process_result(result):
            process_calls.append(result)

        exchanger = Exchanger(FauxStorage([{"type": "test"}]),
                              {"server_name": "example.com"}, stub_post)

        # Monkeypatching
        exchanger._process_result = stub_process_result

        exchanger.run()

        self.assertEqual([None], process_calls)
        expected_payload = {
            'data': b'ds14:accepted-typess0:s10:client-apis3:3.3s8:messagesld'
                    b's4:types4:test;;s22:next-expected-sequencei1;s8:sequenc'
                    b'es1:0s10:server-apis3:3.3s14:total-messagesi1;;',
            'headers': {
                'User-Agent': 'Portrait-client DEVEL',
                'X-Message-API': '3.3',
                'Content-Type': 'application/octet-stream'}}

        expected = [("https://example.com/message-system", expected_payload)]

        self.assertEqual(expected, post_calls)

    def test_exchanger_bails_out_on_no_message(self):
        """
        The exchanger's run() method returns immediately if there are no
        messages to send.
        """
        post_calls = []
        process_calls = []

        def stub_post(url, **kwargs):
            post_calls.append((url, kwargs))

        def stub_process_result(result):
            process_calls.append(result)


        exchanger = Exchanger(FauxStorage([]),
                              {"server_name": "example.com"}, stub_post)
        # Monkeypatching
        exchanger._process_result = stub_process_result

        exchanger.run()

        self.assertEqual([], process_calls)
        self.assertEqual([], post_calls)

    def test_wb_process_results_dispatching(self):
        """
        The "process result" method takes a bpickled list of messages and
        calls the appropriate handler depending on the message type.
        """
        answer = {"messages": [{"type": "set-id"}]}
        banswer = bpickle.dumps(answer)

        contents = namedtuple("Answer", "content")
        contents.content = banswer

        exchanger = Exchanger({}, {})

        calls = []

        def stub_handle_set_id(message):
            calls.append(True)

        exchanger._handle_set_id = stub_handle_set_id
        exchanger._process_result(contents)

        self.assertEqual([True], calls)

    def test_wb_handle_set_id(self):
        """
        Handle-set-id sets the secure-id and insecure-id keys in storage.
        """
        storage = FauxStorage()
        exchanger = Exchanger(storage, {})

        exchanger._handle_set_id({"type": "set-id",
                                  "id": "secure",
                                  "insecure-id": "insecure"})
        expected = {"secure-id": "secure", "insecure-id": "insecure"}
        self.assertEqual(expected, storage.contents)
