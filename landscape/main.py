# The main file for landscape client.

import sched
import time

from landscape import config


scheduler = sched.scheduler(time.time, time.sleep)


if __name__ == "__main__":
    config = config.load_config_file()
    scheduler.run()
