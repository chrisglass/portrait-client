# The main file for landscape client.

import sched
import time

from landscape import config
from landscape.exchanger.ping import Pinger
from landscape.scheduler import initial_schedule
from landscape.storage import Storage


# TODO: This doens't quite work yet, but the intent is to show what the idea
# is. Feel free to bang on it until it works :)

EXCHANGE_MODULES = [Pinger]

scheduler = sched.scheduler(time.time, time.sleep)
config = config.load_config_file()
storage = Storage()


def start_all_modules(config, storage, scheduler):

    for module in EXCHANGE_MODULES:
        instance = module(config, storage)
        initial_schedule(scheduler, instance)


if __name__ == "__main__":
    start_all_modules(config, storage, scheduler)
    scheduler.run()
