# 🩺 MedAssist RAG - Guia de Instalação e Execução

Este documento descreve como configurar e executar o projeto MedAssist RAG com o novo frontend em HTML, CSS e JavaScript.

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

1. **Python 3.8+** - [Download](https://www.python.org/downloads/)
2. **Ollama** - [Download](https://ollama.ai)
3. **Git** (opcional, para clonar o repositório)

## 🚀 Passo 1: Instalar Dependências

Abra um terminal na pasta do projeto e execute:

```bash
pip install -r requirements.txt
```

Isso instalará todas as dependências necessárias:
- FastAPI (framework web)
- Uvicorn (servidor ASGI)
- LangChain e integrações
- Chroma (banco vetorial)
- E outras dependências

## 🔧 Passo 2: Configurar Ollama

1. **Instale e inicie o Ollama** seguindo as instruções em [ollama.ai](https://ollama.ai)

2. **Puxe os modelos necessários** (em um terminal separado):

```bash
ollama pull nomic-embed-text
ollama pull qwen2.5:7b-instruct
```

3. **Verifique se o Ollama está rodando**:
   - Ollama deve estar acessível em `http://localhost:11434`
   - Se estiver usando uma máquina remota, ajuste a variável `OLLAMA_BASE_URL` em `src/backend.py`

## 📁 Passo 3: Preparar Dados

As bulas devem estar no diretório `data/bulas/` em formato Markdown (.md).

O projeto já inclui várias bulas de exemplo. Se quiser adicionar mais:

1. Coloque os arquivos `.md` em `data/bulas/`
2. Ou use a interface web para fazer upload (após iniciar o servidor)

## ▶️ Passo 4: Iniciar os Servidores

### Opção A: Dois Terminais Separados (Recomendado)

**Terminal 1 - Backend FastAPI:**
```bash
python run_backend.py
```

Você verá:
```
✅ Iniciando servidor na porta 8000...
📍 Acesse o frontend em: http://localhost:8000/docs
🔌 API disponível em: http://localhost:8000
```

**Terminal 2 - Frontend HTTP:**
```bash
python run_frontend.py
```

Você verá:
```
✅ Iniciando servidor na porta 8080...
📍 Acesse o frontend em: http://localhost:8080
```

### Opção B: Comando Direto (Linux/Mac)

```bash
# Terminal 1
python run_backend.py

# Terminal 2 (em outro terminal)
python run_frontend.py
```

## 🌐 Acessar a Aplicação

Após iniciar ambos os servidores:

1. **Abra seu navegador** e acesse: `http://localhost:8080`
2. Você verá a interface do MedAssist RAG
3. Verifique se o status do Ollama está "✅ Sistema Operacional" na barra lateral

## 📝 Como Usar

1. **Descrever Sintomas**: Digite os sintomas do paciente no campo de texto
2. **Analisar**: Clique em "⚡ Analisar"
3. **Visualizar Resultados**: 
   - Medicamentos sugeridos aparecem como cards
   - Fontes (trechos das bulas) aparecem na coluna lateral
4. **Gerenciar Base**: Use o painel "📂 Gerenciar Base" para:
   - Adicionar novas bulas
   - Remover bulas existentes
   - Resetar o banco vetorial

## 🎨 Funcionalidades

- ✅ **Tema Claro/Escuro** - Toggle na barra lateral
- ✅ **Interface Responsiva** - Funciona em desktop, tablet e mobile
- ✅ **Gerenciamento de Bulas** - Upload, remoção e reset
- ✅ **Status do Ollama** - Verificação automática a cada 30 segundos
- ✅ **Download de Parecer** - Baixe a análise em formato texto
- ✅ **Fontes Expandíveis** - Visualize os trechos das bulas

## 🔌 Estrutura da API

### Endpoints Principais

- `GET /health` - Verifica saúde da API e status do Ollama
- `POST /analisar` - Analisa sintomas e retorna medicamentos sugeridos
- `GET /bulas` - Lista todas as bulas disponíveis
- `POST /upload-bula` - Faz upload de uma nova bula
- `DELETE /bula/{nome_arquivo}` - Deleta uma bula
- `POST /resetar-base` - Reseta o banco vetorial

### Documentação Interativa

Acesse `http://localhost:8000/docs` para ver a documentação interativa do Swagger.

## 🐛 Solução de Problemas

### "Ollama Offline"
- Certifique-se de que o Ollama está rodando
- Verifique se está acessível em `http://localhost:11434`
- Se usar uma máquina remota, ajuste `OLLAMA_BASE_URL` em `src/backend.py`

### "Erro ao conectar com o servidor"
- Verifique se o backend está rodando na porta 8000
- Verifique se o frontend está rodando na porta 8080
- Verifique o console do navegador (F12) para mais detalhes

### "Nenhum documento encontrado"
- Certifique-se de que há arquivos `.md` em `data/bulas/`
- Use o painel "Gerenciar Base" para fazer upload de bulas

### "Erro ao fazer upload de bula"
- Verifique se o arquivo tem extensão `.md`
- Certifique-se de que tem permissão de escrita no diretório

## 📊 Estrutura do Projeto

```
projeto_ai/
├── src/
│   ├── app.py              # Código original do Streamlit
│   ├── backend.py          # Novo backend FastAPI
│   ├── index.html          # Frontend HTML
│   ├── styles.css          # Estilos CSS
│   └── script.js           # Lógica JavaScript
├── data/
│   └── bulas/              # Bulas em formato Markdown
├── tests/                  # Testes do projeto
├── requirements.txt        # Dependências Python
├── run_backend.py          # Script para iniciar backend
├── run_frontend.py         # Script para iniciar frontend
└── SETUP.md               # Este arquivo
```

## 🔄 Atualizações Futuras

Para atualizar o projeto:

1. Puxe as mudanças do repositório
2. Reinstale as dependências se houver mudanças em `requirements.txt`
3. Reinicie os servidores

## 📞 Suporte

Se encontrar problemas:

1. Verifique se todos os pré-requisitos estão instalados
2. Consulte os logs dos servidores para mais detalhes
3. Verifique o console do navegador (F12) para erros de JavaScript
4. Verifique a documentação da API em `http://localhost:8000/docs`

## 📄 Licença

Este projeto é baseado no projeto original do GitHub e mantém a mesma licença.

---

**Desenvolvido com ❤️ para assistência médica inteligente**
