# Projeto-Engenharia-de-AI

Desenvolvimento de uma 'Agente Neuro-Simbólico para Consulta de Bulas Médicas (RAG)'

## Entrega 1 - Proposta

Documento de uma página referente ao projeto final integrador usando Google Docs.

### Link para o Google Docs

- [Proposta-de-Projeto](https://docs.google.com/document/d/1N6_rNRkz7HLPVQVe9aApThFwQcKJbMNH/edit?usp=sharing&ouid=115746372230166662249&rtpof=true&sd=true)

---

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

## 🛠️ Stack Tecnológico

### Backend

- **FastAPI** - Framework web moderno e performático

- **Uvicorn** - Servidor ASGI de alta performance

- **LangChain** - Orquestração do pipeline de IA

- **ChromaDB** - Banco de dados vetorial para busca semântica

- **Ollama** - Modelos de linguagem rodando localmente
  - **Qwen2.5 (7B)** - Modelo de chat para geração de respostas
  - **Nomic-Embed-Text** - Modelo de embeddings para busca semântica

### Frontend

- **HTML5** - Estrutura semântica

- **CSS3** - Estilos modernos com variáveis CSS e tema dinâmico

- **JavaScript (Vanilla)** - Lógica interativa sem dependências

- **Fetch API** - Comunicação com backend

### Técnicas de IA

- **RAG (Retrieval-Augmented Generation)** - Garantir respostas baseadas em documentos oficiais

- **MMR (Maximal Marginal Relevance)** - Busca semântica com diversidade

- **Vector Embeddings** - Representação semântica de textos

---

## 📈 Resultados e Métricas

- **Acurácia de Recuperação:** O sistema utiliza busca MMR (Maximal Marginal Relevance) para garantir diversidade e precisão nos trechos recuperados.

- **Latência:** Respostas geradas em média em menos de 10 segundos em hardware padrão.

- **Confiabilidade:** 100% das respostas são acompanhadas de citações diretas da fonte original.

- **Performance:** Interface responsiva com carregamento instantâneo do frontend.

---

## 🚀 Como Rodar

### Pré-requisitos

1. **Python 3.8+** - [Download](https://www.python.org/downloads/)

1. **Ollama** instalado - [ollama.com](https://ollama.com)

1. Modelos Ollama baixados:

   ```bash
   ollama pull nomic-embed-text
   ollama pull qwen2.5:7b-instruct
   ```

### Instalação Rápida

#### 1. Clone o repositório

```bash
git clone https://github.com/EytorSantos/Projeto-Engenharia-de-AI.git
cd Projeto-Engenharia-de-AI
```

#### 2. Crie um ambiente virtual (opcional, mas recomendado )

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

#### 4. Inicie o Ollama

```bash
# O Ollama deve estar rodando em http://localhost:11434
ollama serve
```

#### 5. Inicie o Backend (Terminal 1 )

```bash
python run_backend.py
```

Você verá:

```
✅ Iniciando servidor na porta 8000...
📍 Acesse o frontend em: http://localhost:8000/docs
🔌 API disponível em: http://localhost:8000
```

#### 6. Inicie o Frontend (Terminal 2 )

```bash
python run_frontend.py
```

Você verá:

```
✅ Iniciando servidor na porta 8080...
📍 Acesse o frontend em: http://localhost:8080
```

#### 7. Acesse a aplicação

Abra seu navegador e acesse: [**http://localhost:8080**](http://localhost:8080)

---

## 📖 Documentação

### Guias Detalhados

- [**SETUP.md**](./SETUP.md) - Guia completo de instalação, configuração e solução de problemas

- [**RESUMO_ALTERACOES.md**](./RESUMO_ALTERACOES.md) - Detalhes das mudanças na refatoração

### Documentação da API

Acesse a documentação interativa do Swagger em: [**http://localhost:8000/docs**](http://localhost:8000/docs)

### Endpoints Principais

| Método | Endpoint | Descrição |
| --- | --- | --- |
| GET | `/health` | Verifica saúde da API e status do Ollama |
| POST | `/analisar` | Analisa sintomas e retorna medicamentos sugeridos |
| GET | `/bulas` | Lista todas as bulas disponíveis |
| POST | `/upload-bula` | Faz upload de uma nova bula |
| DELETE | `/bula/{nome_arquivo}` | Deleta uma bula existente |
| POST | `/resetar-base` | Reseta o banco vetorial |

---

## ✨ Funcionalidades

### Frontend

- ✅ Interface responsiva (desktop, tablet, mobile )

- ✅ Tema claro/escuro com persistência (localStorage)

- ✅ Análise de sintomas em tempo real

- ✅ Cards de medicamentos com informações estruturadas

- ✅ Fontes expandíveis com trechos das bulas

- ✅ Download de parecer em formato texto

- ✅ Gerenciamento de bulas (upload, delete, reset)

- ✅ Status do Ollama em tempo real

- ✅ Tratamento robusto de erros

### Backend

- ✅ API RESTful com FastAPI

- ✅ CORS habilitado para comunicação frontend-backend

- ✅ Cache de motor RAG para melhor performance

- ✅ Upload de arquivos Markdown

- ✅ Deleção de bulas existentes

- ✅ Reset de banco vetorial

- ✅ Verificação de saúde e status

- ✅ Documentação automática (Swagger/OpenAPI)

---

## 📁 Estrutura do Repositório

```
Projeto-Engenharia-de-AI/
├── README.md                      # Documentação principal (este arquivo)
├── SETUP.md                       # Guia de instalação e configuração
├── RESUMO_ALTERACOES.md          # Detalhes das mudanças na refatoração
├── .gitignore                     # Configuração do Git
├── requirements.txt               # Dependências Python
├── run_backend.py                 # Script para iniciar backend FastAPI
├── run_frontend.py                # Script para iniciar servidor frontend
├── .env.example                   # Exemplo de variáveis de ambiente
│
├── src/
│   ├── app.py                     # Código original Streamlit (referência)
│   ├── backend.py                 # ✨ Novo backend FastAPI
│   ├── index.html                 # ✨ Frontend HTML
│   ├── styles.css                 # ✨ Estilos CSS
│   ├── script.js                  # ✨ Lógica JavaScript
│   └── banco_vetorial_test/       # Banco de dados vetorial (gerado)
│
├── data/
│   ├── bula_dipirona.md           # Exemplo de bula
│   └── bulas/                     # Acervo de bulas em Markdown
│       ├── bula_aciclovir.md
│       ├── bula_amoxicilina.md
│       ├── bula_atenolol.md
│       └── ... (mais bulas)
│
├── tests/
│   ├── test_cases.py              # Casos de teste
│   ├── test_grounding.py          # Testes de grounding
│   ├── ragas_evaluation.py        # Avaliação RAGAS
│   ├── ragmed_tests.md            # Documentação de testes
│   ├── test_data/                 # Dados de teste
│   └── test_reports/              # Relatórios de teste
│
├── notebooks/
│   └── desenvolvimento.ipynb      # Notebook de desenvolvimento
│
├── relatorio/
│   ├── relatorio_tecnico.md       # Relatório técnico
│   └── relatorio_tecnico.pdf      # Relatório em PDF
│
└── slides/
    ├── pitch.md                   # Conteúdo do pitch
    └── pitch.pdf                  # Slides do pitch
```

---

## 🔄 Fluxo de Funcionamento

```
1. Usuário acessa http://localhost:8080
   ↓
2. Frontend carrega (HTML + CSS + JS )
   ↓
3. JavaScript verifica saúde da API (/health)
   ↓
4. Usuário digita sintomas
   ↓
5. JavaScript envia POST /analisar
   ↓
6. Backend FastAPI processa com LangChain + Ollama
   ├─ Busca trechos relevantes no Chroma
   ├─ Envia para o LLM (Qwen2.5)
   └─ Parseia resposta estruturada
   ↓
7. Backend retorna JSON com medicamentos e fontes
   ↓
8. JavaScript renderiza resultados dinamicamente
   ↓
9. Usuário pode fazer download do parecer
```

---

## 🤖 Uso de IA no Desenvolvimento

Utilizamos LLMs (como ChatGPT e Claude) para:

- Estruturação do pipeline LangChain

- Design da interface frontend (HTML/CSS)

- Refinamento do CSS dinâmico para tema Dark/Light

- Geração de templates de prompt para o assistente médico

- Desenvolvimento do backend FastAPI

- Revisão e estruturação da documentação técnica

---

## 🔐 Segurança e Privacidade

- ✅ **Processamento 100% Local:** Todos os modelos rodam localmente via Ollama

- ✅ **Sem Envio de Dados:** Nenhum dado do paciente sai da máquina

- ✅ **Open Source:** Código transparente e auditável

- ✅ **HIPAA Compliant:** Adequado para ambientes clínicos

---

## 🐛 Solução de Problemas

### "Ollama Offline"

- Certifique-se de que o Ollama está rodando: `ollama serve`

- Verifique se está acessível em `http://localhost:11434`

### "Erro ao conectar com o servidor"

- Verifique se o backend está rodando na porta 8000

- Verifique se o frontend está rodando na porta 8080

- Abra o console do navegador (F12 ) para mais detalhes

### "Nenhum documento encontrado"

- Certifique-se de que há arquivos `.md` em `data/bulas/`

- Use o painel "Gerenciar Base" para fazer upload de bulas

Para mais detalhes, consulte [SETUP.md](./SETUP.md)

---

## 📊 Comparação: Streamlit vs Nova Solução

| Aspecto | Streamlit | Nova Solução |
| --- | --- | --- |
| Frontend | Python + Streamlit | HTML + CSS + JS |
| Backend | Streamlit integrado | FastAPI |
| Customização | Limitada | Total |
| Performance | Boa | Excelente |
| Responsividade | Boa | Excelente |
| Tema Dinâmico | Nativo | Customizado |
| Documentação API | Não | Swagger automático |
| Escalabilidade | Limitada | Excelente |
| Tamanho | Grande | Pequeno |

---

## 🎓 Próximos Passos

- [ ] Dockerizar a aplicação

- [ ] Adicionar testes unitários e E2E

- [ ] Configurar CI/CD com GitHub Actions

- [ ] Deploy em servidor (AWS, Heroku, etc.)

- [ ] Adicionar autenticação de usuários

- [ ] Integração com banco de dados persistente

- [ ] Mais animações e efeitos UI

---

## 📞 Suporte e Contribuições

Para dúvidas ou sugestões:

1. Consulte a documentação em [SETUP.md](./SETUP.md)

1. Verifique os logs dos servidores

1. Abra uma issue no repositório

---

## 📄 Licença

Este projeto é de código aberto e disponível sob a licença MIT.

---

## 🙏 Agradecimentos

- **LangChain** - Framework de orquestração de IA

- **Ollama** - Execução local de modelos

- **ChromaDB** - Banco de dados vetorial

- **FastAPI** - Framework web moderno

- **Comunidade Open Source** - Ferramentas e bibliotecas utilizadas

---

**Desenvolvido com ❤️ para assistência médica inteligente**

*Última atualização: Julho de 2026*