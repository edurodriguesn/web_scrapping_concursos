# concursos/management/commands/scrape_concursos.py
from django.core.management.base import BaseCommand
from concursos.scrapers.pci_scraper import PCIConcursosScraper
from concursos.utils import file_utils, telegram_utils
from concursos.models import Concurso
from concursos.utils.text_processing import filtrar_cargos_ti
from datetime import datetime

class Command(BaseCommand):
    help = 'Executa o web scraping de concursos de TI'

    def handle(self, *args, **options):
        scraper = PCIConcursosScraper()
        config = scraper.config
        concursos = scraper.obter_concursos()
        concursos_encontrados = {}
        
        for concurso in concursos:
            div_cc = concurso.find("div", class_="cc")
            data_concurso = concurso.find("div", class_="ce")
            span_text = data_concurso.find("span").get_text(strip=True)
            
            if "Suspenso" in span_text or "Cancelado" in span_text:
                continue
            
            data_concurso = scraper.extrair_data(span_text)
            hoje = datetime.today()
            
            if div_cc:
                estado = div_cc.get_text(strip=True) or "NACIONAL"
                
                if estado in config['ESTADOS_INTERESSE'] and hoje.date() <= data_concurso.date():
                    link = concurso.get("data-url")
                    if not link:
                        continue
                    
                    detalhes = scraper.obter_detalhes_concurso(link)
                    
                    if filtrar_cargos_ti(detalhes):
                        if estado not in concursos_encontrados:
                            concursos_encontrados[estado] = []
                        concursos_encontrados[estado].append(link)
                        
                        # Salvar no banco de dados
                        Concurso.objects.update_or_create(
                            link=link,
                            defaults={
                                'titulo': concurso.find("div", class_="cd").get_text(strip=True),
                                'estado': estado,
                                'data_concurso': data_concurso,
                                'descricao': detalhes,
                                'novo': True
                            }
                        )
        
        concursos_atuais, concursos_novos = self.organizar_dados(concursos_encontrados)
        
        mensagem_telegram = ""
        if concursos_atuais:
            for estado, links in concursos_atuais.items():
                mensagem_telegram += f"[{estado}]\n"
                for link in links:
                    if estado in concursos_novos and link in [l.replace(" [!]", "") for l in concursos_novos[estado]]:
                        mensagem_telegram += f"- {link} [!]\n"
                    else:
                        mensagem_telegram += f"- {link}\n"
                mensagem_telegram += "\n"
        
        if mensagem_telegram:
            self.stdout.write(self.style.SUCCESS("Concursos encontrados. Enviando mensagem no Telegram..."))
            telegram_utils.enviar_telegram(mensagem_telegram.strip())
        else:
            self.stdout.write("Nenhuma alteração nos concursos.")
    
    def organizar_dados(self, concursos_encontrados):
        """Compara os concursos encontrados com o backup."""
        concursos_backup = file_utils.ler_backup_concursos()
        concursos_atuais = {}
        concursos_novos = {}

        for estado, links in concursos_encontrados.items():
            concursos_atuais[estado] = links
            
            # Identificar os novos
            links_atuais = set(concursos_backup.get(estado, []))
            links_encontrados = set(links)
            novos_links = links_encontrados - links_atuais
            
            if novos_links:
                concursos_novos[estado] = [f"{link} [!]" for link in novos_links]

        # Atualiza o arquivo de backup
        file_utils.salvar_backup_concursos(concursos_atuais)

        return concursos_atuais, concursos_novos