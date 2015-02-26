# The main file for landscape client.

import sched
import sys
import time

from landscape import config
from landscape.exchanger.ping import Pinger
from landscape.exchanger.register import Registration
from landscape.scheduler import initial_schedule
from landscape.storage import Storage


# TODO: This doens't quite work yet, but the intent is to show what the idea
# is. Feel free to bang on it until it works :)

EXCHANGE_MODULES = [Pinger]

# TODO: Make this better! The poor man's argument "parsing"
account_name = sys.argv[1]
assert account_name

config_file = sys.argv[2]
assert config_file


scheduler = sched.scheduler(time.time, time.sleep)
config = config.load_config_file(config=config_file)
storage = Storage("test.db")

def start_all_modules(config, storage, scheduler):

    for module in EXCHANGE_MODULES:
        instance = module(config, storage)
        initial_schedule(scheduler, instance)


if __name__ == "__main__":
    registration = Registration(storage, config)
    if registration.should_register():
        # TODO: Hook the UI for the interactive registration here
        registration.register(computer_title=config["computer_title"],
                              account_name=account_name)

    start_all_modules(config, storage, scheduler)
    #scheduler.run()
