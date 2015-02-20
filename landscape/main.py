# The main file for landscape client.

import sched
import time


scheduler = sched.sheduler(time.time, time.sleep)


def setup_first_events():
    scheduler.enter(1, 1, setup_monitor_plugins, ())
    scheduler.enter(1, 1, setup_manager_plugins, ())


if __name__ == "__main__":
    scheduler.run()
