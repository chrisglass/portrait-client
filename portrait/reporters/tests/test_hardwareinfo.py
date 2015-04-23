import unittest

from portrait.reporters.hardwareinfo import HardwareReporter


class HardwareReporterTest(unittest.TestCase):

    def test_get_message(self):
        """The monitor returns a correct message."""
        calls = []
        payload = "<xml>some XML</xml>"
        def faux_check_output(command):
            calls.append(command)
            return payload
        reporter = HardwareReporter({}, {})
        result = reporter.get_message(check_output=faux_check_output)

        self.assertEqual({"type": "hardware-info", "data": payload}, result)
        self.assertEqual([["/usr/bin/lshw", "-xml", "-quiet"]], calls)
