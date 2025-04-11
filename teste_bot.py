import requests
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Função para enviar mensagem no Telegram
def enviar_telegram(message, token, chat_id):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.get(url, params=params)
    print(response.text)  # Exibe a resposta para verificar se deu certo
    return response

# Configurações
token_bot = os.getenv('TOKEN_BOT')
chat_id = os.getenv('CHAT_ID')
mensagem = "Teste de envio de mensagem para o bot do Telegram!"

# Envia a mensagem

enviar_telegram(mensagem, token_bot, chat_id)

