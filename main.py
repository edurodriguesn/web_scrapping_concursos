import scraper
import organizar_resultado as organizador
import requests
import re
from datetime import datetime, timedelta

# Configurações
ARQUIVO_BACKUP = "concursos_backup.txt"
TOKEN_BOT = "7829942554:AAFuapRP-53eW0o54IOG7f3PavZr-jIH30U"
CHAT_ID = 2081844601

ESTADOS_INTERESSE = ["AP", "SC", "PA", "PR", "NACIONAL"]
CARGOS_TI = [
    "tecnologia da informação", "informática", "sistema", "computação", "desenvolvimento", "desenvolvedor",
    "segurança da informação", "banco de dados", "redes", "suporte técnico", "programação", "programador"
    "engenharia de software", "arquitetura de software", "infraestrutura de ti", "suporte de ti"
    "analista de ti", "cientista de dados", "inteligência artificial", "ciência de dados", "aprendizado de máquina",
    "governança de ti", "gestão de projetos de ti", "gestão de riscos de ti",
    "computação em nuvem", "forense digital", "big data", "automação", "devops"
]
TERMOS_EXCLUIR = [
    "informática básica", "noções de informática", "informática para iniciantes", "conceitos de informática", 
    "conhecimentos em informática", "cursos de informática", ", informática", "informática nível básico", 
    "informática nível iniciante", "informática fundamental", "nível básico em informática",
    "básico em informática", "básico de informática", "básicos em informática", "básicos de informática", 
    "iniciante em informática", "iniciante de informática"
]

# Função para enviar mensagem no Telegram
def enviar_telegram(mensagem):
    """Envia mensagem para o Telegram."""
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "HTML"}
    requests.get(url, params=params)

def extrair_data(texto):
    while texto and not texto[-1].isdigit():
        texto = texto[:-1]
    for i in range(len(texto) - 10, -1, -1):  # i vai de len(texto) - 10 até 0
        data_tentativa = texto[i:i+10]  # Extrai 10 caracteres a partir de i
        if data_tentativa.count("/") == 2:  # Verifica se contém duas barras (formato dd/mm/yyyy)
            try:
                # Tenta converter para data
                print(data_tentativa)
                return datetime.strptime(data_tentativa, "%d/%m/%Y")
            except ValueError:
                continue  # Se a conversão falhar, tenta a próxima sequência
    return None 

def main():
    # Lê os concursos antigos
    concursos_antigos = organizador.ler_backup_concursos(ARQUIVO_BACKUP)
    novos_concursos = set()
    mensagem = ""

    # Obtém os concursos
    concursos = scraper.obter_concursos()

    for concurso in concursos:
        div_cc = concurso.find("div", class_="cc")
        data_concurso = concurso.find("div", class_="ce")
        span_text = data_concurso.find("span").get_text(strip=True)
        
        if "Suspenso" in span_text or "Cancelado" in span_text:
            continue

        data_concurso = extrair_data(span_text)
        hoje = datetime.today()

        if div_cc:
            estado = div_cc.get_text(strip=True) or "NACIONAL"
            if estado in ESTADOS_INTERESSE:
                if data_concurso >= hoje:
                    link = concurso.get("data-url")
                    if not link:
                        continue

                    # Obtém detalhes do concurso
                    detalhes = scraper.obter_detalhes_concurso(link)

                    # Verifica se há palavras-chave relevantes e não há termos indesejados
                    if any(cargo in detalhes for cargo in CARGOS_TI) and not any(termo in detalhes for termo in TERMOS_EXCLUIR):
                        novos_concursos.add(link)
                        mensagem += f"Novo concurso de TI encontrado em {estado}!\nLink: {link}\n" + "-" * 80 + "\n"

    # Remove concursos antigos que não existem mais
    organizador.remover_concursos_antigos(ARQUIVO_BACKUP, novos_concursos)

    # Se houver novos concursos, envia a mensagem
    if novos_concursos != concursos_antigos:
        organizador.salvar_backup_concursos(ARQUIVO_BACKUP, novos_concursos)

        mensagem_telegram = (
            "Concursos Atuais:\n" + "\n".join(concursos_antigos) + 
            "\n\nConcursos Novos:\n" + "\n".join(novos_concursos)
        )

        enviar_telegram(mensagem_telegram)
    else:
        print("Nenhuma alteração nos concursos.")

if __name__ == "__main__":
    main()
