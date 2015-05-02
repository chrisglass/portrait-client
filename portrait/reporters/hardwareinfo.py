import subprocess

from portrait.scheduler import Scheduleable
from portrait.storage.main import MainStore


class HardwareReporter(Scheduleable):
    """
    A simple plugin reporting lshw output.
    """

    scheduling_delay = 60 * 60 * 24
    thread_name = "hardware-reporter"
    run_immediately = True

    def __init__(self, config, main_storage_factory=MainStore):
        super(HardwareReporter, self).__init__(config, main_storage_factory)
        self.config = config

    def get_message(self, check_output=subprocess.check_output):
        output = check_output(["/usr/bin/lshw", "-xml", "-quiet"])
        return {"type": "hardware-info", "data": output}

    def run(self):
        message = self.get_message()
        self.main_store.pile_message(message)
