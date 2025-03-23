import requests

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

# Teste de envio
token_bot = "7829942554:AAFuapRP-53eW0o54IOG7f3PavZr-jIH30U"
chat_id = 2081844601  # Substitua pelo seu chat_id correto
mensagem = "Teste de envio de mensagem para o bot do Telegram!"

# Envia a mensagem
enviar_telegram(mensagem, token_bot, chat_id)

