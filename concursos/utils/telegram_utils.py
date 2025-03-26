# concursos/utils/telegram_utils.py
import requests
from django.conf import settings

def enviar_telegram(mensagem):
    """Envia mensagem para o Telegram."""
    config = settings.CONCURSOS_CONFIG
    url = f"https://api.telegram.org/bot{config['TOKEN_BOT']}/sendMessage"
    params = {"chat_id": config['CHAT_ID'], "text": mensagem, "parse_mode": "HTML"}
    requests.get(url, params=params)