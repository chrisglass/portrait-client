import unittest
import time
import json
#import numpy  #XXX: this is not part of the real dependencies! Install manually
#import msgpack  #XXX: Not in the deps either!

from portrait.lib import bpickle


@unittest.skip  #XXX: REMOVE BEFORE FLIGHT
class BpickleBechmarksTest(unittest.TestCase):

    small_dict = {
        "a string": "something",
        "a float": 12.45,
        "an int": 12345,
        "true!": True,
        "false": False,
        "none": None,
        "dict": {"a": 1, "b": 2, "c": 3},
        "list": ["a", "b", "c"]}

    def setUp(self):
        self.big_dict = {}

        for i in range(1000):
            self.big_dict.update({i: self.small_dict.copy()})


    def test_bpickle_vs_json_1000_big_dict(self):
        """
        Some crappy benchmarks.
        """
        bpickle_results = []
        json_results = []
        msgpack_results = []

        for i in range(1000):

            # Time the conversion
            bpickle_start = time.time()
            result = bpickle.dumps(self.big_dict)
            assert result is not None
            bpickle_stop = time.time()

            json_start = time.time()
            result2 = json.dumps(self.big_dict)
            assert result2 is not None
            json_stop = time.time()


            msgpack_start = time.time()
            result2 = msgpack.dumps(self.big_dict)
            assert result2 is not None
            msgpack_stop = time.time()


            # Compute elapsed time for each
            bpickle_elapsed = bpickle_stop - bpickle_start
            json_elapsed = json_stop - json_start
            msgpack_elapsed = msgpack_stop - msgpack_start

            # Append for this run's results.
            bpickle_results.append(bpickle_elapsed)
            json_results.append(json_elapsed)
            msgpack_results.append(msgpack_elapsed)

        print("Bpickle average: %f" % numpy.mean(bpickle_results))
        print("Bpickle standard deviation: %f" % numpy.std(bpickle_results))
        print("JSON average: %f" % numpy.mean(json_results))
        print("JSON standard deviation: %f" % numpy.std(json_results))
        print("msgpack average: %f" % numpy.mean(msgpack_results))
        print("msgpack standard deviation: %f" % numpy.std(msgpack_results))
        import ipdb; ipdb.set_trace()
