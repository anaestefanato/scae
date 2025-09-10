// =========================
// GERENCIAR EDITAIS - JAVASCRIPT
// =========================

// ===== DADOS MOCK DOS EDITAIS =====
let editais = [
    {
        id: 1,
        numero: "001/2025",
        titulo: "Edital de Auxílio Alimentação - 1º Semestre 2025",
        tipo: "auxilio-alimentacao",
        status: "ativo",
        dataPublicacao: "2025-01-15",
        dataInicio: "2025-02-01",
        dataFim: "2025-02-28",
        valorBolsa: 300.00,
        vagas: 150,
        arquivo: "edital_001_2025_alimentacao.pdf",
        tamanhoArquivo: "2.5 MB",
        descricao: "Processo seletivo para concessão de auxílio alimentação aos estudantes em situação de vulnerabilidade socioeconômica."
    },
    {
        id: 2,
        numero: "002/2025",
        titulo: "Edital de Auxílio Transporte - 1º Semestre 2025",
        tipo: "auxilio-transporte",
        status: "ativo",
        dataPublicacao: "2025-01-20",
        dataInicio: "2025-02-05",
        dataFim: "2025-03-05",
        valorBolsa: 150.00,
        vagas: 100,
        arquivo: "edital_002_2025_transporte.pdf",
        tamanhoArquivo: "2.1 MB",
        descricao: "Processo seletivo para concessão de auxílio transporte para estudantes que residem distante do campus."
    },
    {
        id: 3,
        numero: "003/2025",
        titulo: "Edital de Auxílio Moradia - 1º Semestre 2025",
        tipo: "auxilio-moradia",
        status: "ativo",
        dataPublicacao: "2025-01-25",
        dataInicio: "2025-02-10",
        dataFim: "2025-03-10",
        valorBolsa: 400.00,
        vagas: 50,
        arquivo: "edital_003_2025_moradia.pdf",
        tamanhoArquivo: "3.2 MB",
        descricao: "Processo seletivo para concessão de auxílio moradia para estudantes de outros municípios."
    },
    {
        id: 4,
        numero: "004/2024",
        titulo: "Edital de Material Didático - 2º Semestre 2024",
        tipo: "material-didatico",
        status: "encerrado",
        dataPublicacao: "2024-08-01",
        dataInicio: "2024-08-15",
        dataFim: "2024-09-15",
        valorBolsa: 200.00,
        vagas: 80,
        arquivo: "edital_004_2024_material.pdf",
        tamanhoArquivo: "1.8 MB",
        descricao: "Processo seletivo para concessão de auxílio para aquisição de material didático."
    },
    {
        id: 5,
        numero: "005/2024",
        titulo: "Edital de Auxílio Alimentação - 2º Semestre 2024",
        tipo: "auxilio-alimentacao",
        status: "encerrado",
        dataPublicacao: "2024-07-10",
        dataInicio: "2024-08-01",
        dataFim: "2024-08-31",
        valorBolsa: 280.00,
        vagas: 120,
        arquivo: "edital_005_2024_alimentacao.pdf",
        tamanhoArquivo: "2.3 MB",
        descricao: "Processo seletivo para concessão de auxílio alimentação do segundo semestre de 2024."
    },
    {
        id: 6,
        numero: "006/2025",
        titulo: "Rascunho - Edital Auxílio Especial",
        tipo: "auxilio-alimentacao",
        status: "rascunho",
        dataPublicacao: null,
        dataInicio: "2025-03-01",
        dataFim: "2025-03-31",
        valorBolsa: 350.00,
        vagas: 75,
        arquivo: null,
        tamanhoArquivo: null,
        descricao: "Rascunho de edital para auxílio especial em situações emergenciais."
    }
];

let filteredEditais = [...editais];
let uploadedFile = null;

// ===== FUNÇÕES DE INICIALIZAÇÃO =====
document.addEventListener('DOMContentLoaded', function() {
    loadEditaisList();
    updateStatistics();
});

// ===== FUNÇÃO PARA CARREGAR LISTA DE EDITAIS =====
function loadEditaisList() {
    const grid = document.getElementById('editaisGrid');
    if (!grid) return;

    grid.innerHTML = '';

    if (filteredEditais.length === 0) {
        showEmptyState(grid);
        return;
    }

    filteredEditais.forEach(edital => {
        const card = createEditalCard(edital);
        grid.appendChild(card);
    });
}

// ===== FUNÇÃO PARA MOSTRAR ESTADO VAZIO =====
function showEmptyState(container) {
    container.innerHTML = `
        <div class="empty-state col-12">
            <div class="empty-state-icon">
                <i class="bi bi-file-earmark-text"></i>
            </div>
            <h3 class="empty-state-title">Nenhum edital encontrado</h3>
            <p class="empty-state-text">Não há editais correspondentes aos filtros aplicados ou ainda não foram publicados editais.</p>
            <button class="btn btn-publicar-edital" onclick="openNewEditalModal()">
                <i class="bi bi-file-earmark-plus me-2"></i>Publicar Primeiro Edital
            </button>
        </div>
    `;
}

// ===== FUNÇÃO PARA CRIAR CARD DO EDITAL =====
function createEditalCard(edital) {
    const card = document.createElement('div');
    card.className = 'edital-card';
    
    const statusBadge = getStatusBadge(edital.status);
    const tipoBadge = getTipoBadge(edital.tipo);
    const dataPublicacao = edital.dataPublicacao ? new Date(edital.dataPublicacao).toLocaleDateString('pt-BR') : 'Não publicado';
    const dataInicio = new Date(edital.dataInicio).toLocaleDateString('pt-BR');
    const dataFim = new Date(edital.dataFim).toLocaleDateString('pt-BR');
    
    card.innerHTML = `
        <div class="edital-card-header">
            <h5 class="edital-titulo">${edital.titulo}</h5>
            <p class="edital-numero">Edital Nº ${edital.numero}</p>
        </div>
        <div class="edital-card-body">
            <div class="edital-info">
                <div class="edital-info-label">Tipo de Auxílio</div>
                <div class="edital-info-value">${tipoBadge}</div>
            </div>
            <div class="edital-dates">
                <div class="date-item">
                    <div class="date-label">Início</div>
                    <div class="date-value">${dataInicio}</div>
                </div>
                <div class="date-item">
                    <div class="date-label">Fim</div>
                    <div class="date-value">${dataFim}</div>
                </div>
            </div>
            <div class="edital-info">
                <div class="edital-info-label">Valor da Bolsa</div>
                <div class="edital-info-value">R$ ${edital.valorBolsa.toFixed(2).replace('.', ',')}</div>
            </div>
            <div class="edital-info">
                <div class="edital-info-label">Vagas Disponíveis</div>
                <div class="edital-info-value">${edital.vagas} vagas</div>
            </div>
        </div>
        <div class="edital-card-footer">
            <div>${statusBadge}</div>
            <div class="edital-actions">
                <button class="btn btn-sm btn-outline-info" onclick="viewEdital(${edital.id})" title="Visualizar">
                    <i class="bi bi-eye"></i>
                </button>
                ${edital.arquivo ? `
                    <button class="btn btn-sm btn-outline-primary" onclick="downloadEdital(${edital.id})" title="Download">
                        <i class="bi bi-download"></i>
                    </button>
                ` : ''}
                <button class="btn btn-sm btn-outline-secondary" onclick="editEdital(${edital.id})" title="Editar">
                    <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="deleteEdital(${edital.id})" title="Excluir">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        </div>
    `;
    
    return card;
}

// ===== FUNÇÃO PARA OBTER BADGE DE STATUS =====
function getStatusBadge(status) {
    const statusMap = {
        'ativo': '<span class="status-badge ativo">Ativo</span>',
        'encerrado': '<span class="status-badge encerrado">Encerrado</span>',
        'rascunho': '<span class="status-badge rascunho">Rascunho</span>'
    };
    
    return statusMap[status] || '<span class="status-badge">Indefinido</span>';
}

// ===== FUNÇÃO PARA OBTER BADGE DE TIPO =====
function getTipoBadge(tipo) {
    const tipoMap = {
        'auxilio-alimentacao': '<span class="tipo-badge auxilio-alimentacao">Alimentação</span>',
        'auxilio-transporte': '<span class="tipo-badge auxilio-transporte">Transporte</span>',
        'auxilio-moradia': '<span class="tipo-badge auxilio-moradia">Moradia</span>',
        'material-didatico': '<span class="tipo-badge material-didatico">Material</span>'
    };
    
    return tipoMap[tipo] || '<span class="tipo-badge">Outro</span>';
}

// ===== FUNÇÃO PARA ATUALIZAR ESTATÍSTICAS =====
function updateStatistics() {
    const editaisAtivos = editais.filter(e => e.status === 'ativo').length;
    const totalEditais = editais.length;
    const inscricoesAbertas = editais.filter(e => e.status === 'ativo' && new Date(e.dataFim) > new Date()).length;
    const editaisEncerrados = editais.filter(e => e.status === 'encerrado').length;

    // Atualizar cards de estatísticas
    document.querySelector('.editais-ativos .number').textContent = editaisAtivos;
    document.querySelector('.total-editais .number').textContent = totalEditais;
    document.querySelector('.inscricoes-abertas .number').textContent = inscricoesAbertas;
    document.querySelector('.editais-encerrados .number').textContent = editaisEncerrados;
}

// ===== FUNÇÃO DE FILTRO =====
function filterEditais() {
    const filterStatus = document.getElementById('filterStatus').value;
    const filterTipo = document.getElementById('filterTipo').value;
    const filterAno = document.getElementById('filterAno').value;
    
    filteredEditais = editais.filter(edital => {
        let matchStatus = !filterStatus || edital.status === filterStatus;
        let matchTipo = !filterTipo || edital.tipo === filterTipo;
        let matchAno = !filterAno || 
            (edital.dataPublicacao && edital.dataPublicacao.includes(filterAno)) ||
            edital.dataInicio.includes(filterAno);
        
        return matchStatus && matchTipo && matchAno;
    });
    
    loadEditaisList();
    
    const totalFiltrados = filteredEditais.length;
    const mensagem = totalFiltrados === editais.length ? 
        'Filtros removidos. Mostrando todos os editais.' :
        `${totalFiltrados} edital(is) encontrado(s) com os filtros aplicados.`;
    
    showToast(mensagem, 'info');
}

// ===== FUNÇÃO PARA ABRIR MODAL DE NOVO EDITAL =====
function openNewEditalModal() {
    const modalHtml = `
        <div class="modal fade" id="newEditalModal" tabindex="-1">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="bi bi-file-earmark-plus me-2"></i>Publicar Novo Edital
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="newEditalForm">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-floating mb-3">
                                        <input type="text" class="form-control" id="newNumero" required>
                                        <label for="newNumero">Número do Edital</label>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="form-floating mb-3">
                                        <select class="form-select" id="newTipo" required>
                                            <option value="">Selecione...</option>
                                            <option value="auxilio-alimentacao">Auxílio Alimentação</option>
                                            <option value="auxilio-transporte">Auxílio Transporte</option>
                                            <option value="auxilio-moradia">Auxílio Moradia</option>
                                            <option value="material-didatico">Material Didático</option>
                                        </select>
                                        <label for="newTipo">Tipo de Auxílio</label>
                                    </div>
                                </div>
                            </div>
                            <div class="form-floating mb-3">
                                <input type="text" class="form-control" id="newTitulo" required>
                                <label for="newTitulo">Título do Edital</label>
                            </div>
                            <div class="form-floating mb-3">
                                <textarea class="form-control" id="newDescricao" style="height: 100px" required></textarea>
                                <label for="newDescricao">Descrição</label>
                            </div>
                            <div class="row">
                                <div class="col-md-4">
                                    <div class="form-floating mb-3">
                                        <input type="date" class="form-control" id="newDataInicio" required>
                                        <label for="newDataInicio">Data de Início</label>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-floating mb-3">
                                        <input type="date" class="form-control" id="newDataFim" required>
                                        <label for="newDataFim">Data de Fim</label>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="form-floating mb-3">
                                        <input type="number" class="form-control" id="newValorBolsa" step="0.01" required>
                                        <label for="newValorBolsa">Valor da Bolsa (R$)</label>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-floating mb-3">
                                        <input type="number" class="form-control" id="newVagas" required>
                                        <label for="newVagas">Número de Vagas</label>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="form-floating mb-3">
                                        <select class="form-select" id="newStatus" required>
                                            <option value="rascunho">Salvar como Rascunho</option>
                                            <option value="ativo">Publicar Imediatamente</option>
                                        </select>
                                        <label for="newStatus">Status de Publicação</label>
                                    </div>
                                </div>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Arquivo do Edital (PDF)</label>
                                <div class="file-upload-area" id="fileUploadArea">
                                    <div class="file-upload-icon">
                                        <i class="bi bi-cloud-upload"></i>
                                    </div>
                                    <div class="file-upload-text">
                                        <strong>Clique para selecionar</strong> ou arraste o arquivo aqui
                                    </div>
                                    <div class="file-upload-text">
                                        <small>Formato aceito: PDF (máx. 10MB)</small>
                                    </div>
                                    <input type="file" id="editalFile" accept=".pdf" style="display: none;">
                                    <button type="button" class="file-upload-button" onclick="document.getElementById('editalFile').click()">
                                        Selecionar Arquivo
                                    </button>
                                </div>
                                <div id="filePreview" style="display: none;"></div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-success" onclick="saveNewEdital()">
                            <i class="bi bi-check-lg me-1"></i>Salvar Edital
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('newEditalModal'));
    modal.show();
    
    // Configurar upload de arquivo
    setupFileUpload();
    
    // Remove o modal do DOM quando fechado
    document.getElementById('newEditalModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
        uploadedFile = null;
    });
}

// ===== FUNÇÃO PARA CONFIGURAR UPLOAD DE ARQUIVO =====
function setupFileUpload() {
    const fileInput = document.getElementById('editalFile');
    const uploadArea = document.getElementById('fileUploadArea');
    const filePreview = document.getElementById('filePreview');
    
    // Click no upload area
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });
    
    // Seleção de arquivo
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });
    
    function handleFileSelect(file) {
        if (file.type !== 'application/pdf') {
            showToast('Por favor, selecione apenas arquivos PDF.', 'error');
            return;
        }
        
        if (file.size > 10 * 1024 * 1024) { // 10MB
            showToast('O arquivo deve ter no máximo 10MB.', 'error');
            return;
        }
        
        uploadedFile = file;
        showFilePreview(file);
    }
    
    function showFilePreview(file) {
        const sizeInMB = (file.size / (1024 * 1024)).toFixed(2);
        
        filePreview.innerHTML = `
            <div class="uploaded-file">
                <div class="file-info">
                    <i class="bi bi-file-earmark-pdf file-icon"></i>
                    <div class="file-details">
                        <h6>${file.name}</h6>
                        <small>${sizeInMB} MB</small>
                    </div>
                </div>
                <div class="file-actions">
                    <button type="button" class="btn btn-sm btn-outline-danger" onclick="removeFile()">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </div>
        `;
        
        filePreview.style.display = 'block';
        uploadArea.style.display = 'none';
    }
}

// ===== FUNÇÃO PARA REMOVER ARQUIVO =====
function removeFile() {
    uploadedFile = null;
    document.getElementById('filePreview').style.display = 'none';
    document.getElementById('fileUploadArea').style.display = 'block';
    document.getElementById('editalFile').value = '';
}

// ===== FUNÇÃO PARA SALVAR NOVO EDITAL =====
function saveNewEdital() {
    const form = document.getElementById('newEditalForm');
    
    // Validar formulário
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const newEdital = {
        id: Date.now(),
        numero: document.getElementById('newNumero').value,
        titulo: document.getElementById('newTitulo').value,
        tipo: document.getElementById('newTipo').value,
        status: document.getElementById('newStatus').value,
        dataPublicacao: document.getElementById('newStatus').value === 'ativo' ? 
            new Date().toISOString().split('T')[0] : null,
        dataInicio: document.getElementById('newDataInicio').value,
        dataFim: document.getElementById('newDataFim').value,
        valorBolsa: parseFloat(document.getElementById('newValorBolsa').value),
        vagas: parseInt(document.getElementById('newVagas').value),
        arquivo: uploadedFile ? uploadedFile.name : null,
        tamanhoArquivo: uploadedFile ? `${(uploadedFile.size / (1024 * 1024)).toFixed(2)} MB` : null,
        descricao: document.getElementById('newDescricao').value
    };
    
    // Verificar se número já existe
    if (editais.find(e => e.numero === newEdital.numero)) {
        showToast('Número de edital já existe no sistema.', 'error');
        return;
    }
    
    // Adicionar à lista
    editais.push(newEdital);
    filteredEditais = [...editais];
    
    // Atualizar interface
    loadEditaisList();
    updateStatistics();
    
    // Fechar modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('newEditalModal'));
    modal.hide();
    
    const statusText = newEdital.status === 'ativo' ? 'publicado' : 'salvo como rascunho';
    showToast(`Edital ${statusText} com sucesso!`, 'success');
}

// ===== FUNÇÃO PARA VISUALIZAR EDITAL =====
function viewEdital(id) {
    const edital = editais.find(e => e.id === id);
    if (!edital) return;
    
    const modalHtml = `
        <div class="modal fade" id="viewEditalModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="bi bi-file-earmark-text me-2"></i>Detalhes do Edital
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-md-8">
                                <h4>${edital.titulo}</h4>
                                <p class="text-muted mb-3">Edital Nº ${edital.numero}</p>
                            </div>
                            <div class="col-md-4 text-end">
                                ${getStatusBadge(edital.status)}
                                ${getTipoBadge(edital.tipo)}
                            </div>
                        </div>
                        
                        <div class="row mb-4">
                            <div class="col-md-6">
                                <h6>Informações Básicas</h6>
                                <p><strong>Valor da Bolsa:</strong> R$ ${edital.valorBolsa.toFixed(2).replace('.', ',')}</p>
                                <p><strong>Vagas Disponíveis:</strong> ${edital.vagas}</p>
                                <p><strong>Data de Publicação:</strong> ${edital.dataPublicacao ? new Date(edital.dataPublicacao).toLocaleDateString('pt-BR') : 'Não publicado'}</p>
                            </div>
                            <div class="col-md-6">
                                <h6>Período de Inscrições</h6>
                                <p><strong>Data de Início:</strong> ${new Date(edital.dataInicio).toLocaleDateString('pt-BR')}</p>
                                <p><strong>Data de Fim:</strong> ${new Date(edital.dataFim).toLocaleDateString('pt-BR')}</p>
                                ${edital.arquivo ? `
                                    <p><strong>Arquivo:</strong> ${edital.arquivo} (${edital.tamanhoArquivo})</p>
                                ` : ''}
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <h6>Descrição</h6>
                            <p>${edital.descricao}</p>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                        ${edital.arquivo ? `
                            <button type="button" class="btn btn-outline-primary" onclick="downloadEdital(${edital.id})">
                                <i class="bi bi-download me-1"></i>Download PDF
                            </button>
                        ` : ''}
                        <button type="button" class="btn btn-outline-secondary" onclick="editEdital(${edital.id}); bootstrap.Modal.getInstance(document.getElementById('viewEditalModal')).hide();">
                            <i class="bi bi-pencil me-1"></i>Editar
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('viewEditalModal'));
    modal.show();
    
    // Remove o modal do DOM quando fechado
    document.getElementById('viewEditalModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

// ===== FUNÇÃO PARA DOWNLOAD DO EDITAL =====
function downloadEdital(id) {
    const edital = editais.find(e => e.id === id);
    if (!edital || !edital.arquivo) return;
    
    showToast(`Download do arquivo "${edital.arquivo}" iniciado.`, 'info');
    
    // Simular download
    setTimeout(() => {
        showToast('Download concluído com sucesso!', 'success');
    }, 2000);
}

// ===== FUNÇÃO PARA EDITAR EDITAL =====
function editEdital(id) {
    const edital = editais.find(e => e.id === id);
    if (!edital) return;
    
    // Implementação similar ao modal de criação, mas com dados preenchidos
    showToast('Funcionalidade de edição em desenvolvimento.', 'info');
}

// ===== FUNÇÃO PARA EXCLUIR EDITAL =====
function deleteEdital(id) {
    const edital = editais.find(e => e.id === id);
    if (!edital) return;
    
    const modalHtml = `
        <div class="modal fade" id="deleteEditalModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header bg-danger text-white">
                        <h5 class="modal-title">
                            <i class="bi bi-exclamation-triangle me-2"></i>Confirmar Exclusão
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p>Tem certeza que deseja excluir o edital?</p>
                        <div class="alert alert-info">
                            <strong>Edital:</strong> ${edital.titulo}<br>
                            <strong>Número:</strong> ${edital.numero}
                        </div>
                        <p class="text-muted">Esta ação não pode ser desfeita. Todas as inscrições relacionadas a este edital também serão removidas.</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-danger" onclick="confirmDeleteEdital(${edital.id})">
                            <i class="bi bi-trash me-1"></i>Excluir Edital
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('deleteEditalModal'));
    modal.show();
    
    // Remove o modal do DOM quando fechado
    document.getElementById('deleteEditalModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

// ===== FUNÇÃO PARA CONFIRMAR EXCLUSÃO =====
function confirmDeleteEdital(id) {
    const editalIndex = editais.findIndex(e => e.id === id);
    if (editalIndex === -1) return;
    
    const editalTitulo = editais[editalIndex].titulo;
    
    // Remover da lista
    editais.splice(editalIndex, 1);
    filteredEditais = [...editais];
    
    // Atualizar interface
    loadEditaisList();
    updateStatistics();
    
    // Fechar modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('deleteEditalModal'));
    modal.hide();
    
    showToast(`Edital "${editalTitulo}" excluído com sucesso.`, 'success');
}

// ===== FUNÇÃO PARA MOSTRAR TOAST =====
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer') || createToastContainer();
    
    const toastId = 'toast_' + Date.now();
    const bgClass = {
        'success': 'bg-success',
        'error': 'bg-danger',
        'warning': 'bg-warning',
        'info': 'bg-info'
    }[type] || 'bg-info';
    
    const iconClass = {
        'success': 'bi-check-circle',
        'error': 'bi-exclamation-circle',
        'warning': 'bi-exclamation-triangle',
        'info': 'bi-info-circle'
    }[type] || 'bi-info-circle';
    
    const toastHtml = `
        <div id="${toastId}" class="toast" role="alert">
            <div class="toast-header ${bgClass} text-white">
                <i class="bi ${iconClass} me-2"></i>
                <strong class="me-auto">Sistema SCAE</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remove o toast do DOM após ser escondido
    toastElement.addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

// ===== FUNÇÃO PARA CRIAR CONTAINER DE TOAST =====
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}
