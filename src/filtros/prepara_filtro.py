# filtros/filtros_db.py

from database.database import get_db_connection, init_db, obter_urls_processadas, adicionar_url_processada
from datetime import datetime
from utils.data import extrair_data

def remover_concursos_expirados_html(concursos_html):
    """
    Remove elementos do HTML cuja data esteja ausente, inválida ou expirada.
    Adiciona todas as URLs processadas à lista de URLs processadas.

    :param concursos_html: Lista de elementos <div> do BeautifulSoup.
    :return: Lista filtrada.
    """
    concursos_validos = []
    hoje = datetime.today().date()

    for concurso_div in concursos_html:
        link = concurso_div.get("data-url")
        data_ce = concurso_div.find("div", class_="ce")
        if not data_ce:
            if link:
                adicionar_url_processada(link)
            continue

        span = data_ce.find("span")
        if not span:
            if link:
                adicionar_url_processada(link)
            continue

        span_text = span.get_text(strip=True)
        if not span_text:
            if link:
                adicionar_url_processada(link)
            continue

        data = extrair_data(span_text)
        if not data:
            if link:
                adicionar_url_processada(link)
            continue

        if data.date() >= hoje:
            concursos_validos.append(concurso_div)
            # Adiciona URLs válidas à lista de processadas
            if link:
                adicionar_url_processada(link)
        else:
            if link:
                adicionar_url_processada(link)

    return concursos_validos

def remover_urls_ja_processadas(concursos_html):
    """
    Remove elementos do HTML cuja URL já foi processada anteriormente.
    
    :param concursos_html: Lista de elementos <div> do BeautifulSoup.
    :return: Lista filtrada de elementos <div>.
    """
    init_db()
    urls_processadas = obter_urls_processadas()
    
    concursos_filtrados = []

    for concurso_div in concursos_html:
        link = concurso_div.get("data-url")
        if not link:
            continue
        if link not in urls_processadas:
            concursos_filtrados.append(concurso_div)

    return concursos_filtrados
