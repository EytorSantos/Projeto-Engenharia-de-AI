# Casos de teste do sistema RAGMed

test_cases = [
    {
        "question": "Qual a dosagem recomendada da dipirona?",
        "expected": "Resposta baseada na bula da dipirona"
    },
    {
        "question": "Quais os efeitos colaterais do paracetamol?",
        "expected": "Resposta baseada na bula do paracetamol"
    },
    {
        "question": "Qual a dose do medicamento XYZ123?",
        "expected": "Informação não encontrada"
    }
]

print("Casos de teste carregados com sucesso.")
