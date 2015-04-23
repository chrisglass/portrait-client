import threading


DEFAULT_PRIORITY = 3  # 1 is highest. That leaves room for refinement.


class Scheduleable(object):
    """
    A superclass for "modules", objects that perform a unit of work.

    Subclasses are expected to expose a run() method performing the actual work
    without taking any argument, all necessary instanciation should ideally be
    done in the subclasse's __init__.
    """

    scheduling_delay = 15  # seconds
    thread_name = "landscape-client-module"
    run_immediately = False  # Whether or not to run at daemon startup.

    def run(self):
        pass  # Should be implemented by subclasses


def run_in_thread(module):
    # Run the module in a thread.
    thread = threading.Thread(target=module.run, name=module.thread_name)
    thread.start()


def run_and_reschedule(scheduler, module):
    """
    Run a Schedulable in a thread, and reschedule it immediately.
    """
    run_in_thread(module)
    scheduler.enter(module.scheduling_delay, DEFAULT_PRIORITY,
                    action=run_and_reschedule, argument=(scheduler, module))


def initial_schedule(scheduler, module):
    """
    Schedule a module to be run after an initial delay.

    This is used as the first "bootstrap" run on service start.
    """
    if module.run_immediately:
        run_and_reschedule(module)
    else:
        scheduler.enter(module.scheduling_delay, DEFAULT_PRIORITY,
                        action=run_and_reschedule,
                        argument=(scheduler, module))
