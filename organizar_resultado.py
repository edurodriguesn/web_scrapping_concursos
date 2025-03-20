import os

def ler_backup_concursos(arquivo_backup):
    """Lê os concursos salvos no backup e retorna um dicionário."""
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


def salvar_backup_concursos(arquivo_backup, concursos):
    """Salva os concursos no arquivo de backup."""
    with open(arquivo_backup, "w", encoding="utf-8") as arquivo:
        for estado, links in concursos.items():
            arquivo.write(f"[{estado}]\n")
            arquivo.write("\n".join(links) + "\n\n")


def organizar_dados(concursos_encontrados, arquivo_backup):
    """Compara os concursos encontrados com o backup e retorna os atuais e os novos."""
    concursos_backup = ler_backup_concursos(arquivo_backup)
    
    concursos_atuais = {}
    concursos_novos = {}

    for estado, links in concursos_encontrados.items():
        concursos_atuais[estado] = links  # Todos os encontrados são considerados "atuais"
        
        # Identificar os novos
        links_atuais = set(concursos_backup.get(estado, []))
        links_encontrados = set(links)
        novos_links = links_encontrados - links_atuais
        
        if novos_links:
            concursos_novos[estado] = [f"{link} [!]" for link in novos_links]

    # Atualiza o arquivo de backup
    salvar_backup_concursos(arquivo_backup, concursos_atuais)

    return concursos_atuais, concursos_novos