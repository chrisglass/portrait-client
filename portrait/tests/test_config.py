import os
import tempfile
import textwrap
import unittest

from portrait.config import load_config_file, DEFAULTS


class Maintest(unittest.TestCase):

    def setUp(self):
        _, self.filename = tempfile.mkstemp()

    def tearDown(self):
        os.remove(self.filename)

    def test_load_config_file_works(self):
        """
        Loading the config file returns the python representation of the INI
        contents.
        """
        contents = textwrap.dedent("""
        [portrait]
        ping_interval = 30
        server = example.com
        """)

        with open(self.filename, "w") as thefile:
            thefile.write(contents)

        result = load_config_file(self.filename, use_defaults=False)
        expected = {"ping_interval": "30", "server": "example.com"}
        self.assertEqual(expected, result)

    def test_empty_file_loads_defaults(self):
        """
        If the configuration file exists but is empty or contains other keys,
        the defaults are used/loaded.
        """
        contents = textwrap.dedent("""
        [portrait]
        something_random = Whatever
        """)

        with open(self.filename, "w") as thefile:
            thefile.write(contents)

        result = load_config_file(self.filename)
        expected = {}
        expected.update(DEFAULTS)
        expected.update({"something_random": "Whatever"})
        self.assertEqual(expected, result)
