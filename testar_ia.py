from transformers import pipeline

classificador_ti = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

labels = [
            "vaga de trabalho na área de tecnologia da informação",
            "vaga de trabalho em outra área que não é tecnologia",
        ]

frases = [
    "Médico cardiologista",
    "Analista em tecnologia da informação",
    "tecnico em desenvolvimento infantil",
    "Professor de programação",
    "administrador de banco de dados"
]

for frase in frases:
    resultado = classificador_ti(frase, labels)
    if resultado["labels"][0] == labels[0] and resultado["scores"][0] > 0.8:
        print(f"\nFrase: {frase}")
        print(f"Classificação: {resultado['labels'][0]} - Score: {resultado['scores'][0]:.4f}")
