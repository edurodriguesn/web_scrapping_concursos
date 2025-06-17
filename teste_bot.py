import requests
import os

def enviar_telegram(message, token, chat_id):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.get(url, params=params)
    print(response.text)  # Exibe a resposta para verificar se deu certo
    return response

# Pegando as variáveis do ambiente (funciona tanto no local quanto no GitHub Actions)
token_bot = os.getenv('TOKEN_BOT')
chat_id = os.getenv('CHAT_ID')
mensagem = "Teste de envio de mensagem para o bot do Telegram!"

# Debug opcional
print(f"TOKEN_BOT: {token_bot}")
print(f"CHAT_ID: {chat_id}")

# Envia a mensagem
enviar_telegram(mensagem, token_bot, chat_id)
