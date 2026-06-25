
"""
PROJETO RAGMED - Gerenciador de Casos de Teste
Papel: Tester e Validador (Cristovam)

Este módulo carrega os casos de teste definidos em JSON para serem usados
por outros scripts de teste e validação.
"""

import json
import os

def carregar_casos_teste():
    """
    Carrega os casos de teste do ficheiro qa_pairs.json.
    """
    caminho_base = os.path.dirname(__file__)
    caminho_json = os.path.join(caminho_base, 'test_data', 'qa_pairs.json')
    
    try:
        with open(caminho_json, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            return dados.get("test_cases", [])
    except FileNotFoundError:
        print(f"⚠️ Erro: Ficheiro {caminho_json} não encontrado.")
        return []

# Manter compatibilidade com a estrutura anterior, mas agora carregando do JSON
test_cases = carregar_casos_teste()

if __name__ == "__main__":
    print(f"✅ {len(test_cases)} casos de teste carregados com sucesso do qa_pairs.json.")
    for case in test_cases:
        print(f"- [{case.get('medication')}]: {case.get('question')}")

