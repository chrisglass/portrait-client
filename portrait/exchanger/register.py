import time

from portrait import SERVER_API

from portrait.exchanger.exchange import Exchanger
from portrait.storage.main import MainStore


class Registration(object):
    """
    This class handles the registration logic.
    """

    def __init__(self, config, main_store_factory=MainStore):
        self.main_store = main_store_factory(config)
        self.config = config

    def should_register(self):
        """
        Determine whether this computer should register with the landscape
        server or not.
        """
        stored_id = self.main_store.get("secure-id")
        return not bool(stored_id)

    def register(self, computer_title, account_name, registration_password="",
                 tags="", access_group="", exchanger_factory=Exchanger):
        """
        Send a registration message to the landscape server, and save the
        answer's content in the main storage.

        This is done in-thread because without registration nothing works.
        """
        # The message is built.
        message_header = {"type": "register",
                          "api": SERVER_API,
                          "timestamp": time.time()}

        # The registration message itself.
        registration = {"account_name": account_name,
                        "computer_title": computer_title}
        if registration_password:
            registration.update(
                {"registration_password": registration_password})
        if tags:
            registration.update({"tags": tags})
        if access_group:
            registration.update({"access_group": access_group})

        # Building the actual message now, by fusing both dicts above.
        message = {}
        message.update(registration)
        message.update(message_header)

        # Let's add the message to the message store.
        self.main_store.pile_message(message)

        # We would normally wait for the exchanger to be scheduled, but it
        # is not worth it to wait for anything if we're not registered, so
        # let's just run in-thread:
        exchange = exchanger_factory(self.config, main_store=self.main_store)
        exchange.run()
