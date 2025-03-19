# Web Scrapping de Concursos de TI
## Objetivo
- Informar sobre novos concursos públicos da área de TI

## Funcionamento
- Faz web scrapping em site de concurso, filtrando pela área de TI
- Organiza os resultados em um arquivo txt
- Envia os resultados através de um bot no telegram
- Para melhor funcionamento é recomendado agendar execução diária ou semanal, garantindo atualizações constantes

## Instalação
- Primeramente certifique-se de que possui python instalado
### 0 - Ativar ambiente virtual de execução (Linux)
``` bash
source env.sh
```
### 1 - Instalar dependências
``` bash
pip install -r requirements.txt
```

## Execução
``` bash
python3 main.py
```

---
### Melhorias e Correções Futuras
- Adicionar mais sites de concurso
- Melhorar o sistema de notificação
- Otimizar segurança (relacionado ao bot do Telegram)

---
💡 Este projeto foi desenvolvido com o auxílio de IA para otimizar código e estrutura.  
Sinta-se à vontade para contribuir!