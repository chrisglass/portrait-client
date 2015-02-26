import unittest

from landscape.exchanger.exchange import Exchanger


class FauxStorage(object):

    def pop_all_pending_messages(self):
        return [{"type": "whatever"}]


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

        exchanger = Exchanger(
            FauxStorage(), {"server_name": "example.com"}, stub_post)

        # Monkeypatching
        exchanger._process_result = stub_process_result

        exchanger.run()

        self.assertEqual([None], process_calls)

