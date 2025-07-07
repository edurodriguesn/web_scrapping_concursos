import os
from dotenv import load_dotenv
import requests

load_dotenv()

# Configurações
TOKEN_BOT = os.getenv('TOKEN_BOT')
CHAT_ID = os.getenv('CHAT_ID')

def enviar_mensagem(conteudo):
    mensagem = formatar_mensagem(conteudo)
    dispatch(mensagem)

def formatar_mensagem(conteudo):
    # Formata a mensagem para o Telegram
    mensagem_telegram = "NOVOS CONCURSOS ENCONTRADOS\n\n"
    
    for estado, links in conteudo.items():
        mensagem_telegram += f"[{estado}]\n"
        for link, data in links:
            mensagem_telegram += f"- {link}\n"
        mensagem_telegram += "\n"
    return mensagem_telegram.strip()    

def dispatch(mensagem):
    # Envia a mensagem para o Telegram
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "HTML"}
    requests.get(url, params=params)