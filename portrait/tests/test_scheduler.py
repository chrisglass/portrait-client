import os
import sched
import tempfile
import time
import unittest


from portrait.scheduler import Scheduleable, run_and_reschedule
from portrait.scheduler import run_in_new_process
from portrait.storage import MainStore

TEST_MESSAGE = {"type": "test", "something": "whatever"}

class MutatingScheduleable(Scheduleable):
    """A schedulable that puts a message in the main storage when run,
    and mutates instance state (the configuration, specifically)."""

    def __init__(self, config):
        super(MutatingScheduleable, self).__init__(config)
        self.config["thekey"] = 1

    def run(self):
        self.config["thekey"] = 5
        self.main_store.pile_message(TEST_MESSAGE)


class SchedulerTest(unittest.TestCase):

    def test_run_in_another_process(self):
        """
        The run_in_new_process function make sa given module run in a new
        process.
        """
        _, filepath = tempfile.mkstemp()
        self.addCleanup(os.remove, filepath)

        config = {"main_store": filepath}

        the_module = MutatingScheduleable(config)
        process = run_in_new_process(the_module)
        process.join()

        storage = MainStore(config)
        messages = storage.pop_all_pending_messages()

        self.assertEqual([TEST_MESSAGE], messages)

    def test_schedulable_dont_mutate_instance_state(self):
        """
        A module from this process will be passed to a new process via the
        scheduling functions, and we make sure it can't mutate the state from
        the main process's instance.
        """
        config = {"main_store": ":memory:"}
        the_module = MutatingScheduleable(config)
        process = run_in_new_process(the_module)
        process.join()
        self.assertEqual(1, the_module.config["thekey"])

    def test_re_schedule_module(self):
        """
        Running a module means its exectution is offloaded to a thread, and
        it is rescheduled after module.scheduling_delay has elapsed.
        """
        scheduler = sched.scheduler(time.time, time.sleep)
        config = {"main_store": ":memory:"}
        the_module = MutatingScheduleable(config)
        process = run_and_reschedule(scheduler, the_module)
        process.join()

        #NOTE: it might be worth it to look better into how to assert what we
        # scheduled is really what we expect.
        self.assertEqual(1, len(scheduler.queue))
