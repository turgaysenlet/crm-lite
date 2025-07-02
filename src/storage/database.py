import logging
import uuid
import time
from sqlite3 import Connection, Cursor
from typing import Optional

from pydantic import BaseModel, ConfigDict
import sqlite3
import json

from src.core.data.data_object import DataObject

logging.basicConfig()
logger = logging.getLogger("Database")
logger.setLevel(logging.DEBUG)


class DataBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)  # Apply this here

    db_name: str
    conn: Optional[Connection] = None  # Connection object
    cursor: Optional[Cursor] = None  # Cursor object

    def __init__(self, **data):
        super().__init__(**data)
        logger.info(f"Initializing database at {self.db_name}")
        self.connect()
        self.init_db_schema()

    def connect(self) -> Connection:
        try:
            self.conn = None
            self.conn = sqlite3.connect(self.db_name)
            self.conn.row_factory = sqlite3.Row  # Allows accessing columns by name
            self.cursor = self.conn.cursor()
            logger.debug(f"Connected to database: {self.db_name}")
        except sqlite3.Error as e:
            logger.error(f"Error connecting to database: {e}")
            raise
        return self.conn

    def init_db_schema(self) -> None:
        self.connect()

        # Create ObjectDefinition table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ObjectDefinition (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                api_name TEXT UNIQUE NOT NULL,
                type TEXT NOT NULL, -- 'STANDARD' or 'CUSTOM'
                description TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        ''')

        # Create FieldDefinition table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS FieldDefinition (
                id TEXT PRIMARY KEY,
                object_definition_id TEXT NOT NULL,
                name TEXT NOT NULL,
                api_name TEXT NOT NULL,
                type TEXT NOT NULL, -- 'STANDARD' or 'CUSTOM'
                data_type TEXT NOT NULL,
                is_required BOOLEAN DEFAULT 0,
                default_value TEXT,
                picklist_values TEXT, -- Stored as JSON string
                lookup_object_id TEXT,
                description TEXT,
                created_at TEXT,
                updated_at TEXT,
                FOREIGN KEY (object_definition_id) REFERENCES ObjectDefinition(id),
                FOREIGN KEY (lookup_object_id) REFERENCES ObjectDefinition(id),
                UNIQUE (object_definition_id, api_name)
            )
        ''')

        # Create Record table (for custom objects/fields)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Record (
                id TEXT PRIMARY KEY,
                object_definition_id TEXT NOT NULL,
                data TEXT, -- Stored as JSON string
                created_at TEXT,
                updated_at TEXT,
                created_by_user_id TEXT,
                updated_by_user_id TEXT,
                FOREIGN KEY (object_definition_id) REFERENCES ObjectDefinition(id)
            )
        ''')

        self.conn.commit()
        self.conn.close()

    def insert_object_definition_from_object(self, obj: DataObject):
        self.insert_object_definition(obj.name, obj.api_name, obj.obj_type, obj.description)

    def insert_object_definition(self, name, api_name, obj_type, description=None, id=None):
        """Inserts a new object definition."""
        if id is None:
            obj_id = str(uuid.uuid4())
        else:
            obj_id = id
        now = time.time()
        try:
            self.cursor.execute(
                "INSERT INTO ObjectDefinition (id, name, api_name, type, description, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (obj_id, name, api_name, obj_type, description, now, now)
            )
            self.conn.commit()
            logger.info(f"Object '{name}' ({api_name}) added successfully.")
            return obj_id
        except sqlite3.IntegrityError as e:
            logger.error(f"Error: Object with name '{name}' or api_name '{api_name}' already exists. {e}")
            return None
        except sqlite3.Error as e:
            logger.error(f"Error inserting object definition: {e}")
            return None

    def list_table(self, table_name):
        """
        Lists all records from the specified table.
        Returns a list of dictionaries, where each dictionary represents a row.
        """
        if not self.conn:
            logger.error("Database connection not established. Cannot list table.")
            return []

        try:
            query = f"SELECT * FROM {table_name}"
            logger.debug(f'Running SQL query "{query}"')
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            logger.debug(f'Received rows: "{rows}"')
            # Convert sqlite3.Row objects to dictionaries for easier handling
            return [dict(row) for row in rows]
        except sqlite3.OperationalError as e:
            logger.error(f"Error: Table '{table_name}' does not exist or SQL error. {e}")
            return []
        except sqlite3.Error as e:
            logger.error(f"Error listing table '{table_name}': {e}")
            return []
