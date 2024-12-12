import dbm
import sqlite3
import logging
import pickle
import threading
import traceback

logger = logging.getLogger(__name__)


class LocalDB:
    """
    A class for managing a local database using either dbm with pickle serialization
    or SQLite3.
    """

    def __init__(self, db_path, db_type="dbm"):
        """
        Initialize the LocalDB instance.

        Args:
            db_path (str): The path to the database file.
            db_type (str): Type of the database ('dbm' or 'sqlite3').
        """
        self.db_path = db_path
        self.db_type = db_type
        self.db = None
        self.lock = threading.Lock()

    def __enter__(self):
        """
        Enter method for context management. Opens the database based on the db_type.

        Returns:
            LocalDB: The LocalDB instance.

        Raises:
            Exception: If there's an error opening the database.
        """
        try:
            if self.db_type == "dbm":
                self.db = dbm.open(self.db_path, "c")
            elif self.db_type == "sqlite3":
                self.db = sqlite3.connect(self.db_path)
                self._create_sqlite_table()
            else:
                raise ValueError("Unsupported db_type. Use 'dbm' or 'sqlite3'.")
            return self
        except Exception as e:
            logger.critical(f"Error opening database: {e}")
            # Log the full traceback for debugging
            logger.critical(traceback.format_exc())
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit method for context management. Closes the database.

        Args:
            exc_type: Exception type.
            exc_val: Exception value.
            exc_tb: Exception traceback.
        """
        if self.db is not None:
            if self.db_type == "dbm":
                self.db.close()
            elif self.db_type == "sqlite3":
                self.db.commit()
                self.db.close()
            self.db = None  # Reset the database object after closing

    def _serialize(self, value):
        """
        Serialize a Python object using pickle.

        Args:
            value: The object to serialize.

        Returns:
            bytes: The serialized object.
        """
        return pickle.dumps(value)

    def _deserialize(self, value):
        """
        Deserialize a pickle-serialized object.

        Args:
            value (bytes): The serialized object.

        Returns:
            object: The deserialized Python object.
        """
        return pickle.loads(value)

    def _create_sqlite_table(self):
        """
        Creates the necessary table for SQLite if it doesn't exist.
        """
        cursor = self.db.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS data (
                key TEXT PRIMARY KEY,
                value BLOB
            )
        """
        )
        self.db.commit()

    def load_value(self, key):
        """
        Load a value from the database given a key.

        Args:
            key: The key to retrieve the value.

        Returns:
            object: The deserialized value associated with the key, or None if not found.

        Raises:
            Exception: If there's an error loading the value.
        """
        with self.lock:
            try:
                if self.db_type == "dbm":
                    serialized_key = self._serialize(key)
                    serialized_value = self.db.get(serialized_key)
                    return (
                        self._deserialize(serialized_value)
                        if serialized_value
                        else None
                    )

                elif self.db_type == "sqlite3":
                    cursor = self.db.cursor()
                    cursor.execute("SELECT value FROM data WHERE key = ?", (key,))
                    result = cursor.fetchone()
                    if result:
                        return self._deserialize(result[0])
                    return None

            except Exception as e:
                logger.error(f"Error loading value for {key}: {e}")
                return None

    def save_value(self, key, value):
        """
        Save a value into the database with a given key.

        Args:
            key: The key under which to save the value.
            value: The value to save.

        Returns:
            bool: True if the value was saved successfully, False otherwise.

        Raises:
            Exception: If there's an error saving the value.
        """
        with self.lock:
            try:
                serialized_key = self._serialize(key)
                serialized_value = self._serialize(value)

                if self.db_type == "dbm":
                    self.db[serialized_key] = serialized_value
                elif self.db_type == "sqlite3":
                    cursor = self.db.cursor()
                    cursor.execute(
                        "INSERT OR REPLACE INTO data (key, value) VALUES (?, ?)",
                        (key, serialized_value),
                    )
                    self.db.commit()

                return True

            except Exception as e:
                logger.error(f"Error saving value for {key}: {e}")
                return False
