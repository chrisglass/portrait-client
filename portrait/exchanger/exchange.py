import requests

from portrait import SERVER_API
from portrait.lib import bpickle
from portrait.scheduler import Scheduleable
from portrait.storage import MainStore


class Exchanger(Scheduleable):
    """
    A class performing the actual exchanges with the portrait server.

    The idea is that it should periodically look in the message store and send
    all unsent messages.

    Sending the message requires to know a few things from teh server
    """

    scheduling_delay = 120  # Run every 2 minutes?
    thread_name = "portrait-client-exchanger"

    def __init__(self, config, post=requests.post, main_store=None,
                 main_store_factory=MainStore):
        super(Exchanger, self).__init__(config, main_store_factory)

        # For the registration message, we are passed the main_store to use
        # directly since it's run in-thread/process.
        if main_store is not None:
            self.main_store = main_store

        self.post = post
        self.config = config

    def run(self):
        """
        Look in the message store and send any message you find!
        """
        messages = self.main_store.pop_all_pending_messages()

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

        # If we have a next expected token in the store, send it to the server.
        exchange_token = self.main_store.get("next-expected-token")
        if exchange_token is not None:
            headers.update({"X-Exchange-Token": exchange_token})

        # Let's perform the actual POST.
        url = "https://%s/message-system" % self.config["server_name"]
        result = self.post(url, data=bpayload, headers=headers)

        self._process_result(result)

    def _process_result(self, result):
        # The reply is a bpickle again.
        answer = bpickle.loads(result.content)

        #TODO: Set next expected sequence if received

        #Set next expected token if received.
        next_expected_token = answer.get("next-expected-token")
        if next_expected_token is not None:
            self.main_store.set("next-expected-token", next_expected_token)

        #Set server uuid if received.
        server_uuid = answer.get("server-uuid")
        if server_uuid is not None:
            self.main_store.set("server-uuid", server_uuid)

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
        self.main_store.set("secure-id", message["id"])
        self.main_store.set("insecure-id", message["insecure-id"])
