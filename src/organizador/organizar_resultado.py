import sqlite3
from database.database import get_db_connection, init_db
import datetime
def ler_backup_concursos():
    """Lê os concursos salvos no banco de dados e retorna um dicionário."""
    concursos_backup = {}
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT estado, link FROM concursos")
        for estado, link in cursor.fetchall():
            if estado not in concursos_backup:
                concursos_backup[estado] = []
            concursos_backup[estado].append(link)
    
    return concursos_backup

def remover_concursos_expirados():
    """
    Remove concursos do banco cuja data de expiração já passou.
    """
    hoje = datetime.today().date()

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM concursos WHERE date(data_expiracao) < ?", (hoje.isoformat(),))
        conn.commit()

def salvar_backup_concursos(concursos):
    """Salva os concursos no banco de dados."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM concursos")

        for estado, concursos_info in concursos.items():
            for link, data_expiracao in concursos_info:
                try:
                    cursor.execute(
                        "INSERT INTO concursos (estado, link, data_expiracao) VALUES (?, ?, ?)",
                        (estado, link, data_expiracao)
                    )
                except sqlite3.IntegrityError:
                    pass

        conn.commit()

def organizar_dados(concursos_encontrados):
    """Compara os concursos encontrados com o banco e retorna os atuais e os novos."""
    init_db()

    remover_concursos_expirados()

    concursos_backup = ler_backup_concursos()

    concursos_atuais = {}
    concursos_novos = {}

    for estado, concursos_info in concursos_encontrados.items():
        concursos_atuais[estado] = concursos_info

        links_backup = set(concursos_backup.get(estado, []))  # lista de links
        links_encontrados = set(link for link, _ in concursos_info)  # só os links

        novos_links = links_encontrados - links_backup

        if novos_links:
            concursos_novos[estado] = [
                (link, data) for (link, data) in concursos_info if link in novos_links
            ]

    if concursos_novos:
        salvar_backup_concursos(concursos_atuais)

    return concursos_atuais, concursos_novos