import requests

from portrait import SERVER_API
from portrait.lib import bpickle
from portrait.scheduler import Scheduleable


class Exchanger(Scheduleable):
    """
    A class performing the actual exchanges with the portrait server.

    The idea is that it should periodically look in the message store and send
    all unsent messages.
    """

    scheduling_delay = 120  # Run every 2 minutes?
    thread_name = "portrait-client-exchanger"

    def __init__(self, storage, config, post=requests.post):
        self.storage = storage
        self.post = post
        self.config = config

    def run(self):
        """
        Look in the message store and send any message you find!
        """
        messages = self.storage.pop_all_pending_messages()

        # Bail out immediately if there are no messages to send.
        if len(messages) == 0:
            return

        # The exchange's payload. It can contain a number of messages (not
        # just one).

        # TODO: Update sequence numbers for the case where the computer is
        # registered already.
        payload = {"server-api": SERVER_API,
                   "client-api": SERVER_API,
                   "sequence": "0",
                   "accepted-types": "",
                   "messages": messages,
                   "total-messages": len(messages),
                   "next-expected-sequence": 1}

        # The server expects the wire format to be bpickle.
        bpayload = bpickle.dumps(payload)

        headers = {"X-Message-API": SERVER_API,
                   "User-Agent": "Portrait-client DEVEL",
                   "Content-Type": "application/octet-stream"}

        # Let's perform the actual POST.
        url = "https://%s/message-system" % self.config["server_name"]
        result = self.post(url, data=bpayload, headers=headers)

        self._process_result(result)

    def _process_result(self, result):
        # The reply is a bpickle again.
        answer = bpickle.loads(result.content)

        received_messages = {
            message["type"]:message for message in answer["messages"]}

        for msgtype, message in received_messages.items():
            handler_name = "_handle_%s" % msgtype.lower().replace("-", "_")
            handler = getattr(self, handler_name)

            error_message = "Couldn't find a handler for '%s'." % msgtype
            assert handler is not None, error_message

            # Call the message handler
            handler(message)

    def _handle_set_id(self, message):
        """Handle the "set-id" messages from the server."""
        self.storage.set("secure-id", message["id"])
        self.storage.set("insecure-id", message["insecure-id"])
