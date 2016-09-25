

class IdHandler(object):
    """
    A handler for the computer ID message type.
    """
    message_type = "set-id"

    def __init__(self, config, main_storage):
        self.storage = main_storage

    def handle(self, message):
        self.storage.set("secure-id", message["id"])
        self.main_store.set("insecure-id", message["insecure-id"])
