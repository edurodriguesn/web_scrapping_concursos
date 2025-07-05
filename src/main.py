import scraper.scraper as scraper
import organizador.organizar_resultado as organizador
import mensagens.enviar_mensagem as enviar_mensagem
import filtros.filtrar_concursos as filtrar_concursos
import filtros.prepara_filtro as prepara_filtro

def main():
    print("Buscando concursos...")
    concursos = scraper.obter_concursos()
    concursos = prepara_filtro.remover_concursos_expirados_html(concursos)
    concursos = prepara_filtro.remover_concursos_existentes(concursos)
    concursos_encontrados = filtrar_concursos.filtrar_texto(concursos)
    concursos_atuais, concursos_novos = organizador.organizar_dados(concursos_encontrados)
    
    # Só envia mensagem se houver concursos novos
    if concursos_novos:
        print("Novos concursos encontrados, enviando mensagem...")
        mensagem_telegram = enviar_mensagem.formatar_mensagem(concursos_novos)
        enviar_mensagem.enviar_telegram(mensagem_telegram)
    else:
        print("Nenhum novo concurso encontrado.")

if __name__ == "__main__":
    main()