import requests

from portrait.scheduler import Scheduleable
from portrait.storage import MainStore


class Pinger(Scheduleable):
    """
    A "Scheduleable" Pinger that simply sends an http request to the configured
    ping server every "ping_interval" (as defined in the configuration).
    """

    thread_name = "portrait-client-pinger"

    def __init__(self, config, post=requests.post,
                 main_store_factory=MainStore):
        super(Pinger, self).__init__(config, main_store_factory)

        self.scheduling_delay = config.get("ping_interval")
        self.ping_url = "http://%s/ping" % config.get("server")
        self.post = post

    def run(self):
        """
        This is invoked by the scheduler every ping_interval seconds.

        Ask the question: are there messages for this computer ID?

        The self.main_store instance variable is accessible and holds a
        MainStore instance (see portrait.storage.Scheduleable).
        """
        # Bail out if the insecure-id is not set. We will retry next run anyway
        insecure_id = self.main_store.get("insecure_id")
        if insecure_id is None:
            return

        # Make the HTTP request to the ping URL.
        # It's a POST with the "insecure ID" as single post data item.
        url = self.ping_url

        # Actually perform the POST.
        result = self.post(url, data={"insecure_id": insecure_id})
        #TODO: Actually do something now that we know if there are new messages
