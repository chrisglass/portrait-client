import unittest
from landscape.exchanger import ping


class FauxScheduler(object):

    def enter(self, *args):
        pass


class PingTest(unittest.TestCase):

    def test_pings(self):
        config = {"ping_url": "http://example.com/ping"}
        storage = {"insecure_id": "whatever"}
        scheduler = FauxScheduler()
        calls = []
        def fauxpost(*args, **kwargs):
            calls.append((args, kwargs))
        post = fauxpost
        pinger = ping.Pinger(config, storage, post=post)

        pinger.run()
