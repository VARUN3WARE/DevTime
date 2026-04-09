import sqlite3
import os
from pathlib import Path

DB_FILE = Path.home() / ".devos" / "devos.db"

def get_db_path():
    """Where the magic happens (and the data stays)"""
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    return str(DB_FILE)

def init_db():
    """Sets up the graveyard for your time... just kidding, it's a database"""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()

    # Sessions: A chunk of your life spent coding
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            project TEXT
        )
    ''')

    # Events: The tiny steps of a developer
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            file TEXT,
            project TEXT,
            event_type TEXT
        )
    ''')

    # Files: Keeping track of where the bugs live
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE,
            project TEXT
        )
    ''')

    # Metrics: Precomputed stats for speed
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            metric_name TEXT,
            value REAL,
            project TEXT
        )
    ''')

    conn.commit()
    conn.close()

def execute_query(query, params=()):
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    result = cursor.fetchall()
    conn.close()
    return result
