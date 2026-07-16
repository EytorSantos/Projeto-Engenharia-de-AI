import os
import shutil
import re
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
import subprocess
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Configuração FastAPI
app = FastAPI(title="MedAssist RAG API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONFIGURAÇÕES E CAMINHOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_BULAS = os.path.join(BASE_DIR, "../data/bulas")
DIRETORIO_BANCO = os.path.join(BASE_DIR, "banco_vetorial_test")
OLLAMA_EMBEDDING_MODEL = "nomic-embed-text"
OLLAMA_CHAT_MODEL = "qwen2.5:7b-instruct"
OLLAMA_BASE_URL = "http://localhost:11434"

# Cache global para o motor RAG
rag_cache = {"motor": None, "buscador": None}

# --- MODELOS PYDANTIC ---
class SintomasRequest(BaseModel):
    sintomas: str

class MedicamentoResponse(BaseModel):
    nome: str
    alinhamento: str
    pros: str
    contras: str

class AnaliseResponse(BaseModel):
    medicamentos: list[MedicamentoResponse]
    resposta_bruta: str
    fontes: list[dict]

# --- FUNÇÕES DE SUPORTE ---
def verificar_ollama():
    try:
        subprocess.run(["ollama", "list"], check=True, capture_output=True)
        return True
    except:
        return False

def formatar_documentos(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def carregar_motor_rag():
    """Carrega ou recupera do cache o motor RAG."""
    if rag_cache["motor"] is not None:
        return rag_cache["motor"], rag_cache["buscador"]
    
    if not os.path.exists(PASTA_BULAS):
        os.makedirs(PASTA_BULAS)
    
    try:
        embeddings = OllamaEmbeddings(model=OLLAMA_EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL)
        
        if os.path.exists(DIRETORIO_BANCO) and len(os.listdir(DIRETORIO_BANCO)) > 0:
            vector_store = Chroma(persist_directory=DIRETORIO_BANCO, embedding_function=embeddings)
        else:
            loader = DirectoryLoader(PASTA_BULAS, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
            documentos = loader.load()
            if not documentos:
                raise Exception("Nenhum documento encontrado na pasta de bulas")
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
            chunks = text_splitter.split_documents(documentos)
            vector_store = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=DIRETORIO_BANCO)
        
        retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 5, "fetch_k": 15})
        llm = ChatOllama(model=OLLAMA_CHAT_MODEL, temperature=0, base_url=OLLAMA_BASE_URL, timeout=300)
        
        template_prompt = """
        Você é um assistente médico rigoroso. Analise os sintomas e as bulas para sugerir tratamentos.
        REGRAS CRÍTICAS:
        1. Para CADA medicamento, você DEVE usar os marcadores EXATOS: ---MED--- e ---END---.
        2. Dentro dos marcadores, use EXATAMENTE estes campos: NOME:, ALINHAMENTO:, PROS:, CONTRAS:.
        3. Não use negrito (**) dentro dos campos.
        4. Coloque cada campo em uma nova linha.
        EXEMPLO DE FORMATO OBRIGATÓRIO:
        ---MED---
        NOME: Dipirona
        ALINHAMENTO: Indicado para febre e dor.
        PROS: Ação rápida em 30 minutos.
        CONTRAS: Risco de choque anafilático.
        ---END---
        Contexto: {context}
        Paciente: {input}
        Resposta:
        """
        
        prompt = ChatPromptTemplate.from_template(template_prompt)
        rag_chain = ({"context": retriever | formatar_documentos, "input": RunnablePassthrough()} | prompt | llm | StrOutputParser())
        
        rag_cache["motor"] = rag_chain
        rag_cache["buscador"] = retriever
        
        return rag_chain, retriever
    except Exception as e:
        raise Exception(f"Erro na inicialização do motor RAG: {str(e)}")

def parse_response_flexible(text):
    """Extrai medicamentos da resposta do LLM."""
    blocks = re.split(r"---MED---|---END---", text)
    results = []
    for block in blocks:
        if "NOME:" in block:
            nome = re.search(r"NOME:\s*(.*?)(?:\n|$)", block, re.I)
            alin = re.search(r"ALINHAMENTO:\s*(.*?)(?:\n|$|PROS:)", block, re.S | re.I)
            pros = re.search(r"PROS:\s*(.*?)(?:\n|$|CONTRAS:)", block, re.S | re.I)
            cons = re.search(r"CONTRAS:\s*(.*?)(?:\n|$)", block, re.S | re.I)
            if nome:
                results.append({
                    "nome": nome.group(1).strip(),
                    "alinhamento": alin.group(1).strip() if alin else "Informação não disponível.",
                    "pros": pros.group(1).strip() if pros else "Informação não disponível.",
                    "contras": cons.group(1).strip() if cons else "Informação não disponível."
                })
    return results

# --- ENDPOINTS ---

@app.get("/health")
async def health():
    """Verifica saúde da API e status do Ollama."""
    ollama_ok = verificar_ollama()
    return {
        "status": "ok",
        "ollama": "online" if ollama_ok else "offline",
        "acervo": len([f for f in os.listdir(PASTA_BULAS) if f.endswith('.md')]) if os.path.exists(PASTA_BULAS) else 0
    }

@app.post("/analisar")
async def analisar(request: SintomasRequest):
    """Analisa sintomas e retorna medicamentos sugeridos."""
    if not request.sintomas or len(request.sintomas.strip()) == 0:
        raise HTTPException(status_code=400, detail="Sintomas não podem estar vazios")
    
    if not verificar_ollama():
        raise HTTPException(status_code=503, detail="Ollama está offline")
    
    try:
        motor, buscador = carregar_motor_rag()
        
        # Buscar evidências
        trechos = buscador.invoke(request.sintomas)
        
        # Gerar parecer
        resposta_raw = motor.invoke(request.sintomas)
        
        # Parsear medicamentos
        meds = parse_response_flexible(resposta_raw)
        
        # Formatar fontes
        fontes = []
        for idx, doc in enumerate(trechos):
            origem = os.path.basename(doc.metadata.get('source', 'Bula'))
            fontes.append({
                "indice": idx + 1,
                "origem": origem,
                "conteudo": doc.page_content
            })
        
        return AnaliseResponse(
            medicamentos=[MedicamentoResponse(**m) for m in meds],
            resposta_bruta=resposta_raw,
            fontes=fontes
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar análise: {str(e)}")

@app.get("/bulas")
async def listar_bulas():
    """Lista todas as bulas disponíveis."""
    if not os.path.exists(PASTA_BULAS):
        return {"bulas": []}
    
    bulas = [f for f in os.listdir(PASTA_BULAS) if f.endswith('.md')]
    return {"bulas": bulas, "total": len(bulas)}

@app.post("/upload-bula")
async def upload_bula(file: UploadFile = File(...)):
    """Faz upload de uma nova bula."""
    if not file.filename.endswith('.md'):
        raise HTTPException(status_code=400, detail="Apenas arquivos .md são aceitos")
    
    try:
        if not os.path.exists(PASTA_BULAS):
            os.makedirs(PASTA_BULAS)
        
        file_path = os.path.join(PASTA_BULAS, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        # Limpar cache para recarregar
        if os.path.exists(DIRETORIO_BANCO):
            shutil.rmtree(DIRETORIO_BANCO)
        rag_cache["motor"] = None
        rag_cache["buscador"] = None
        
        return {"mensagem": "Bula adicionada com sucesso", "arquivo": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload: {str(e)}")

@app.delete("/bula/{nome_arquivo}")
async def deletar_bula(nome_arquivo: str):
    """Deleta uma bula existente."""
    file_path = os.path.join(PASTA_BULAS, nome_arquivo)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    
    try:
        os.remove(file_path)
        
        # Limpar cache para recarregar
        if os.path.exists(DIRETORIO_BANCO):
            shutil.rmtree(DIRETORIO_BANCO)
        rag_cache["motor"] = None
        rag_cache["buscador"] = None
        
        return {"mensagem": "Bula deletada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar: {str(e)}")

@app.post("/resetar-base")
async def resetar_base():
    """Reseta o banco vetorial."""
    try:
        if os.path.exists(DIRETORIO_BANCO):
            shutil.rmtree(DIRETORIO_BANCO)
        rag_cache["motor"] = None
        rag_cache["buscador"] = None
        return {"mensagem": "Base de dados resetada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao resetar: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
