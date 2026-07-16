# Relatório Técnico: MedAssist RAG
## Sistema de Suporte à Decisão Clínica com IA Local

**Disciplina:** CC0121 - Inteligência Artificial  
**Data:** 15 de Julho de 2026  

---

### 1. Introdução
O projeto MedAssist RAG surge da necessidade de ferramentas digitais seguras e eficientes para profissionais de saúde. Em cenários hospitalares, a rapidez no acesso a informações precisas sobre medicamentos é crucial. Este relatório detalha a arquitetura, implementação e resultados de um sistema de Recuperação Aumentada por Geração (RAG) focado em bulas médicas.

### 2. Descrição do Problema
O volume de informações contido em bulas farmacêuticas é vasto e complexo. Profissionais enfrentam desafios como:
- Tempo escasso para leitura integral de documentos.
- Necessidade de comparar múltiplos medicamentos simultaneamente.
- Preocupação com a privacidade de dados sensíveis ao usar IAs baseadas em nuvem.

### 3. Metodologia e Arquitetura
A solução foi construída utilizando uma arquitetura RAG 100% local, composta por:
- **Ingestão de Dados:** Conversão de bulas para Markdown e segmentação em chunks de 1200 caracteres com sobreposição de 200.
- **Vetorização:** Uso do modelo `nomic-embed-text` para criar representações matemáticas do texto.
- **Armazenamento:** ChromaDB para persistência e busca vetorial.
- **Recuperação:** Busca semântica com algoritmo MMR para evitar redundância.
- **Geração:** Modelo `qwen2.5:7b-instruct` para sintetizar a resposta final baseada apenas no contexto recuperado.

### 4. Tecnologias Utilizadas
- **Linguagem:** Python 3.11
- **Framework de IA:** LangChain
- **Interface:** Streamlit
- **Infraestrutura Local:** Ollama

### 5. Resultados Obtidos
O sistema demonstrou alta eficácia na identificação de contraindicações específicas. Em testes de estresse com sintomas ambíguos, o MedAssist RAG manteve-se fiel às fontes, recusando-se a inventar informações não presentes no acervo (alucinação zero).

### 6. Conclusão
O MedAssist RAG prova que é possível aliar o poder das LLMs à segurança exigida pela área médica através de implementações locais. O projeto cumpre todos os requisitos técnicos e éticos propostos.

