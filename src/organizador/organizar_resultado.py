import sqlite3
from database.database import get_db_connection, init_db
from datetime import datetime
def ler_backup_concursos():
    """Lê os concursos salvos no banco de dados e retorna um dicionário."""
    concursos_backup = {}
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT estado, link, data_expiracao FROM concursos")
        for estado, link, data_expiracao in cursor.fetchall():
            if estado not in concursos_backup:
                concursos_backup[estado] = []
            concursos_backup[estado].append((link, data_expiracao))
    
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
        
        for estado, concursos_info in concursos.items():
            for link, data_expiracao in concursos_info:
                try:
                    cursor.execute(
                        "INSERT OR REPLACE INTO concursos (estado, link, data_expiracao) VALUES (?, ?, ?)",
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

        links_backup = set(link for link, _ in concursos_backup.get(estado, []))  # lista de links
        links_encontrados = set(link for link, _ in concursos_info)  # só os links

        novos_links = links_encontrados - links_backup

        if novos_links:
            concursos_novos[estado] = [
                (link, data) for (link, data) in concursos_info if link in novos_links
            ]

    if concursos_novos:
        # Combinar concursos existentes com os novos encontrados
        todos_concursos = {}
        
        # Primeiro, adicionar todos os concursos existentes no banco
        for estado, concursos_existentes in concursos_backup.items():
            todos_concursos[estado] = concursos_existentes.copy()
        
        # Depois, adicionar os novos concursos encontrados
        for estado, concursos_info in concursos_encontrados.items():
            if estado not in todos_concursos:
                todos_concursos[estado] = []
            
            # Adicionar apenas os novos concursos (que não existem no backup)
            for link, data_expiracao in concursos_info:
                if not any(existing_link == link for existing_link, _ in todos_concursos[estado]):
                    todos_concursos[estado].append((link, data_expiracao))
        
        salvar_backup_concursos(todos_concursos)

    return concursos_atuais, concursos_novos