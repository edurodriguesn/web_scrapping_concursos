import os
from dotenv import load_dotenv
import requests

load_dotenv()

# Configurações
TOKEN_BOT = os.getenv('TOKEN_BOT')
CHAT_ID = os.getenv('CHAT_ID')

def formatar_mensagem(concursos_novos):
    # Formata a mensagem para o Telegram
    mensagem_telegram = "NOVOS CONCURSOS ENCONTRADOS\n\n"
    
    for estado, links in concursos_novos.items():
        mensagem_telegram += f"[{estado}]\n"
        for link, data in links:
            mensagem_telegram += f"- {link}\n"
        mensagem_telegram += "\n"
    return mensagem_telegram.strip()

def enviar_telegram(mensagem):
    # Envia a mensagem para o Telegram
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "HTML"}
    requests.get(url, params=params)