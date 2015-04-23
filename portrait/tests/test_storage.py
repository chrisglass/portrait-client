import unittest
import tempfile
import sqlite3
import os

from portrait.storage import Storage


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
        some_message = {"some_key": "some value"}
        self.storage.pile_message(some_message)

        result = self.storage.pop_all_pending_messages()
        self.assertEqual([some_message], result)

    def test_poping_a_message_marks_it_as_sent(self):
        """
        Pop_all_pending_messages removes the messages from the database.
        """
        some_message = {"some_key": "some value"}
        self.storage.pile_message(some_message)
        self.storage.pop_all_pending_messages()

        with self.storage.connection as conn:
            result = conn.execute("Select * from message_store where sent == 0")
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

    def test_get_non_existing_key(self):
        """Getting a non-existant key returns None."""
        result = self.storage.get("Nonexistant")
        self.assertIsNone(result)
