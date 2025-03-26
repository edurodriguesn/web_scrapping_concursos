# concursos/scrapers/pci_scraper.py
from .base_scraper import BaseScraper
from datetime import datetime

class PCIConcursosScraper(BaseScraper):
    def obter_concursos(self):
        """Obtém a lista de concursos a partir do site."""
        soup = self.get_soup(self.config['URL_BASE_PCI'])
        return soup.find_all("div", class_=["na", "da", "ea"])
    
    def obter_detalhes_concurso(self, link):
        """Obtém os detalhes do concurso a partir do link fornecido."""
        soup = self.get_soup(link)
        detalhe_div = soup.find("article", id="noticia")
        return self.normalize_text(detalhe_div.get_text(strip=True)) if detalhe_div else ""
    
    def extrair_data(self, texto):
        while texto and not texto[-1].isdigit():
            texto = texto[:-1]
        for i in range(len(texto) - 10, -1, -1):
            data_tentativa = texto[i:i+10]
            if data_tentativa.count("/") == 2:
                try:
                    return datetime.strptime(data_tentativa, "%d/%m/%Y")
                except ValueError:
                    continue
        return None