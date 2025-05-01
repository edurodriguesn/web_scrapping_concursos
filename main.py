import scraper
import organizar_resultado as organizador
import requests
from datetime import datetime
import unicodedata
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Configurações
TOKEN_BOT = os.getenv('TOKEN_BOT')
CHAT_ID = os.getenv('CHAT_ID')

ESTADOS_INTERESSE = ["AP", "PA", "GO", "MT", "MS", "PB", "MG", "SC", "RS", "PR", "NACIONAL"]

CARGOS_TI = [
    "tecnologia da informacao", "informatica", "analista de sistema", "analise de sistema", "analise em sistema",  
    "arquiteto de sistema", "arquitetura de sistema", "engenheiro de sistema", "engenharia de sistema", "especialista em sistema", "especialidade em sistema",  
    "gerente de sistema", "gerenciamento de sistema", "gestao de sistema", "coordenador de sistema", "coordenacao de sistema",  
    "tecnico de sistema", "tecnica de sistema", "consultor de sistema", "consultoria de sistema", "administrador de sistema", "administracao de sistema",  
    "suporte de sistema",  "testador de sistema", "testes de sistema", "testagem de sistema",  "sistemas",
    "auditor de sistema", "auditoria de sistema",  "operador de sistema", "operacao de sistema",  "cientista de sistema", "ciencia de sistema",  
    "líder de sistema", "liderança de sistema", "computacao", "desenvolvimento de", "analisa de desenvolvimento", 
    "tecnico em desenvolvimento", "especialista em desenvolvimento", "engenheiro de desenvolvimento", "desenvolvedor", "seguranca da informacao", "banco de dados", 
    "redes", "suporte tecnico", "programacao", "programador", "engenharia de software", "arquitetura de software", "infraestrutura de ti", 
    "suporte de ti", "analista de ti", "cientista de dados", "inteligencia artificial", "ciencia de dados", "aprendizado de maquina",
    "governanca de ti", "gestao de projetos de ti", "gestao de riscos de ti", "computacao em nuvem", "forense digital", "tecnologista", "tecnologic",
    "big data", "automacao", "devops", "analise de dados", "analista de dados", "ciencia e tecnologia"
]

TERMOS_EXCLUIR = [
    "informatica basica", "nocoes de informatica", "informatica para iniciantes", "conceitos de informatica", 
    "conhecimentos em informatica", "cursos de informatica", ", informatica", "informatica nivel basico", 
    "informatica nivel iniciante", "informatica fundamental", "nivel basico em informatica", "; informatica",
    "basico em informatica", "basico de informatica", "basicos em informatica", "basicos de informatica", 
    "iniciante em informatica", "iniciante de informatica"
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
    print("Buscando concursos...")
    concursos = scraper.obter_concursos()
    concursos_encontrados = {}
    
    for concurso in concursos:
        div_cc = concurso.find("div", class_="cc")
        data_concurso = concurso.find("div", class_="ce")
        span_text = data_concurso.find("span").get_text(strip=True)
        
        if not span_text[0].isdigit():
            continue
        
        data_concurso = extrair_data(span_text)
        hoje = datetime.today()
        
        if div_cc:
            estado = div_cc.get_text(strip=True) or "NACIONAL"
            
            if estado in ESTADOS_INTERESSE and hoje.date() <= data_concurso.date():
                link = concurso.get("data-url")
                if not link:
                    continue
                
                detalhes = scraper.obter_detalhes_concurso(link)
                detalhes = ''.join(c for c in unicodedata.normalize('NFD', detalhes) if unicodedata.category(c) != 'Mn')

                if any(cargo in detalhes for cargo in CARGOS_TI) and not any(termo in detalhes for termo in TERMOS_EXCLUIR):
                    if estado not in concursos_encontrados:
                        concursos_encontrados[estado] = []
                    concursos_encontrados[estado].append(link)
    
    concursos_atuais, concursos_novos = organizador.organizar_dados(concursos_encontrados)
    
    # Só envia mensagem se houver concursos novos
    if concursos_novos:
        mensagem_telegram = "NOVOS CONCURSOS ENCONTRADOS\n\n"
        
        for estado, links in concursos_novos.items():
            mensagem_telegram += f"[{estado}]\n"
            for link in links:
                mensagem_telegram += f"- {link}\n"
            mensagem_telegram += "\n"
        
        print("Novos concursos encontrados. Enviando mensagem no Telegram...")
        enviar_telegram(mensagem_telegram.strip())
    else:
        print("Nenhum novo concurso encontrado.")


if __name__ == "__main__":
    main()
