
"""
PROJETO RAGMED - Testes de Grounding (Ancoragem)
Papel: Tester e Validador (Cristovam)

Este script utiliza o pytest para validar se as respostas do RAGMed
estão devidamente ancoradas nos documentos (sem alucinações).
"""

import pytest
import os
import sys

# Adicionar o diretório src ao path para importar o pipeline
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.ragmed_code import carregar_multiplos_documentos, criar_banco_vetorial, configurar_chain_rag, consultar_ragmed
from tests.test_cases import carregar_casos_teste

# Configuração global para os testes
@pytest.fixture(scope="module")
def rag_agent():
    diretorio_projeto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    diretorio_data = os.path.join(diretorio_projeto, "data")
    persist_dir = os.path.join(diretorio_projeto, "db_ragmed_test")
    
    chunks = carregar_multiplos_documentos(diretorio_data)
    vector_db = criar_banco_vetorial(chunks, persist_dir)
    return configurar_chain_rag(vector_db)

def test_grounding_keywords(rag_agent):
    """
    Verifica se a resposta contém as palavras-chave esperadas definidas no qa_pairs.json.
    """
    casos = carregar_casos_teste()
    
    for caso in casos:
        pergunta = caso["question"]
        keywords = caso["expected_keywords"]
        
        print(f"Testando: {pergunta}")
        resultado = consultar_ragmed(pergunta, rag_agent)
        resposta = resultado["result"].lower()
        
        # Verifica se pelo menos uma das palavras-chave ou a ideia central está na resposta
        encontrou = any(kw.lower() in resposta for kw in keywords)
        
        assert encontrou, f"Falha no grounding para: '{pergunta}'. Esperava uma das keywords {keywords} na resposta."

def test_source_attribution(rag_agent):
    """
    Verifica se o sistema está citando as fontes corretamente (explicabilidade).
    """
    pergunta = "Quais as contraindicações da dipirona?"
    resultado = consultar_ragmed(pergunta, rag_agent)
    
    # Verifica se a resposta contém o padrão de citação (Fonte: ...)
    assert "Fonte:" in resultado["result"], "O sistema não citou a fonte na resposta."
    assert len(resultado["source_documents"]) > 0, "Nenhum documento de origem foi retornado."

if __name__ == "__main__":
    print("🚀 Para executar estes testes, use o comando: pytest tests/test_grounding.py")

