
"""
PROJETO RAGMED - Agente Neuro-Simbólico para Consulta de Bulas Médicas
Papel: Engenheiros de IA (Eytor e Diuler)
Ambiente: Google Colab / Jupyter Notebook

Este módulo contém o pipeline completo para carregar, processar, vetorizar e consultar bulas médicas utilizando LangChain e ChromaDB, com foco em mitigar alucinações e garantir a explicabilidade das respostas.
"""

import os
from typing import List, Dict
from pathlib import Path

# Instalação das dependências necessárias (executar no Colab, se necessário)
# !pip install langchain langchain-community langchain-openai chromadb pypdf tiktoken

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document

# --- 1. CONFIGURAÇÃO E CARREGAMENTO DE DADOS ---

def carregar_e_processar_documentos(caminho_documento: str) -> List[Document]:
    """
    Carrega um documento (bula), limpa o texto e realiza o chunking inteligente.
    Prioriza MarkdownHeaderTextSplitter para manter a semântica das seções.
    Se o documento não for Markdown, usa RecursiveCharacterTextSplitter.

    Args:
        caminho_documento (str): O caminho completo para o arquivo da bula.

    Returns:
        List[Document]: Uma lista de documentos (chunks) processados com metadados.
    """
    print(f"🔄 Carregando e processando documento: {caminho_documento}")
    
    # Determina o tipo de loader com base na extensão do arquivo
    if caminho_documento.endswith('.pdf'):
        loader = PyPDFLoader(caminho_documento)
    elif caminho_documento.endswith('.md') or caminho_documento.endswith('.txt'):
        loader = TextLoader(caminho_documento, encoding='utf-8')
    else:
        raise ValueError("Formato de arquivo não suportado. Use .pdf, .md ou .txt.")

    documentos = loader.load()
    
    if not documentos:
        print(f"⚠️ Nenhum conteúdo encontrado no documento: {caminho_documento}")
        return []

    # Adiciona metadados iniciais (nome do arquivo)
    for doc in documentos:
        doc.metadata["source"] = Path(caminho_documento).name

    # Estratégia de Chunking: Prioriza MarkdownHeaderTextSplitter para bulas estruturadas
    # Se o documento for Markdown, tenta dividir por cabeçalhos
    if caminho_documento.endswith('.md'):
        headers_to_split_on = [
            ("#", "Titulo"),
            ("##", "Secao"),
            ("###", "SubSecao"),
            ("####", "SubSubSecao"),
        ]
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        # Assume que o conteúdo principal está no primeiro documento carregado
        md_header_splits = markdown_splitter.split_text(documentos[0].page_content)
        
        # Adiciona metadados de source para os chunks gerados pelo MarkdownHeaderTextSplitter
        for split in md_header_splits:
            split.metadata["source"] = documentos[0].metadata["source"]

        # Refinamento com RecursiveCharacterTextSplitter para garantir tamanho adequado dos chunks
        # e lidar com texto dentro das seções
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Aumentado para capturar mais contexto por chunk
            chunk_overlap=100, # Sobreposição para manter o contexto entre chunks
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        chunks = text_splitter.split_documents(md_header_splits)
    else:
        # Para PDFs ou outros textos, usa RecursiveCharacterTextSplitter diretamente
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, # Tamanho do chunk
            chunk_overlap=100, # Sobreposição entre chunks
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        chunks = text_splitter.split_documents(documentos)

    print(f"✅ Total de fragmentos (chunks) gerados para {Path(caminho_documento).name}: {len(chunks)}")
    return chunks

def carregar_multiplos_documentos(diretorio_bulas: str) -> List[Document]:
    """
    Carrega e processa múltiplos documentos (bulas) de um diretório.

    Args:
        diretorio_bulas (str): O caminho para o diretório contendo as bulas.

    Returns:
        List[Document]: Uma lista consolidada de todos os chunks processados.
    """
    todos_chunks = []
    for root, _, files in os.walk(diretorio_bulas):
        for file in files:
            if file.endswith(('.pdf', '.md', '.txt')):
                caminho_completo = os.path.join(root, file)
                try:
                    chunks_documento = carregar_e_processar_documentos(caminho_completo)
                    todos_chunks.extend(chunks_documento)
                except Exception as e:
                    print(f"❌ Erro ao processar {caminho_completo}: {e}")
    return todos_chunks

# --- 2. VETORIZAÇÃO E ARMAZENAMENTO ---

def criar_banco_vetorial(chunks: List[Document], persist_directory: str = "db_ragmed") -> Chroma:
    """
    Cria ou carrega o banco de dados vetorial ChromaDB com os embeddings.
    Utiliza OpenAI Embeddings, mas pode ser configurado para outros modelos.

    Args:
        chunks (List[Document]): Lista de documentos (chunks) a serem vetorizados.
        persist_directory (str): Diretório onde o ChromaDB será persistido.

    Returns:
        Chroma: Instância do banco de dados vetorial ChromaDB.
    """
    print(f"🔄 Criando/Carregando banco vetorial em: {persist_directory}")
    # Utilizando OpenAI Embeddings (substituir por outros se necessário)
    # Certifique-se de que OPENAI_API_KEY está configurada no ambiente
    embeddings = OpenAIEmbeddings()
    
    # Verifica se o diretório de persistência existe e se contém dados
    if os.path.exists(persist_directory) and os.listdir(persist_directory):
        print("✅ Banco vetorial existente encontrado. Carregando...")
        vector_db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    else:
        print("✨ Criando novo banco vetorial...")
        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=persist_directory
        )
    
    print(f"✅ Banco vetorial pronto em: {persist_directory}")
    return vector_db

# --- 3. CONFIGURAÇÃO DA CHAIN DE QA (NEURO-SIMBÓLICA) ---

def configurar_chain_rag(vector_db: Chroma, llm_model_name: str = "gpt-4o") -> RetrievalQA:
    """
    Configura a Chain de Question-Answering (QA) com Grounding Estrito.
    O prompt é projetado para mitigar alucinações e forçar a citação de fontes.

    Args:
        vector_db (Chroma): Instância do banco de dados vetorial ChromaDB.
        llm_model_name (str): Nome do modelo LLM a ser utilizado (ex: "gpt-4o", "claude-3-opus-20240229").

    Returns:
        RetrievalQA: Instância da Chain de QA configurada.
    """
    print(f"🔄 Configurando Chain de QA com LLM: {llm_model_name}")
    # Prompt Mestre Anti-Alucinação e com Explicabilidade
    template = """Você é o Agente RAGMed, um assistente médico especialista em bulas da ANVISA.
Use os seguintes fragmentos de contexto recuperados para responder à pergunta do usuário.
Se você não souber a resposta com base APENAS no contexto fornecido, diga explicitamente que não possui essa informação na bula.
NÃO invente informações clínicas, posologias ou qualquer dado médico.
Sua resposta DEVE ser concisa e direta, focando na informação solicitada.
Para cada afirmação na sua resposta, você DEVE citar a 'Secao' e o 'source' (nome do arquivo da bula) de onde a informação foi extraída.
Se uma 'Secao' não estiver disponível, cite apenas o 'source'.

Exemplo de citação: (Fonte: [Nome do Remédio, Secao: Indicação e Para que serve?])

CONTEXTO:
{context}

PERGUNTA: {question}

RESPOSTA FORMATADA (incluindo fontes):
"""

    PROMPT = PromptTemplate(
        template=template, 
        input_variables=["context", "question"]
    )

    # Inicialização do LLM (Camada Neural)
    # Escolha do LLM: GPT-4o é selecionado pela sua capacidade avançada de seguir instruções e raciocínio.
    # Alternativas como Claude 3.5 Sonnet também seriam excelentes escolhas.
    llm = ChatOpenAI(model_name=llm_model_name, temperature=0)

    # Configuração do Retriever (Camada Simbólica)
    # search_kwargs={'k': 3} recupera os 3 chunks mais relevantes
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})

    # Criação da Chain de QA
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff", # 'stuff' concatena todos os documentos em um único prompt
        retriever=retriever,
        return_source_documents=True, # Importante para a explicabilidade
        chain_type_kwargs={"prompt": PROMPT}
    )
    
    print("✅ Chain de QA configurada com sucesso.")
    return qa_chain

# --- 4. FUNÇÃO PRINCIPAL DE CONSULTA ---

def consultar_ragmed(query: str, qa_chain: RetrievalQA) -> Dict:
    """
    Executa uma consulta no agente RAGMed e retorna a resposta com as fontes.

    Args:
        query (str): A pergunta do usuário.
        qa_chain (RetrievalQA): A instância da Chain de QA configurada.

    Returns:
        Dict: Um dicionário contendo a resposta ('result') e os documentos fonte ('source_documents').
    """
    print(f"🔎 Consultando RAGMed com a pergunta: '{query}'")
    resultado = qa_chain({"query": query})
    print("✅ Consulta concluída.")
    return resultado

# --- 5. EXECUÇÃO DO PIPELINE (EXEMPLO DE USO NO COLAB) ---

if __name__ == "__main__":
    # Exemplo de uso em um ambiente Google Colab ou Jupyter Notebook
    # Certifique-se de ter a sua OPENAI_API_KEY configurada como variável de ambiente.
    # Ex: os.environ["OPENAI_API_KEY"] = "sua_chave_aqui"

    # Diretório onde as bulas (ex: bula_dipirona.md) estão localizadas
    # Para este exemplo, vamos usar o arquivo bula_dipirona.md que já foi extraído.
    # Em um cenário real, você apontaria para um diretório com várias bulas.
    diretorio_bulas_exemplo = "/home/ubuntu/task_content/Nova pasta (4)/depois veja/02/"
    caminho_bula_exemplo = os.path.join(diretorio_bulas_exemplo, "bula_dipirona.md")

    # 1. Carregar e processar documentos
    # Em um cenário real, você carregaria todas as bulas do seu diretório
    # todos_os_chunks = carregar_multiplos_documentos(diretorio_bulas_exemplo)
    # Para o exemplo, vamos carregar apenas a bula da dipirona
    todos_os_chunks = carregar_e_processar_documentos(caminho_bula_exemplo)

    if todos_os_chunks:
        # 2. Criar/Carregar banco vetorial
        persist_dir = "/home/ubuntu/RAGMed_Project/db_ragmed"
        db = criar_banco_vetorial(todos_os_chunks, persist_dir)

        # 3. Configurar a Chain de QA
        # Você pode escolher o LLM aqui. GPT-4o é uma boa escolha para seguir instruções.
        ragmed_agent = configurar_chain_rag(db, llm_model_name="gpt-4o")

        # 4. Exemplo de consulta
        query1 = "Quais são as contraindicações da Dipirona para grávidas?"
        resultado1 = consultar_ragmed(query1, ragmed_agent)
        print("\n--- RESPOSTA 1 ---")
        print(resultado1["result"])
        # print("\nDocumentos Fonte:")
        # for doc in resultado1["source_documents"]:
        #     print(f"  - {doc.metadata}")

        query2 = "Qual a posologia para adultos?"
        resultado2 = consultar_ragmed(query2, ragmed_agent)
        print("\n--- RESPOSTA 2 ---")
        print(resultado2["result"])

        query3 = "Quais são os efeitos colaterais mais comuns?"
        resultado3 = consultar_ragmed(query3, ragmed_agent)
        print("\n--- RESPOSTA 3 ---")
        print(resultado3["result"])

        query4 = "Qual o nome do remédio?"
        resultado4 = consultar_ragmed(query4, ragmed_agent)
        print("\n--- RESPOSTA 4 ---")
        print(resultado4["result"])

        query5 = "Quem descobriu a dipirona?"
        resultado5 = consultar_ragmed(query5, ragmed_agent)
        print("\n--- RESPOSTA 5 ---")
        print(resultado5["result"])

    else:
        print("Não foi possível carregar documentos para criar o banco vetorial.")

