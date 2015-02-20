import requests


class Pinger(object):
    """
    A simple class whose run() command is scheduled to run every run_interval,
    and that pings the landscape server with a simple HTTP post.
    """

    def __init__(self, config, scheduler, storage):
        self.ping_interval = config.ping_interval
        self.scheduler = scheduler
        self.storage = storage

    def run(self):
        """
        This is invoked by the scheduler every ping_interval seconds.

        Ask the question: are there messages for this computer ID?
        """
        # Make the HTP request to the ping URL.
        # It's a POST with the "insecure ID" as single post data item.
        insecure_id = self.storage.get("insecure_id")
        url = self.config["ping_url"]
        requests.post(url, data={"insecure_id": insecure_id})

        self.scheduler.enter(self.ping_interval, 1, self.run, ())
