import requests

from landscape.scheduler import Scheduleable


class Pinger(Scheduleable):
    """
    A "Scheduleable" Pinger that simply sends an http request to the configured
    ping server every "ping_interval" (as defined in the configuration).
    """

    thread_name = "landscape-client-pinger"

    def __init__(self, config, storage, post=requests.post):
        self.scheduling_delay = config.get("ping_interval")
        self.ping_url = config.get("ping_url")
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
        result = self.post(url, data={"insecure_id": insecure_id})
