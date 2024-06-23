# pylocaldb

pylocaldb is a lightweight Python package for managing a local database using the dbm module. It provides a simple and thread-safe interface for storing and retrieving Python objects in a local database file.

## Installation

You can install LocalDB using pip:

```bash
pip install git+https://github.com/edsalisbury/pylocaldb.git
```

## Usage

## Initialization

To initialize a pylocaldb instance, import the LocalDB class and create an instance by specifying the database path and optionally a logger:

```python
import logging
from pylocaldb import LocalDB

# Create a logger (optional)
logger = logging.getLogger(__name__)

# Initialize pylocaldb
db_path = '/path/to/your/dbfile.db'
with LocalDB(db_path, logger) as db:
    # Use the db instance
    db.save_value('key', {'value': 123})
    value = db.load_value('key')
    print(value)  # {'value': 123}
```

## Methods

### save_value(key, value)

Saves a Python object value under the specified key.

```python
db.save_value('key', {'value': 123})
```

### load_value(key)

Loads and returns the Python object stored under the specified key.

```python
value = db.load_value('key')
print(value)  # {'value': 123}
```

### Configuration

You can configure the logging level by setting the logger's level:

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
```
