import sqlite3
from database.database import get_db_connection, init_db

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


def salvar_backup_concursos(concursos):
    """Salva os concursos no banco de dados."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Limpa a tabela antes de inserir novos dados (opcional)
        cursor.execute("DELETE FROM concursos")
        
        for estado, links in concursos.items():
            for link in links:
                try:
                    cursor.execute(
                        "INSERT INTO concursos (estado, link) VALUES (?, ?)",
                        (estado, link)
                    )
                except sqlite3.IntegrityError:
                    # Ignora duplicatas (devido à constraint UNIQUE)
                    pass
        
        conn.commit()


def organizar_dados(concursos_encontrados):
    """Compara os concursos encontrados com o banco e retorna os atuais e os novos."""
    init_db()
    concursos_backup = ler_backup_concursos()
    
    concursos_atuais = {}
    concursos_novos = {}

    for estado, links in concursos_encontrados.items():
        concursos_atuais[estado] = links
        
        # Identificar os novos
        links_backup = set(concursos_backup.get(estado, []))
        links_encontrados = set(links)
        novos_links = links_encontrados - links_backup
        
        if novos_links:
            concursos_novos[estado] = list(novos_links)

    # Atualiza o banco de dados apenas se houver alterações
    if concursos_novos:
        salvar_backup_concursos(concursos_atuais)

    return concursos_atuais, concursos_novos