import multiprocessing

from portrait.storage.main import MainStore


DEFAULT_PRIORITY = 3  # 1 is highest. That leaves room for refinement.


class Scheduleable(object):
    """
    A superclass for "modules", objects that perform a unit of work.

    Subclasses are expected to expose a run() method performing the actual work
    without taking any argument, all necessary instanciation should ideally be
    done in the subclasse's __init__.
    """

    scheduling_delay = 15  # seconds
    thread_name = "portrait-client-module"
    run_immediately = False  # Whether or not to run at daemon startup.
    main_store = None

    def __init__(self, config, main_store_factory=MainStore):
        self.config = config
        self.main_store_factory = main_store_factory

    def run_wrapper(self):
        """
        This is what the scheduler calls, and this takes care of instanciating
        a new connection to the main store (since it should be thread-local).
        """
        self._instanciate_main_store()
        self.run()

    def run(self):
        pass  # Should be implemented by subclasses

    def _instanciate_main_store(self):
        if self.main_store is None:  # If the subclass already set it, noop.
            self.main_store = self.main_store_factory(self.config)


def run_in_new_process(module):
    # Run the module in another process.
    process = multiprocessing.Process(target=module.run_wrapper,
                                     name=module.thread_name)
    process.start()

    return process


def run_and_reschedule(scheduler, module):
    """
    Run a Schedulable in a process, and reschedule it immediately.
    """
    process = run_in_new_process(module)
    scheduler.enter(module.scheduling_delay, DEFAULT_PRIORITY,
                    action=run_and_reschedule, argument=(scheduler, module))
    return process


def initial_schedule(scheduler, module):
    """
    Schedule a module to be run after an initial delay.

    This is used as the first "bootstrap" run on service start.
    """
    process = None
    if module.run_immediately:
        process = run_and_reschedule(module)
    else:
        scheduler.enter(module.scheduling_delay, DEFAULT_PRIORITY,
                        action=run_and_reschedule,
                        argument=(scheduler, module))
    return process
