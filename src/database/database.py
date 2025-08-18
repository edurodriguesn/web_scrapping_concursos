import sqlite3
from contextlib import contextmanager
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

# database.database.py
def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS concursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estado TEXT NOT NULL,
            link TEXT NOT NULL,
            data_expiracao TEXT NOT NULL,
            UNIQUE(estado, link)
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls_processadas (
            link TEXT PRIMARY KEY
        )
        """)
        conn.commit()

def adicionar_url_processada(link):
    """Adiciona uma URL à lista de URLs já processadas."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO urls_processadas (link) VALUES (?)", (link,))
            conn.commit()
        except sqlite3.IntegrityError:
            # URL já existe na lista
            pass

def obter_urls_processadas():
    """Retorna um conjunto com todas as URLs já processadas."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT link FROM urls_processadas")
        return set(row[0] for row in cursor.fetchall())