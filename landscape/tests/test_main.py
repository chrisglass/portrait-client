import tempfile
import textwrap
import unittest

from landscape.main import load_config_file


class Maintest(unittest.TestCase):

    def test_load_config_file_works(self):
        """
        Loading the config file returns the python representation of the yaml
        contents.
        """
        contents = textwrap.dedent("""
        ping_interval: 15
        """)

        _, filename = tempfile.mkstemp()

        with open(filename, "w") as thefile:
            thefile.write(contents)

        result = load_config_file(filename)
        expected = {"ping_interval": 15}
        self.assertEqual(expected, result)
