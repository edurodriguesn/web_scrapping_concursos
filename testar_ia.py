from transformers import pipeline

classificador_ti = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

labels = [
            "cargo na área de tecnologia da informação",
            "cargo em outra área que não é tecnologia",
        ]

frases = [
    "tecnico em desenvolvimento educacional especializado (5 vagas)",
    "analista judiciário - especialidade: redes de computadores",
    "analista judiciário - especialidade: banco de dados",
    "auxiliar em desenvolvimento infantil",
    "tecnico em sistemas para internet"
]

for frase in frases:
    resultado = classificador_ti(frase, labels)
    if resultado["labels"][0] == labels[0]: #and resultado["scores"][0] > 0.8:
        print(f"\nFrase: {frase}")
        print(f"Classificação: {resultado['labels'][0]} - Score: {resultado['scores'][0]:.4f}")
