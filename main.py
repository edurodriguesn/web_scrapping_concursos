import scraper
import organizar_resultado as organizador
import enviar_mensagem
import filtrar_concursos

def main():
    print("Buscando concursos...")
    # adicionarverificador de url no banco de dados e data de vencimento, para evitar acessar urls ja acessadas 
    # e remover concursos ja encerrados sem acessar o site
    concursos = scraper.obter_concursos()
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