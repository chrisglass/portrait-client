import os
import tempfile
import textwrap
import unittest

from landscape.config import load_config_file


class Maintest(unittest.TestCase):

    def setUp(self):
        _, self.filename = tempfile.mkstemp()

    def tearDown(self):
        os.remove(self.filename)

    def test_load_config_file_works(self):
        """
        Loading the config file returns the python representation of the yaml
        contents.
        """
        contents = textwrap.dedent("""
        ping_interval: 30
        server: example.com
        """)

        with open(self.filename, "w") as thefile:
            thefile.write(contents)

        result = load_config_file(self.filename)
        expected = {"ping_interval": 30, "server": "example.com"}
        self.assertEqual(expected, result)

    def test_empty_file_loads_defaults(self):
        """
        If the configuration file exists but is empty or contains other keys,
        the defaults are used/loaded.
        """
        contents = textwrap.dedent("""
        something_random: Whatever
        """)

        with open(self.filename, "w") as thefile:
            thefile.write(contents)

        result = load_config_file(self.filename)
        expected = {"ping_interval": 15,
                    "server": "landscape.canonical.com",
                    "something_random": "Whatever"}
        self.assertEqual(expected, result)
