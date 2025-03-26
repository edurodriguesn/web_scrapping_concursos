# concursos/scrapers/base_scraper.py
from django.conf import settings
import requests
from bs4 import BeautifulSoup

class BaseScraper:
	def __init__(self):
		self.config = settings.CONCURSOS_CONFIG
	def get_soup(self, url):
		response = requests.get(url)
		return BeautifulSoup(response.text, "html.parser")
	def normalize_text(self, text):
		import unicodedata
		return ''.join(
			c for c in unicodedata.normalize('NFD', text) 
			if unicodedata.category(c) != 'Mn'
		).lower()