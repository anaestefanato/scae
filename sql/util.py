import sqlite3
import os

def get_connection():
    database_path = os.environ.get('TEST_DATABASE_PATH', 'dados.db')
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection