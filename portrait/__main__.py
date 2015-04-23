# The main file for portrait client.

import sched
import sys
import time
import itertools

from portrait import config
from portrait.exchanger.ping import Pinger
from portrait.exchanger.exchange import Exchanger
from portrait.exchanger.register import Registration
from portrait.reporters.hardware import HardwareReporter
from portrait.scheduler import initial_schedule
from portrait.storage import MainStore


# TODO: This doens't quite work yet, but the intent is to show what the idea
# is. Feel free to bang on it until it works :)

EXCHANGE_MODULES = [Pinger, Exchanger]

REPORTER_MODULES = [HardwareReporter]

# TODO: Make this better! The poor man's argument "parsing"
account_name = sys.argv[1]
assert account_name

config_file = sys.argv[2]
assert config_file


scheduler = sched.scheduler(time.time, time.sleep)
config = config.load_config_file(config=config_file)
#storage = Storage("test.db")

def start_all_modules(config, scheduler):
    for module in itertools.chain(EXCHANGE_MODULES, REPORTER_MODULES):
        instance = module(config)
        initial_schedule(scheduler, instance)


if __name__ == "__main__":
    registration = Registration(config)
    if registration.should_register():
        # TODO: Hook the UI for the interactive registration here
        registration.register(computer_title=config["computer_title"],
                              account_name=account_name)

    start_all_modules(config, scheduler)
    #scheduler.run()
