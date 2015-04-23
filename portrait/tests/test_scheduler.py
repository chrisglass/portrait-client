import sched
import time
import unittest


from portrait.scheduler import Scheduleable, run_and_reschedule


class SchedulerTest(unittest.TestCase):

    def test_re_schedule_module(self):
        """
        Running a module means its exectution is offloaded to a thread, and
        it is rescheduled after module.scheduling_delay has elapsed.
        """
        scheduler = sched.scheduler(time.time, time.sleep)
        module = Scheduleable()

        run_and_reschedule(scheduler, module)

    def test_write_some(self):
        self.fail("Write tests!")
