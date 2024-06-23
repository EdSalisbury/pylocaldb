import dbm
import logging
import pickle
import threading
import traceback


class LocalDB:
    """
    A class for managing a local database using dbm with pickle serialization.

    Attributes:
        db_path (str): The path to the database file.
        db: The dbm database object.
        lock (threading.Lock): A lock for thread-safe access to the database.
        logger (logging.Logger): Logger instance for logging errors and debug messages.
    """

    def __init__(self, db_path, logger):
        """
        Initialize the LocalDB instance.

        Args:
            db_path (str): The path to the database file.
            logger (logging.Logger, optional): Logger instance for logging errors and debug messages.
                If not provided, a logger named after the current module is used.
        """
        self.db_path = db_path
        self.db = None
        self.lock = threading.Lock()
        self.logger = logger or logging.getLogger(__name__)

    def __enter__(self):
        """
        Enter method for context management. Opens the database.

        Returns:
            LocalDB: The LocalDB instance.

        Raises:
            Exception: If there's an error opening the database.
        """
        try:
            self.db = dbm.open(self.db_path, 'c')
            return self
        except Exception as e:
            self.logger.critical(f"Error opening database: {e}")
            # Log the full traceback for debugging
            self.logger.critical(traceback.format_exc())
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
                serialized_key = self._serialize(key)
                serialized_value = self.db.get(serialized_key)
                return self._deserialize(
                    serialized_value) if serialized_value else None
            except Exception as e:
                self.logger.error(f"Error loading value for {key}: {e}")
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
                self.db[serialized_key] = serialized_value
                return True
            except Exception as e:
                self.logger.error(f"Error saving value for {key}: {e}")
                return False
