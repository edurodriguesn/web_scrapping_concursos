import scraper.scraper as scraper
import organizador.organizar_resultado as organizador
import mensagens.telegram as telegram
import filtros.filtrar_concursos as filtrar_concursos
import filtros.prepara_filtro as prepara_filtro

def main():
    print("Limpando resultados antigos...")
    concursos_encontrados = filtrar_concursos.filtrar_texto(
        prepara_filtro.remover_concursos_expirados_html(
            prepara_filtro.remover_urls_ja_processadas(
                scraper.obter_concursos()
            )
        )
    )
    print("Buscando concursos...")
    if concursos_novos_ti := organizador.organizar_dados(concursos_encontrados)[1]:
        print("Novos concursos encontrados, enviando mensagem...")
        telegram.enviar_mensagem(concursos_novos_ti)
    else:
        print("Nenhum novo concurso encontrado.")

if __name__ == "__main__":
    main()