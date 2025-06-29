import scraper
import organizar_resultado as organizador
import requests
from datetime import datetime
import unicodedata
import os
from dotenv import load_dotenv
import re
from transformers import pipeline

# Carrega o classificador zero-shot uma vez
classificador_ti = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


# Carrega as variáveis do arquivo .env
load_dotenv()

# Configurações
TOKEN_BOT = os.getenv('TOKEN_BOT')
CHAT_ID = os.getenv('CHAT_ID')

ESTADOS_INTERESSE = ["AP", "PA", "GO", "MT", "MS", "PB", "MG", "SC", "RS", "PR", "NACIONAL"]

PALAVRAS_TI_CERTAS = [
    "analista de sistema", "analise de sistema", "tecnologia da informacao", "suporte de ti", "analista de ti",
    "infraestrutura de ti", "cientista de dados", "engenheiro de software", "ciencia de dados",
    "seguranca da informacao", "programador", "programacao", "desenvolvedor", "banco de dados",
    "inteligencia artificial", "devops", "administrador de sistema", "computacao", "tecnico em informatica",
    "analista de ti", "desenvolvimento de software", "desenvolvimento de sistema", "processamento de dados",
    "ciencia da computacao", "tecnico de informatica", "redes de computadores", "professor de informatica",
]

PALAVRAS_TI_POTENCIAIS = [
    "informatica", "desenvolvimento", "suporte", "sistema", 
    "dados", "tecnologia", "rede", "telecomunicac",
    "infraestrutura", "software", "hardware"
]

def eh_vaga_ti(texto):
    """Classifica se o texto indica vaga de TI com base em palavras-chave e zero-shot."""
    # 1. Palavras específicas: se bater aqui, já retorna True
    if any(palavra in texto for palavra in PALAVRAS_TI_CERTAS):
        return True

    # 2. Palavras genéricas: se houver, aplicar zero-shot
    if any(p in texto for p in PALAVRAS_TI_POTENCIAIS):
        labels = [
            "vaga da área de tecnologia da informação",
            "vaga de outra área"
        ]
        
        # Separar texto por ponto e quebra de linha
        fragmentos = re.split(r'[.\n]', texto)
        
        frases_relevantes = []
        
        for fragmento in fragmentos:
            fragmento = fragmento.strip()
            if not fragmento:
                continue
                
            # Filtrar apenas fragmentos que contenham palavras relacionadas a vaga/cargo
            if re.search(r'\b(vaga|cargo|funcao|oportunidade|profiss|pesquisad|nalista|tecnico|auxiliar|engenh|especialista)\b', fragmento, re.IGNORECASE):
                # Separar por ponto e vírgula
                subfrases = fragmento.split(';')
                
                for subfrase in subfrases:
                    subfrase = subfrase.strip()
                    if not subfrase:
                        continue
                    
                    # Verificar se a subfrase contém pelo menos uma palavra potencial
                    if any(re.search(rf'\b{re.escape(p)}\b', subfrase, re.IGNORECASE) for p in PALAVRAS_TI_POTENCIAIS):
                        frases_relevantes.append(subfrase)
        # Processar as frases relevantes com zero-shot
        for frase in frases_relevantes:
            resultado = classificador_ti(frase, labels)
            if resultado["labels"][0] == labels[0]:
                return True
    # 3. Nenhum indício
    return False

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
                detalhes = detalhes[:1500]

                if (eh_vaga_ti(detalhes)):
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
