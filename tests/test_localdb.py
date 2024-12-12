import logging
import os
import pickle
import tempfile
from unittest.mock import patch
import unittest

from localdb.localdb import LocalDB


class TestLocalDB(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, 'test.db')
        self.logger = logging.getLogger('test_logger')
        self.local_db = LocalDB(self.db_path)

    def tearDown(self):
        self.local_db.__exit__(None, None, None)  # Ensure database is closed
        self.temp_dir.cleanup()  # Clean up temporary directory

    def test_open_close_database(self):
        with self.local_db as db:
            self.assertIsNotNone(db.db)
        self.assertIsNone(db.db)

    def test_save_load_value(self):
        key = 'test_key'
        value = {'test': 'value'}

        with self.local_db as db:
            db.save_value(key, value)
            loaded_value = db.load_value(key)
            self.assertEqual(loaded_value, value)

    def test_load_nonexistent_key(self):
        key = 'nonexistent_key'

        with self.local_db as db:
            loaded_value = db.load_value(key)
            self.assertIsNone(loaded_value)

    def test_load_value_exception_handling(self):
        self.logger.disabled = True
        with LocalDB(self.db_path, self.logger) as db:
            # Simulate an error by providing an invalid key type
            with patch.object(db, '_serialize', side_effect=pickle.PickleError("Mocked PickleError")):
                value = db.load_value(12345)  # Provide an integer key
                self.assertIsNone(value)
        self.logger.disabled = False

    def test_save_value_exception_handling(self):
        self.logger.disabled = True
        with LocalDB(self.db_path, self.logger) as db:
            # Simulate an error by providing a non-serializable value
            with patch.object(db, '_serialize', side_effect=pickle.PickleError("Mocked PickleError")):
                # Attempt to save a lambda function
                success = db.save_value('key', lambda x: x)
                self.assertFalse(success)
        self.logger.disabled = False

    def test_init_exception_handling(self):
        invalid_db_path = '/invalid/path/to/db'
        self.logger.disabled = True  # Disable logging for exception
        with self.assertRaises(Exception):
            with LocalDB(invalid_db_path, self.logger):
                pass
        self.logger.disabled = False


if __name__ == '__main__':
    unittest.main()
