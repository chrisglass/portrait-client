import requests

from portrait.scheduler import Scheduleable


class Pinger(Scheduleable):
    """
    A "Scheduleable" Pinger that simply sends an http request to the configured
    ping server every "ping_interval" (as defined in the configuration).
    """

    thread_name = "landscape-client-pinger"

    def __init__(self, config, storage, post=requests.post):
        self.scheduling_delay = config.get("ping_interval")
        self.storage = storage
        self.ping_url = "http://%s/ping" % config.get("server")
        self.post = post

    def run(self):
        """
        This is invoked by the scheduler every ping_interval seconds.

        Ask the question: are there messages for this computer ID?
        """
        # Bail out if the insecure-id is not set. We will surely retry later.
        insecure_id = self.storage.get("insecure_id")
        if insecure_id is None:
            return

        # Make the HTP request to the ping URL.
        # It's a POST with the "insecure ID" as single post data item.
        url = self.ping_url

        # Actually perform the POST.
        result = self.post(url, data={"insecure_id": insecure_id})
        #TODO: Actually do something now that we know if there are new messages
