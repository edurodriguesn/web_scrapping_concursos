import requests
from bs4 import BeautifulSoup

# URL principal dos concursos
URL_BASE = "https://www.pciconcursos.com.br/concursos/"

def obter_concursos():
    """Obtém a lista de concursos a partir do site."""
    response = requests.get(URL_BASE)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find_all("div", class_=["na", "da", "ea"])

def obter_detalhes_concurso(link):
    """Obtém os detalhes do concurso a partir do link fornecido."""
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    detalhe_div = soup.find("article", id="noticia")
    
    if detalhe_div:
        return detalhe_div.get_text(strip=True).lower()
    return ""
