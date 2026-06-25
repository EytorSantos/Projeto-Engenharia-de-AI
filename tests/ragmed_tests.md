# Framework de Testes do RAGMed

## Objetivo
Validar a qualidade, confiabilidade e rastreabilidade das respostas geradas pelo sistema RAG.

## Testes Planejados

### 1. Teste de Grounding
Verificar se a resposta foi baseada no contexto recuperado das bulas.

### 2. Teste de Anti-Alucinação
Verificar se o modelo não inventa informações ausentes nas fontes.

### 3. Teste de Relevância
Verificar se os documentos recuperados são relevantes para a pergunta.

### 4. Avaliação com RAGAS
Métricas:
- Faithfulness
- Answer Relevancy
- Context Precision
- Context Recall

## Casos de Teste Iniciais

| Pergunta | Resultado Esperado |
|-----------|-------------------|
| Qual a dosagem da dipirona? | Resposta baseada na bula |
| Quais os efeitos colaterais do paracetamol? | Resposta baseada na bula |
| Medicamento inexistente | Sistema deve informar ausência de informação |

## Critérios de Aprovação

- Faithfulness > 0.80
- Sem alucinações identificadas
- Respostas fundamentadas nas fontes
