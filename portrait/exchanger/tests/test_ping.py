import unittest

from portrait.exchanger import ping
from portrait.lib import bpickle


class FauxScheduler(object):

    def enter(self, *args):
        pass


class PingTest(unittest.TestCase):

    def test_pings(self):
        config = {"server": "example.com"}
        storage = {"insecure_id": "whatever"}
        calls = []

        def fauxpost(*args, **kwargs):
            calls.append((args, kwargs))

        post = fauxpost
        pinger = ping.Pinger(config, post=post,
                             main_store_factory=lambda x: storage)

        pinger.run_wrapper()
        expected = [
            (('http://example.com/ping',),
                {'data': {'insecure_id': 'whatever'}})]
        self.assertEqual(expected, calls)

    def test_bails_out_if_no_insecure_id(self):
        """
        The pinger does nothing if no insecure_id is set in the storage.
        """
        config = {"server": "example.com"}
        storage = {"insecure_id": None}
        calls = []

        def fauxpost(*args, **kwargs):
            calls.append((args, kwargs))

        post = fauxpost
        pinger = ping.Pinger(config, post=post,
                             main_store_factory=lambda x: storage)

        pinger.run_wrapper()
        expected = []
        self.assertEqual(expected, calls)

    def test_has_messages(self):
        """
        The result of the ping is a "meesages are ready for you" answer.
        """
        config = {"server": "example.com"}
        storage = {"insecure_id": "whatever"}
        calls = []

        def fauxpost(*args, **kwargs):
            calls.append((args, kwargs))
            return bpickle.dumps({"messages": True})

        post = fauxpost

        pinger = ping.Pinger(config, post=post,
                             main_store_factory=lambda x: storage)
        pinger.run_wrapper()

        expected = [
            (('http://example.com/ping',),
                {'data': {'insecure_id': 'whatever'}})]
        self.assertEqual(expected, calls)
