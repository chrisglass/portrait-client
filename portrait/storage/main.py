import json
import sqlite3


DEFAULT_PORTRAIT_DB_PATH = "/var/lib/portrait/main_store.db"


class SQLiteStorage(object):

    schema = ""
    config_database_path = ""

    def __init__(self, config):
        database_path = config.get(self.config_database_path)
        assert database_path is not None

        self.database_path = database_path
        # Connect to the squite3 database at the specified path
        self.connection = sqlite3.connect(self.database_path)

        # If there are no tables in the database, create the schema:
        if not self._is_database_initialized():
            self._create_schema()

    def _create_schema(self):
        with self.connection as conn:
            for statement in self.schema:
                conn.execute(statement)

    def _is_database_initialized(self):
        results = []
        with self.connection as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table';")
            results = cursor.fetchall()
        return len(results) > 0


class MainStore(SQLiteStorage):
    """
    A simple key-value store built on top of squite3.

    Each process/thread in the client should instanciate its own copy of the
    Storage object, as this will in turn create it's own thread-local
    sqlite3.Connection object, and therefore pass all locking/concurrency
    solving to the underlying database.
    """
    config_database_path = "main_store"

    schema = ["""CREATE TABLE message_store
                    (id integer primary key,
                     message varchar,
                     sent bool default (0))"""]

    def pile_message(self, message):
        """
        Add a message to the message store to be sent to the server at next
        exchange.

        @param message; A dict representing the message to send. It will be
            serialized before being inserted in the DB.
        """
        serialized = json.dumps(message, separators=(",", ":"))
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
            cursor = conn.execute("SELECT id, message FROM message_store"
                                  " WHERE sent == 0")
            results = cursor.fetchall()
            ids = [str(row[0]) for row in results]
            id_list = ", ".join(ids)
            conn.execute("UPDATE message_store SET sent=1 where id IN (?)",
                         (id_list,))
        results = [json.loads(row[1]) for row in results]
        return results


class ExchangeStore(SQLiteStorage):

    config_database_path = "exchange_store"

    schema = ["""CREATE TABLE documents
                    (key varchar unique, value varchar)"""]

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
