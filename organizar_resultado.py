def ler_backup_concursos(arquivo):
    """Lê o arquivo de backup de concursos e retorna um set com os links antigos."""
    try:
        with open(arquivo, "r", encoding="utf-8") as file:
            return set(file.read().splitlines())
    except FileNotFoundError:
        with open(arquivo, "w", encoding="utf-8"):
            pass
        return set()

def salvar_backup_concursos(arquivo, concursos):
    """Salva os concursos no arquivo de backup."""
    with open(arquivo, "w", encoding="utf-8") as file:
        for concurso in concursos:
            file.write(concurso + "\n")

def remover_concursos_antigos(arquivo, concursos_existentes):
    """Remove concursos que não existem mais do backup."""
    with open(arquivo, "r", encoding="utf-8") as file:
        links_atualizados = set(file.read().splitlines())

    links_removidos = links_atualizados - concursos_existentes
    if links_removidos:
        with open(arquivo, "w", encoding="utf-8") as file:
            for link in concursos_existentes:
                file.write(link + "\n")
        print(f"Links removidos: {links_removidos}")
