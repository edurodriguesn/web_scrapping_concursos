import scraper
from datetime import datetime
import unicodedata
import re
from transformers import pipeline

# Carrega o classificador zero-shot uma vez
classificador_ti = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


ESTADOS_INTERESSE = ["AP", "PA", "GO", "MT", "MS", "PB", "MG", "SC", "RS", "PR", "NACIONAL"]

PALAVRAS_TI_CERTAS = [
    # Desenvolvimento de Software e Programação
    "programador", "programacao", "desenvolvedor", "desenvolvimento de software", "desenvolvimento de sistema",
    "engenharia de software", "engenheiro de software", "analista de sistema", "analise de sistema",
    "arquiteto de software", "frontend", "backend", "full stack", "front-end", "back-end", "full-stack",

    # Ciência de Dados, IA e Dados
    "cientista de dados", "ciencia de dados", "inteligencia artificial", "ciencia da computacao",
    "processamento de dados", "engenheiro de dados", "analista de dados", "machine learning", "data engineer",

    # Infraestrutura, Redes e Suporte
    "suporte de ti", "auxiliar de ti", "infraestrutura de ti", "redes de computadores",
    "tecnico em informatica", "tecnico de informatica", "administrador de sistema", "devops",
    "sysadmin", "cloud engineer", "service desk",

    # Segurança da Informação
    "seguranca da informacao", "analista de segurança da informação", "cibersegurança",
    "segurança cibernética", "pentester",

    # Banco de Dados
    "banco de dados",

    # Ensino, Pesquisa e Educação em TI
    "professor de informatica", "instrutor de tecnologia", "pesquisador em ti",

    # Área Geral de ti / Computação
    "tecnologia da informacao", "area informatica", "computacao", "analista de ti",
    "tecnico de ti", "especialista em ti", "consultor de ti", "gerente de ti", "tecnico em ti",
    "coordenador de ti", "product owner", "scrum master", "analista funcional", "analista de informatica",
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
            if re.search(r'\b(vaga|cargo|funcao|oportunidade|profiss|pesquisad|analista|tecnico|auxiliar|engenh|especialista)\b', fragmento, re.IGNORECASE):
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

def filtrar_texto(concursos):
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
    return concursos_encontrados