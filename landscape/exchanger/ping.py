import requests


class Pinger(object):
    """
    A simple class whose run() command is scheduled to run every run_interval,
    and that pings the landscape server with a simple HTTP post.
    """

    def __init__(self, config, scheduler, storage, post=requests.post):
        self.ping_interval = config.get("ping_interval")
        self.ping_url = config.get("ping_url")
        self.scheduler = scheduler
        self.insecure_id = storage.get("insecure_id")
        self.post = post

    def run(self):
        """
        This is invoked by the scheduler every ping_interval seconds.

        Ask the question: are there messages for this computer ID?
        """
        # Make the HTP request to the ping URL.
        # It's a POST with the "insecure ID" as single post data item.
        insecure_id = self.insecure_id
        url = self.ping_url

        # Actually perform the POST.
        self.post(url, data={"insecure_id": insecure_id})

        self.scheduler.enter(self.ping_interval, 1, self.run, ())
