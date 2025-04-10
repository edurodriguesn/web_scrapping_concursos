import requests
import os


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
TOKEN_BOT = os.getenv('TOKEN_BOT')
CHAT_ID = os.getenv('CHAT_ID')
mensagem = "Teste de envio de mensagem para o bot do Telegram!"

# Envia a mensagem
enviar_telegram(mensagem, token_bot, chat_id)

