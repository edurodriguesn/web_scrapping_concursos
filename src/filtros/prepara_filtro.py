# filtros/filtros_db.py

from database.database import get_db_connection, init_db
from datetime import datetime
from utils.data import extrair_data

def remover_concursos_expirados_html(concursos_html):
    """
    Remove elementos do HTML cuja data esteja ausente, inválida ou expirada.

    :param concursos_html: Lista de elementos <div> do BeautifulSoup.
    :return: Lista filtrada.
    """
    concursos_validos = []
    hoje = datetime.today().date()

    for concurso_div in concursos_html:
        data_ce = concurso_div.find("div", class_="ce")
        if not data_ce:
            continue

        span = data_ce.find("span")
        if not span:
            continue

        span_text = span.get_text(strip=True)
        if not span_text:
            continue

        data = extrair_data(span_text)
        if not data:
            continue

        if data.date() >= hoje:
            concursos_validos.append(concurso_div)

    return concursos_validos

def remover_concursos_existentes(concursos_html):
    """
    Remove elementos do HTML cuja URL (data-url) já existe no banco de dados.
    
    :param concursos_html: Lista de elementos <div> do BeautifulSoup.
    :return: Lista filtrada de elementos <div>.
    """
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT link FROM concursos")
        links_existentes = set(row[0] for row in cursor.fetchall())

    concursos_filtrados = []

    for concurso_div in concursos_html:
        link = concurso_div.get("data-url")
        if not link:
            continue
        if link not in links_existentes:    
            concursos_filtrados.append(concurso_div)

    return concursos_filtrados
