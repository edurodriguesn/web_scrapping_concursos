import scraper.scraper as scraper
from datetime import datetime
import unicodedata
import re
from transformers import pipeline
from utils.data import extrair_data
from deep_translator import GoogleTranslator

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
    "seguranca da informacao", "analista de segurança da informacao", "ciberseguranca",
    "seguranca cibernetica", "pentester",

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
    "dados", "tecnologia", "redes", "telecomunicac",
    "infraestrutura", "software", "hardware"
]

PADROES_TI_REFORCADOS = [
    r'\bprofessor(?:\s+\w+){0,4}\s+informatica\b',
    r'\binstrutor(?:\s+\w+){0,4}\s+tecnologia\b',
    r'\bpesquisador(?:\s+\w+){0,4}\s+(ti|tecnologia)\b',
    r'\b(analista|engenheiro|tecnico|coordenador|auxiliar)(?:\s+\w+){0,4}\s+(dados|software|rede|sistema|ti)\b'
]

def eh_vaga_ti(texto):
    """Classifica se o texto indica vaga de TI com base em palavras-chave e zero-shot."""
    # 1. Palavras específicas: se bater aqui, já retorna True
    if any(palavra in texto for palavra in PALAVRAS_TI_CERTAS):
        return True

    # 2. Palavras genéricas: se houver, aplicar zero-shot
    if any(p in texto for p in PALAVRAS_TI_POTENCIAIS):
        labels = [
            "job in the information technology area",
            "job in an area other than technology"
        ]
        
        # Separar texto por ponto e quebra de linha
        fragmentos = re.split(r'[.\n]', texto)
        
        frases_relevantes = []
        
        PADROES_CARGO = r'\b(analista|t[eé]cnico|auxiliar|administrador|engenheiro|especialista|desenvolvedor|programador|cientista|coordenador|consultor|instrutor|professor|pesquisador|gerente)\b'
    
        for fragmento in fragmentos:
            fragmento = fragmento.strip()
            if not fragmento:
                continue
            
            # 2. Seleciona apenas fragmentos que indicam contexto de vaga
            if re.search(r'\b(vaga|cargo|fun[cç]ão|oportunidade|profiss|pesquisad|analista|t[eé]cnico|auxiliar|engenh|especialista)\b', fragmento, re.IGNORECASE):
                
                # 3. Divide por ponto e vírgula
                subfrases = re.split(r'[;]', fragmento)
                
                for subfrase in subfrases:
                    subfrase = subfrase.strip()
                    if not subfrase:
                        continue

                    # 4. Dentro da subfrase, procura padrões de cargo
                    for match in re.finditer(PADROES_CARGO, subfrase, flags=re.IGNORECASE):
                        inicio = match.start()
                        trecho = subfrase[inicio:inicio + 100].strip()

                        # Verifica se esse trecho contém palavras de TI potenciais
                        if any(re.search(rf'\b{re.escape(p)}\b', trecho, re.IGNORECASE) for p in PALAVRAS_TI_POTENCIAIS):
                            if any(re.search(padrao, trecho, re.IGNORECASE) for padrao in PADROES_TI_REFORCADOS):
                                print(f"Detectado padrão reforçado direto: {trecho}")
                                return True
                            frases_relevantes.append(trecho)
            # Processar as frases relevantes com zero-shot

            for frase in frases_relevantes:
                traducao = GoogleTranslator(source='auto', target='en').translate(frase)
                traducao = traducao.lower().strip()
                resultado = classificador_ti(traducao, labels)

                print(f"Testado: {traducao}")
                
                if resultado["labels"][0] == labels[0] and resultado["scores"][0] > 0.8:
                    print(f"Aprovado Zero-shot: {frase}\n")
                    return True
    # 3. Nenhum indício
    return False

def filtrar_texto(concursos):
    concursos_encontrados = {}

    for concurso in concursos:
        div_cc = concurso.find("div", class_="cc")
        data_concurso_div = concurso.find("div", class_="ce")
        span_text = data_concurso_div.find("span").get_text(strip=True)

        data_concurso = extrair_data(span_text)  # Deve retornar datetime

        if div_cc:
            estado = div_cc.get_text(strip=True) or "NACIONAL"

            if estado in ESTADOS_INTERESSE:
                link = concurso.get("data-url")
                if not link:
                    continue

                detalhes = scraper.obter_detalhes_concurso(link)
                detalhes = ''.join(c for c in unicodedata.normalize('NFD', detalhes) if unicodedata.category(c) != 'Mn')
                detalhes = detalhes[:1500]

                if eh_vaga_ti(detalhes):
                    if estado not in concursos_encontrados:
                        concursos_encontrados[estado] = []
                    concursos_encontrados[estado].append((link, data_concurso.date().isoformat()))

    return concursos_encontrados