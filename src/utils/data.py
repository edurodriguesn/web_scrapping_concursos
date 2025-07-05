import unicodedata
from datetime import datetime

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