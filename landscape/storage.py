import json
import sqlite3


DEFAULT_LANDSCAPE_DB_PATH = ""


class Storage(object):
    """
    A simple key-value store built on top of squite3.

    Since the database connection is thread-safe (as per the docs) we can
    assume this class is as well (being a simple, thin layer on top of it).
    """

    def __init__(self, database_path):
        self.database_path = database_path
        # Connect to the squite3 database at the specified path
        self.connection = sqlite3.connect(self.database_path)

        # If there are no tables in the database, create the schema:
        if not self._is_database_initialized():
            self._create_schema()

    def _is_database_initialized(self):
        results = []
        with self.connection as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table';")
            results = cursor.fetchall()
        return len(results) > 0

    def _create_schema(self):
        with self.connection as conn:
            conn.execute(
                "CREATE TABLE message_store "
                "    (id integer primary key,"
                "     message varchar,"
                "     sent bool default (0))")
            conn.execute(
                "CREATE TABLE documents "
                    "(key varchar unique, value varchar)")

    def pile_message(self, message):
        """
        Add a message to the message store to be sent to the server at next
        exchange.

        @param message; A dict representing the message to send. It will be
            serialized before being inserted in the DB.
        """
        serialized = json.dumps(message)
        with self.connection as conn:
            conn.execute("INSERT INTO message_store(message) VALUES (?)",
                         (serialized,))

    def pop_all_pending_messages(self):
        """
        Get a list of message to be set to the server, then remove them from
        the store.

        @return The dict representation of the message, deserialized from the
            DB.
        """
        results = []
        with self.connection as conn:
            cursor = conn.execute("SELECT id, message FROM message_store WHERE sent == 0")
            results = cursor.fetchall()
            ids = [str(row[0]) for row in results]
            id_list = ", ".join(ids)
            conn.execute("UPDATE message_store SET sent=1 where id IN (?)",
                         (id_list,))
        results = [json.loads(row[1]) for row in results]
        return results

    def set(self, key, value):
        """
        Persist a key/value pair in the database.
        """
        with self.connection as conn:
            conn.execute("INSERT INTO documents(key, value) VALUES (?, ?)",
                         (key, value,))

    def get(self, key):
        """
        Retreive the value matching a given key from the database.
        """
        with self.connection as conn:
            cursor = conn.execute(
                "SELECT value FROM documents WHERE key == ?", (key,))
            result = cursor.fetchone()
            if result:
                result = result[0]  # The result is wrapped in a tuple
            return result
