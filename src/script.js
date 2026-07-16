// ===== CONFIGURAÇÕES =====
const API_URL = `http://${window.location.hostname}:8000`;
let currentTheme = localStorage.getItem('theme') || 'light';

// ===== ELEMENTOS DO DOM =====
const themeToggle = document.getElementById('themeToggle');
const ollamaStatus = document.getElementById('ollamaStatus');
const acervoCount = document.getElementById('acervoCount');
const toggleManage = document.getElementById('toggleManage');
const managePanel = document.getElementById('managePanel');
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const bulasSelect = document.getElementById('bulasSelect');
const deleteBtn = document.getElementById('deleteBtn');
const resetBtn = document.getElementById('resetBtn');
const sintomasInput = document.getElementById('sintomasInput');
const analisarBtn = document.getElementById('analisarBtn');
const limparBtn = document.getElementById('limparBtn');
const loadingState = document.getElementById('loadingState');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const medicamentosContainer = document.getElementById('medicamentosContainer');
const fontesContainer = document.getElementById('fontesContainer');
const downloadBtn = document.getElementById('downloadBtn');
const errorMessage = document.getElementById('errorMessage');

// ===== INICIALIZAÇÃO =====
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    checkOllamaStatus();
    loadBulas();
    setupEventListeners();
    setInterval(checkOllamaStatus, 30000); // Verificar a cada 30 segundos
});

// ===== TEMA =====
function initTheme() {
    if (currentTheme === 'dark') {
        document.body.classList.add('dark-theme');
        themeToggle.textContent = '☀️ Modo Claro';
    } else {
        document.body.classList.remove('dark-theme');
        themeToggle.textContent = '🌙 Modo Escuro';
    }
}

themeToggle.addEventListener('click', () => {
    currentTheme = currentTheme === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', currentTheme);
    initTheme();
});

// ===== OLLAMA STATUS =====
async function checkOllamaStatus() {
    try {
        const response = await fetch(`${API_URL}/health`);
        const data = await response.json();
        
        if (data.ollama === 'online') {
            ollamaStatus.textContent = '✅ Sistema Operacional';
            ollamaStatus.className = 'status-badge status-online';
        } else {
            ollamaStatus.textContent = '❌ Ollama Offline';
            ollamaStatus.className = 'status-badge status-offline';
        }
    } catch (error) {
        ollamaStatus.textContent = '❌ Erro na Conexão';
        ollamaStatus.className = 'status-badge status-offline';
    }
}

// ===== GERENCIAR BULAS =====
toggleManage.addEventListener('click', () => {
    managePanel.classList.toggle('hidden');
});

async function loadBulas() {
    try {
        const response = await fetch(`${API_URL}/bulas`);
        const data = await response.json();
        
        acervoCount.textContent = `${data.total} Bula${data.total !== 1 ? 's' : ''}`;
        
        // Atualizar select
        bulasSelect.innerHTML = '<option value="">Selecione uma bula...</option>';
        data.bulas.forEach(bula => {
            const option = document.createElement('option');
            option.value = bula;
            option.textContent = bula.replace('.md', '');
            bulasSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Erro ao carregar bulas:', error);
    }
}

uploadBtn.addEventListener('click', async () => {
    if (!fileInput.files.length) {
        alert('Selecione um arquivo');
        return;
    }

    const file = fileInput.files[0];
    if (!file.name.endsWith('.md')) {
        alert('Apenas arquivos .md são aceitos');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        uploadBtn.disabled = true;
        uploadBtn.textContent = '⏳ Enviando...';

        const response = await fetch(`${API_URL}/upload-bula`, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            alert('Bula adicionada com sucesso!');
            fileInput.value = '';
            await loadBulas();
        } else {
            alert('Erro ao enviar bula');
        }
    } catch (error) {
        alert('Erro ao enviar bula: ' + error.message);
    } finally {
        uploadBtn.disabled = false;
        uploadBtn.textContent = 'Enviar';
    }
});

deleteBtn.addEventListener('click', async () => {
    if (!bulasSelect.value) {
        alert('Selecione uma bula para remover');
        return;
    }

    if (!confirm('Tem certeza que deseja remover esta bula?')) {
        return;
    }

    try {
        deleteBtn.disabled = true;
        deleteBtn.textContent = '⏳ Removendo...';

        const response = await fetch(`${API_URL}/bula/${bulasSelect.value}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            alert('Bula removida com sucesso!');
            await loadBulas();
        } else {
            alert('Erro ao remover bula');
        }
    } catch (error) {
        alert('Erro ao remover bula: ' + error.message);
    } finally {
        deleteBtn.disabled = false;
        deleteBtn.textContent = 'Confirmar Exclusão';
    }
});

resetBtn.addEventListener('click', async () => {
    if (!confirm('Tem certeza que deseja resetar a base de dados? Isso irá reconstruir o índice vetorial.')) {
        return;
    }

    try {
        resetBtn.disabled = true;
        resetBtn.textContent = '⏳ Resetando...';

        const response = await fetch(`${API_URL}/resetar-base`, {
            method: 'POST'
        });

        if (response.ok) {
            alert('Base de dados resetada com sucesso!');
        } else {
            alert('Erro ao resetar base de dados');
        }
    } catch (error) {
        alert('Erro ao resetar: ' + error.message);
    } finally {
        resetBtn.disabled = false;
        resetBtn.textContent = '🔄 Resetar Base de Dados';
    }
});

// ===== ANÁLISE =====
analisarBtn.addEventListener('click', analisar);
limparBtn.addEventListener('click', limpar);

async function analisar() {
    const sintomas = sintomasInput.value.trim();

    if (!sintomas) {
        showError('Por favor, descreva os sintomas do paciente');
        return;
    }

    try {
        analisarBtn.disabled = true;
        analisarBtn.textContent = '⏳ Analisando...';
        hideError();
        hideResults();
        showLoading();

        const response = await fetch(`${API_URL}/analisar`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ sintomas })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao processar análise');
        }

        const data = await response.json();
        displayResults(data);
        hideLoading();
    } catch (error) {
        showError(error.message);
        hideLoading();
    } finally {
        analisarBtn.disabled = false;
        analisarBtn.textContent = '⚡ Analisar';
    }
}

function limpar() {
    sintomasInput.value = '';
    hideResults();
    hideError();
    medicamentosContainer.innerHTML = '';
    fontesContainer.innerHTML = '';
}

// ===== EXIBIÇÃO DE RESULTADOS =====
function displayResults(data) {
    // Limpar containers
    medicamentosContainer.innerHTML = '';
    fontesContainer.innerHTML = '';

    // Exibir medicamentos
    if (data.medicamentos && data.medicamentos.length > 0) {
        data.medicamentos.forEach(med => {
            const card = createMedicamentoCard(med);
            medicamentosContainer.appendChild(card);
        });
    } else {
        // Se não houver medicamentos parseados, exibir resposta bruta
        const fallbackDiv = document.createElement('div');
        fallbackDiv.className = 'fallback-response';
        fallbackDiv.textContent = data.resposta_bruta;
        medicamentosContainer.appendChild(fallbackDiv);
    }

    // Exibir fontes
    if (data.fontes && data.fontes.length > 0) {
        data.fontes.forEach(fonte => {
            const item = createFonteItem(fonte);
            fontesContainer.appendChild(item);
        });
    }

    // Configurar download
    downloadBtn.onclick = () => downloadParecer(data.resposta_bruta);

    showResults();
}

function createMedicamentoCard(med) {
    const card = document.createElement('div');
    card.className = 'med-card';
    card.innerHTML = `
        <div class="med-name">💊 ${escapeHtml(med.nome)}</div>
        <div class="med-section">
            <div class="section-label label-alignment">🎯 Alinhamento Clínico</div>
            <div class="section-content">${escapeHtml(med.alinhamento)}</div>
        </div>
        <div class="med-section">
            <div class="section-label label-pros">✅ Prós e Diferenciais</div>
            <div class="section-content">${escapeHtml(med.pros)}</div>
        </div>
        <div class="med-section">
            <div class="section-label label-cons">⚠️ Contras e Alertas</div>
            <div class="section-content">${escapeHtml(med.contras)}</div>
        </div>
    `;
    return card;
}

function createFonteItem(fonte) {
    const item = document.createElement('div');
    item.className = 'fonte-item';
    item.innerHTML = `
        <div class="fonte-header">
            <span>Trecho ${fonte.indice} | ${escapeHtml(fonte.origem)}</span>
            <span class="fonte-icon">▼</span>
        </div>
        <div class="fonte-content">
            <div class="fonte-text">${escapeHtml(fonte.conteudo)}</div>
        </div>
    `;

    const header = item.querySelector('.fonte-header');
    header.addEventListener('click', () => {
        item.classList.toggle('expanded');
    });

    return item;
}

function downloadParecer(conteudo) {
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(conteudo));
    element.setAttribute('download', 'parecer_medico.txt');
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

// ===== UTILITÁRIOS =====
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

function showLoading() {
    loadingState.classList.remove('hidden');
}

function hideLoading() {
    loadingState.classList.add('hidden');
}

function showResults() {
    resultsSection.classList.remove('hidden');
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function hideResults() {
    resultsSection.classList.add('hidden');
}

function showError(message) {
    errorMessage.textContent = message;
    errorSection.classList.remove('hidden');
    errorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function hideError() {
    errorSection.classList.add('hidden');
}

// ===== EVENT LISTENERS SETUP =====
function setupEventListeners() {
    // Enter para analisar
    sintomasInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && e.ctrlKey) {
            analisar();
        }
    });
}

// ===== FALLBACK RESPONSE STYLING =====
const style = document.createElement('style');
style.textContent = `
    .fallback-response {
        background-color: var(--card-bg);
        padding: var(--spacing-lg);
        border-radius: var(--radius-lg);
        border: 1px solid var(--border-color);
        line-height: 1.7;
        color: var(--text-color);
        white-space: pre-wrap;
        word-wrap: break-word;
    }
`;
document.head.appendChild(style);
