import scraper
import organizar_resultado as organizador
import requests
from datetime import datetime

# Configurações
ARQUIVO_BACKUP = "concursos_backup.txt"
TOKEN_BOT = "7829942554:AAFuapRP-53eW0o54IOG7f3PavZr-jIH30U"
CHAT_ID = 2081844601

ESTADOS_INTERESSE = ["AP", "SC", "PA", "PR", "NACIONAL"]
CARGOS_TI = [
    "tecnologia da informação", "informática", "sistema", "computação", "desenvolvimento", "desenvolvedor",
    "segurança da informação", "banco de dados", "redes", "suporte técnico", "programação", "programador",
    "engenharia de software", "arquitetura de software", "infraestrutura de ti", "suporte de ti",
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
    for i in range(len(texto) - 10, -1, -1):
        data_tentativa = texto[i:i+10]
        if data_tentativa.count("/") == 2:
            try:
                return datetime.strptime(data_tentativa, "%d/%m/%Y")
            except ValueError:
                continue
    return None 


def main():
    concursos = scraper.obter_concursos()
    concursos_encontrados = {}
    
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
            if estado in ESTADOS_INTERESSE and data_concurso >= hoje:
                link = concurso.get("data-url")
                if not link:
                    continue
                
                detalhes = scraper.obter_detalhes_concurso(link)
                if any(cargo in detalhes for cargo in CARGOS_TI) and not any(termo in detalhes for termo in TERMOS_EXCLUIR):
                    if estado not in concursos_encontrados:
                        concursos_encontrados[estado] = []
                    concursos_encontrados[estado].append(link)
    
    concursos_atuais, concursos_novos = organizador.organizar_dados(concursos_encontrados, ARQUIVO_BACKUP)
    
    mensagem_telegram = ""
    if concursos_atuais:
        for estado, links in concursos_atuais.items():
            mensagem_telegram += f"[{estado}]\n"
            for link in links:
                if estado in concursos_novos and link in [l.replace(" [!]", "") for l in concursos_novos[estado]]:
                    mensagem_telegram += f"- {link} [!]\n"
                else:
                    mensagem_telegram += f"- {link}\n"
            mensagem_telegram += "\n"
    
    if mensagem_telegram:
        enviar_telegram(mensagem_telegram.strip())
    else:
        print("Nenhuma alteração nos concursos.")


if __name__ == "__main__":
    main()
