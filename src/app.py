import os
import streamlit as st
import subprocess
import time
import shutil
import re
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. Configuração da página Web
st.set_page_config(
    page_title="MedAssist RAG",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- GERENCIAMENTO DE TEMA ---
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

# Injeção de CSS Dinâmico baseado no Tema
theme_css = ""
if st.session_state.theme == "dark":
    theme_css = """
    :root {
        --bg-color: #0e1117;
        --sidebar-bg: #161b22;
        --text-color: #e6edf3;
        --card-bg: #1c2128;
        --border-color: #30363d;
        --primary-blue: #58a6ff;
    }
    """
else:
    theme_css = """
    :root {
        --bg-color: #ffffff;
        --sidebar-bg: #f8fafc;
        --text-color: #1e293b;
        --card-bg: #ffffff;
        --border-color: #e2e8f0;
        --primary-blue: #0066cc;
    }
    """

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@600;700&display=swap');
    
    {theme_css}

    html, body, [data-testid="stAppViewContainer"] {{
        font-family: 'Inter', sans-serif;
        background-color: var(--bg-color) !important;
        color: var(--text-color) !important;
    }}

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px !important;
    }}

    /* Card de Medicamento */
    .med-card {{
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 6px solid var(--primary-blue);
        animation: fadeIn 0.5s ease-out;
    }}

    .med-name {{
        font-family: 'Poppins', sans-serif;
        font-size: 1.5rem;
        color: var(--primary-blue);
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 10px;
        border-bottom: 1px solid var(--border-color);
        padding-bottom: 10px;
    }}

    .med-section {{
        margin-bottom: 15px;
    }}

    .section-label {{
        font-weight: 700;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .label-alignment {{ color: #059669; }}
    .label-pros {{ color: #2563eb; }}
    .label-cons {{ color: #dc2626; }}

    .section-content {{
        font-size: 1rem;
        line-height: 1.6;
        color: var(--text-color);
    }}

    /* Sidebar Clean */
    [data-testid="stSidebar"] {{
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid var(--border-color);
    }}
    
    .sidebar-title {{
        font-family: 'Poppins', sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 20px;
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .source-box {{
        background-color: rgba(100, 116, 139, 0.1);
        border-radius: 10px;
        padding: 15px;
        margin-top: 10px;
        font-size: 0.85rem;
        border-left: 3px solid #64748b;
        color: var(--text-color);
    }}
    
    .fallback-response {{
        background-color: var(--card-bg);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        line-height: 1.7;
        color: var(--text-color);
    }}
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÕES E CAMINHOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_BULAS = os.path.join(BASE_DIR, "./minhas_bulas")
DIRETORIO_BANCO = os.path.join(BASE_DIR, "banco_vetorial_test")
OLLAMA_EMBEDDING_MODEL = "nomic-embed-text"
OLLAMA_CHAT_MODEL = "qwen2.5:7b-instruct"
OLLAMA_BASE_URL = "http://localhost:11434"

# --- FUNÇÕES DE SUPORTE ---
def verificar_ollama_silencioso():
    try:
        subprocess.run(["ollama", "list"], check=True, capture_output=True)
        return True
    except:
        return False

def formatar_documentos(docs):
    return "\n\n".join(doc.page_content for doc in docs)

@st.cache_resource
def carregar_motor_rag():
    if not os.path.exists(PASTA_BULAS):
        os.makedirs(PASTA_BULAS)
    try:
        embeddings = OllamaEmbeddings(model=OLLAMA_EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL)
        if os.path.exists(DIRETORIO_BANCO) and len(os.listdir(DIRETORIO_BANCO)) > 0:
            vector_store = Chroma(persist_directory=DIRETORIO_BANCO, embedding_function=embeddings)
        else:
            loader = DirectoryLoader(PASTA_BULAS, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
            documentos = loader.load()
            if not documentos: return None, None
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
        return rag_chain, retriever
    except Exception as e:
        st.error(f"Erro na inicialização: {e}")
        return None, None

def render_med_card(nome, alinhamento, pros, contras):
    st.markdown(f"""
        <div class="med-card">
            <div class="med-name">💊 {nome}</div>
            <div class="med-section">
                <div class="section-label label-alignment">🎯 Alinhamento Clínico</div>
                <div class="section-content">{alinhamento}</div>
            </div>
            <div class="med-section">
                <div class="section-label label-pros">✅ Prós e Diferenciais</div>
                <div class="section-content">{pros}</div>
            </div>
            <div class="med-section">
                <div class="section-label label-cons">⚠️ Contras e Alertas</div>
                <div class="section-content">{contras}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def parse_response_flexible(text):
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
                    "alin": alin.group(1).strip() if alin else "Informação não disponível.",
                    "pros": pros.group(1).strip() if pros else "Informação não disponível.",
                    "cons": cons.group(1).strip() if cons else "Informação não disponível."
                })
    return results

# --- INTERFACE PRINCIPAL ---

with st.sidebar:
    st.markdown('<div class="sidebar-title">🩺 MedAssist</div>', unsafe_allow_html=True)
    
    # Toggle de Tema
    theme_label = "🌙 Modo Escuro" if st.session_state.theme == "light" else "☀️ Modo Claro"
    if st.button(theme_label, use_container_width=True):
        toggle_theme()
        st.rerun()
    
    st.divider()
    if verificar_ollama_silencioso():
        st.success("Sistema Operacional")
    else:
        st.error("Ollama Offline")
    
    st.divider()
    if os.path.exists(PASTA_BULAS):
        qtd = len([f for f in os.listdir(PASTA_BULAS) if f.endswith('.md')])
        st.metric("Acervo Digital", f"{qtd} Bulas")
    
    st.divider()
    with st.expander("📂 Gerenciar Base"):
        uploaded = st.file_uploader("Nova Bula (.md)", type=["md"])
        if uploaded:
            with open(os.path.join(PASTA_BULAS, uploaded.name), "wb") as f:
                f.write(uploaded.getbuffer())
            st.success("Adicionado!")
            if st.button("Atualizar Base"):
                if os.path.exists(DIRETORIO_BANCO): shutil.rmtree(DIRETORIO_BANCO)
                st.cache_resource.clear()
                st.rerun()
        st.write("---")
        arquivos = [f for f in os.listdir(PASTA_BULAS) if f.endswith('.md')]
        if arquivos:
            remover = st.selectbox("Remover:", arquivos)
            if st.button("Confirmar Exclusão"):
                os.remove(os.path.join(PASTA_BULAS, remover))
                if os.path.exists(DIRETORIO_BANCO): shutil.rmtree(DIRETORIO_BANCO)
                st.cache_resource.clear()
                st.rerun()

st.title("Inteligência de Triagem Clínica")
st.caption("Analise sintomatologias com base em dados farmacêuticos locais.")

with st.container():
    sintomas = st.text_area("Quadro Clínico do Paciente:", placeholder="Ex: Febre alta, dor no corpo...", height=100)
    col1, col2, _ = st.columns([1, 1, 3])
    with col1:
        btn_analisar = st.button("⚡ Analisar", type="primary", use_container_width=True)
    with col2:
        if st.button("🔄 Limpar", use_container_width=True):
            st.session_state.clear()
            st.rerun()

if btn_analisar and sintomas:
    sistema, buscador = carregar_motor_rag()
    if sistema:
        with st.status("🎬 Processando...", expanded=True) as status:
            status.write("🔍 Buscando evidências nas bulas...")
            trechos = buscador.invoke(sintomas)
            status.write("🧠 Gerando parecer clínico...")
            resposta_raw = sistema.invoke(sintomas)
            status.update(label="✅ Concluído", state="complete", expanded=False)
            st.session_state.resposta = resposta_raw
            st.session_state.evidencias = trechos

if "resposta" in st.session_state:
    st.divider()
    col_res, col_evid = st.columns([2.1, 1], gap="large")
    with col_res:
        st.subheader("📋 Parecer Sugerido")
        meds = parse_response_flexible(st.session_state.resposta)
        if not meds:
            st.markdown(f'<div class="fallback-response">{st.session_state.resposta}</div>', unsafe_allow_html=True)
        else:
            for m in meds:
                render_med_card(m['nome'], m['alin'], m['pros'], m['cons'])
        st.download_button("📥 Baixar Parecer", st.session_state.resposta, "parecer_medico.txt")
    with col_evid:
        st.subheader("🔍 Fontes")
        for idx, doc in enumerate(st.session_state.evidencias):
            origem = os.path.basename(doc.metadata.get('source', 'Bula'))
            with st.expander(f"Trecho {idx+1} | {origem}"):
                st.markdown(f'<div class="source-box">{doc.page_content}</div>', unsafe_allow_html=True)
