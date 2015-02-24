import unittest
import tempfile
import sqlite3
import os

from landscape.storage import Storage


class StubbedStorage(Storage):

    calls = []

    def _create_schema(self):
        self.calls.append(True)


class StorageTest(unittest.TestCase):

    def setUp(self):
        self.storage = Storage(":memory:")

    def test_storage_creates_schema(self):
        """
        On a default run, the database schema is created.
        """
        self.assertTrue(self.storage._is_database_initialized())

    def test_do_not_reinitialize_an_existing_db(self):
        """
        If the database pointed to with the file path has tables, do not
        create tables in it.
        """
        _, filepath = tempfile.mkstemp()
        initial_connection = sqlite3.connect(filepath)
        with initial_connection as conn:
            conn.execute("CREATE TABLE foo (id int);")
        initial_connection.close()

        storage = StubbedStorage(filepath)

        self.assertEqual([], storage.calls)
        self.assertTrue(storage._is_database_initialized())
        os.remove(filepath)

    def test_adding_message_saves_it(self):
        """
        Adding a message in the database using pile_message saves it properly.
        """
        some_message = b'Whatever'  # We expect messages to be bytes
        self.storage.pile_message(some_message)

        result = self.storage.pop_all_pending_messages()
        self.assertEqual([(1, some_message)], result)

    def test_poping_a_message_removes_it(self):
        """
        Pop_all_pending_messages removes the messages from the database.
        """
        some_message = b'Whatever'
        self.storage.pile_message(some_message)
        self.storage.pop_all_pending_messages()

        with self.storage.connection as conn:
            result = conn.execute("Select * from message_store")
            self.assertEqual([], result.fetchall())

    def test_key_values_can_be_stored_and_retreived(self):
        """
        The "documents" part of the tables can be used to store arbitrary
        key/value pairs.
        """
        key = "foo"
        value = "Something"
        self.storage.set(key, value)
        result = self.storage.get(key)
        self.assertEqual(value, result)
