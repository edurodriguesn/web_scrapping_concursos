from transformers import pipeline
from deep_translator import GoogleTranslator

classificador_ti = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

labels = [
        "job in the information technology area",
        "job in an area other than technology",
    ]

frases = [
    "técnico especializado em desenvolvimento educacional (5 vagas)",
    "analista judiciário - especialidade: redes de computadores",
    "analista judiciário - especialidade: banco de dados",
    "auxiliar de desenvolvimento infantil",
    "técnico em desenvolvimento regional"
    "técnico em sistemas de internet"
]

for frase in frases:
    traducao = GoogleTranslator(source='auto', target='en').translate(frase)
    traducao = traducao.lower().strip()
    resultado = classificador_ti(traducao, labels)
    if resultado["labels"][0] == labels[0]: #and resultado["scores"][0] > 0.8:
        print(f"\nFrase: {traducao}")
        print(f"Classificação: {resultado['labels'][0]} - Score: {resultado['scores'][0]:.4f}")
