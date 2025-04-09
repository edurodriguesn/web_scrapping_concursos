import sqlite3
from contextlib import contextmanager
import os
from pathlib import Path

# Caminho persistente para o banco de dados
DATABASE_PATH = Path("concursos.db")

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS concursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estado TEXT NOT NULL,
            link TEXT NOT NULL,
            UNIQUE(estado, link)
        )
        """)
        conn.commit()