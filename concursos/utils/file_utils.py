# concursos/utils/file_utils.py
import os
from django.conf import settings

def ler_backup_concursos():
    """Lê os concursos salvos no backup e retorna um dicionário."""
    arquivo_backup = settings.CONCURSOS_CONFIG['ARQUIVO_BACKUP']
    concursos_backup = {}
    
    if not os.path.exists(arquivo_backup):
        return concursos_backup

    with open(arquivo_backup, "r", encoding="utf-8") as arquivo:
        estado_atual = None
        for linha in arquivo:
            linha = linha.strip()
            if linha.startswith("[") and linha.endswith("]"):
                estado_atual = linha.strip("[]")
                concursos_backup[estado_atual] = []
            elif estado_atual and linha:
                concursos_backup[estado_atual].append(linha)
    
    return concursos_backup

def salvar_backup_concursos(concursos):
    """Salva os concursos no arquivo de backup."""
    arquivo_backup = settings.CONCURSOS_CONFIG['ARQUIVO_BACKUP']
    with open(arquivo_backup, "w", encoding="utf-8") as arquivo:
        for estado, links in concursos.items():
            arquivo.write(f"[{estado}]\n")
            arquivo.write("\n".join(links) + "\n\n")