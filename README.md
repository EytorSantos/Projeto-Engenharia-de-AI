# Projeto-Engenharia-de-AI
Desenvolvimento de uma 'Agente Neuro-Simbólico para Consulta de Bulas Médicas (RAG)'

## Entrega 1-Proposta
Documento de uma pagina referente ao projeto final intregador usando google Docs.
### Link para o Goolge docs: 
- [Proposta-de-Projeto](https://docs.google.com/document/d/1N6_rNRkz7HLPVQVe9aApThFwQcKJbMNH/edit?usp=sharing&ouid=115746372230166662249&rtpof=true&sd=true)
# 🩺 MedAssist RAG - Inteligência de Triagem Clínica

**Otimizando decisões terapêuticas com RAG 100% local e seguro.**

---

## 👥 Equipe
- **Cristovam Augusto dos Santos Barreiros**: [Papel: Desenvolvedor Backend/IA]
- **Maria Yasmin de Oliveira de Souza e Eytor Santos Assunção**: [Papel: Desenvolvedor Frontend/UX]
- **Diule Monteiro Pereira Junior**: [Papel: Especialista em Dados/Documentação]

---

## ⚠️ O Problema
No ambiente clínico de alta pressão, profissionais de saúde precisam tomar decisões rápidas sobre prescrições, muitas vezes consultando múltiplas bulas extensas para verificar contraindicações e interações. O erro humano ou a demora na consulta de informações técnicas pode comprometer a segurança do paciente.

## 💡 A Solução
O **MedAssist RAG** é uma ferramenta de suporte à decisão que utiliza a técnica de **Retrieval-Augmented Generation (RAG)** para cruzar sintomas relatados com um acervo digital de bulas médicas. 
- **Privacidade:** Processamento 100% local via Ollama.
- **Transparência:** Exibe as fontes exatas (trechos das bulas) para validação médica.
- **Eficiência:** Gera relatórios comparativos instantâneos de prós e contras.

---

## 🛠️ Técnicas Utilizadas
- **RAG (Retrieval-Augmented Generation):** Para garantir que a IA responda baseada apenas em documentos oficiais (bulas).
- **LangChain:** Framework para orquestração do pipeline de IA.
- **ChromaDB:** Banco de dados vetorial para busca semântica eficiente.
- **Ollama (Qwen2.5 & Nomic-Embed):** Modelos de linguagem e embeddings rodando localmente para privacidade total.
- **Streamlit:** Interface web responsiva e intuitiva.

---

## 📈 Resultados e Métricas
- **Acurácia de Recuperação:** O sistema utiliza busca MMR (Maximal Marginal Relevance) para garantir diversidade e precisão nos trechos recuperados.
- **Latência:** Respostas geradas em média em menos de 10 segundos em hardware padrão.
- **Confiabilidade:** 100% das respostas são acompanhadas de citações diretas da fonte original.

---

## 🚀 Como Rodar

### Pré-requisitos
1. **Python 3.10+**
2. **Ollama** instalado ([ollama.com](https://ollama.com))
3. Modelos baixados:
   ```bash
   ollama pull nomic-embed-text
   ollama pull qwen2.5:7b-instruct
   ```

### Instalação
1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd meu-projeto-ia
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute a aplicação:
   ```bash
   streamlit run src/app.py
   ```

---

## 🤖 Uso de IA no Desenvolvimento
Utilizamos LLMs (como ChatGPT e Claude) para:
- Estruturação do pipeline LangChain.
- Refinamento do CSS dinâmico para o tema Dark/Light.
- Geração de templates de prompt para o assistente médico.
- Revisão e estruturação da documentação técnica.

---

## 📁 Estrutura do Repositório
```text
meu-projeto-ia/
├── README.md            # Documentação principal
├── requirements.txt     # Dependências do projeto
├── notebooks/           # EDA e experimentos
├── src/                 # Código fonte da aplicação
├── data/                # Acervo de bulas (.md)
├── relatorio/           # Relatório técnico final
└── slides/              # Slides do pitch executivo
```
