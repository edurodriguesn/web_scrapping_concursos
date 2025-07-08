import scraper.scraper as scraper
import organizador.organizar_resultado as organizador
import mensagens.telegram as telegram
import filtros.filtrar_concursos as filtrar_concursos
import filtros.prepara_filtro as prepara_filtro

def main():
    print("Buscando concursos...")
    concursos_encontrados = filtrar_concursos.filtrar_texto(
        prepara_filtro.remover_concursos_existentes(
            prepara_filtro.remover_concursos_expirados_html(
                scraper.obter_concursos()
            )
        )
    )
    if concursos_novos_ti := organizador.organizar_dados(concursos_encontrados)[1]:
        print("Novos concursos encontrados, enviando mensagem...")
        telegram.enviar_mensagem(concursos_novos_ti)
    else:
        print("Nenhum novo concurso encontrado.")

if __name__ == "__main__":
    main()