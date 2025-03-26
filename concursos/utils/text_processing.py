# concursos/utils/text_processing.py
from django.conf import settings

def filtrar_cargos_ti(texto):
    """Verifica se o texto contém cargos de TI relevantes."""
    config = settings.CONCURSOS_CONFIG
    return (any(cargo in texto for cargo in config['CARGOS_TI']) and 
            not any(termo in texto for termo in config['TERMOS_EXCLUIR']))