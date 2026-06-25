
"""
PROJETO RAGMED - Framework de Avaliação RAGAS
Papel: Tester e Validador (Cristóvão)

Este script automatiza a avaliação da qualidade das respostas do RAGMed utilizando o framework RAGAS.
Métricas avaliadas:
- Faithfulness (Fidelidade): A resposta é baseada apenas no contexto?
- Answer Relevance (Relevância da Resposta): A resposta aborda a pergunta?
- Context Precision (Precisão do Contexto): O contexto recuperado é relevante?
- Context Recall (Revocação do Contexto): O contexto contém a resposta correta?
"""

import os
import json
import pandas as pd
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevance,
    context_recall,
    context_precision,
)

# Importar o pipeline do RAGMed
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.ragmed_code import carregar_multiplos_documentos, criar_banco_vetorial, configurar_chain_rag, consultar_ragmed

def carregar_dados_teste(caminho_json):
    with open(caminho_json, 'r', encoding='utf-8') as f:
        return json.load(f)

def executar_avaliacao():
    print("🚀 Iniciando Avaliação RAGAS para o RAGMed...")
    
    # 1. Setup do Ambiente
    diretorio_projeto = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    diretorio_data = os.path.join(diretorio_projeto, "data")
    diretorio_test_data = os.path.join(diretorio_projeto, "tests/test_data")
    persist_dir = os.path.join(diretorio_projeto, "db_ragmed_eval")
    
    # 2. Inicializar o Agente RAGMed
    print("📦 Carregando documentos e inicializando banco vetorial...")
    chunks = carregar_multiplos_documentos(diretorio_data)
    vector_db = criar_banco_vetorial(chunks, persist_dir)
    rag_chain = configurar_chain_rag(vector_db)
    
    # 3. Carregar Ground Truth
    ground_truth_data = carregar_dados_teste(os.path.join(diretorio_test_data, "ground_truth.json"))
    
    questions = []
    answers = []
    contexts = []
    ground_truths = []
    
    # 4. Gerar Respostas do Sistema
    print(f"🔎 Gerando respostas para {len(ground_truth_data)} perguntas de teste...")
    for item in ground_truth_data:
        query = item["question"]
        resultado = consultar_ragmed(query, rag_chain)
        
        questions.append(query)
        answers.append(resultado["result"])
        # RAGAS espera uma lista de strings para os contextos
        contexts.append([doc.page_content for doc in resultado["source_documents"]])
        ground_truths.append(item["ground_truth"])
    
    # 5. Preparar Dataset para o RAGAS
    data_dict = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    }
    dataset = Dataset.from_dict(data_dict)
    
    # 6. Executar Avaliação
    print("📊 Calculando métricas RAGAS...")
    result = evaluate(
        dataset,
        metrics=[
            faithfulness,
            answer_relevance,
            context_precision,
            context_recall,
        ],
    )
    
    # 7. Exibir e Salvar Resultados
    df_results = result.to_pandas()
    print("\n--- RESULTADOS DA AVALIAÇÃO ---")
    print(df_results[['question', 'faithfulness', 'answer_relevance']].to_string())
    
    media_metrics = df_results[['faithfulness', 'answer_relevance', 'context_precision', 'context_recall']].mean()
    print("\n--- MÉDIAS GERAIS ---")
    print(media_metrics)
    
    # Salvar relatório
    report_path = os.path.join(diretorio_projeto, "tests/test_reports/ragas_report.csv")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    df_results.to_csv(report_path, index=False)
    print(f"\n✅ Relatório detalhado salvo em: {report_path}")

if __name__ == "__main__":
    # Certifique-access que a chave da OpenAI está no ambiente
    if "OPENAI_API_KEY" not in os.environ:
        print("❌ Erro: Variável de ambiente OPENAI_API_KEY não encontrada.")
    else:
        executar_avaliacao()
