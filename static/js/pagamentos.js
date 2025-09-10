// =====================================================
// GERENCIAR PAGAMENTOS - JAVASCRIPT
// =====================================================

document.addEventListener('DOMContentLoaded', function() {
    // ===== INICIALIZAÇÃO =====
    initializePage();
    loadPagamentos();
    setupEventListeners();
});

// ===== VARIÁVEIS GLOBAIS =====
let currentPage = 1;
const itemsPerPage = 10;
let totalItems = 0;
let currentFilters = {
    status: '',
    tipo: '',
    mes: '',
    banco: ''
};

// Dados de exemplo dos pagamentos
let pagamentosData = [
    {
        id: 1,
        aluno: 'Ana Silva Santos',
        matricula: '20230001',
        tipo: 'Auxílio Moradia',
        valor: 300.00,
        vencimento: '2024-01-15',
        status: 'pendente',
        banco: 'Banco do Brasil',
        conta: '12345-6',
        agencia: '1234'
    },
    {
        id: 2,
        aluno: 'Carlos Eduardo Lima',
        matricula: '20230002',
        tipo: 'Auxílio Transporte',
        valor: 150.00,
        vencimento: '2024-01-12',
        status: 'processando',
        banco: 'Caixa Econômica',
        conta: '23456-7',
        agencia: '2345'
    },
    {
        id: 3,
        aluno: 'Maria Fernanda Costa',
        matricula: '20230003',
        tipo: 'Auxílio Moradia',
        valor: 300.00,
        vencimento: '2024-01-10',
        status: 'concluido',
        banco: 'Santander',
        conta: '34567-8',
        agencia: '3456'
    },
    {
        id: 4,
        aluno: 'João Pedro Oliveira',
        matricula: '20230004',
        tipo: 'Auxílio Transporte',
        valor: 150.00,
        vencimento: '2024-01-08',
        status: 'erro',
        banco: 'Itaú',
        conta: '45678-9',
        agencia: '4567'
    },
    {
        id: 5,
        aluno: 'Beatriz Santos Lima',
        matricula: '20230005',
        tipo: 'Auxílio Moradia',
        valor: 300.00,
        vencimento: '2024-01-20',
        status: 'pendente',
        banco: 'Banco do Brasil',
        conta: '56789-0',
        agencia: '5678'
    },
    {
        id: 6,
        aluno: 'Gabriel Ferreira Souza',
        matricula: '20230006',
        tipo: 'Auxílio Transporte',
        valor: 150.00,
        vencimento: '2024-01-25',
        status: 'pendente',
        banco: 'Caixa Econômica',
        conta: '67890-1',
        agencia: '6789'
    },
    {
        id: 7,
        aluno: 'Larissa Almeida Santos',
        matricula: '20230007',
        tipo: 'Auxílio Moradia',
        valor: 300.00,
        vencimento: '2024-01-18',
        status: 'concluido',
        banco: 'Santander',
        conta: '78901-2',
        agencia: '7890'
    },
    {
        id: 8,
        aluno: 'Rafael Costa Oliveira',
        matricula: '20230008',
        tipo: 'Auxílio Transporte',
        valor: 150.00,
        vencimento: '2024-01-22',
        status: 'processando',
        banco: 'Itaú',
        conta: '89012-3',
        agencia: '8901'
    }
];

// ===== INICIALIZAÇÃO DA PÁGINA =====
function initializePage() {
    updateStats();
    updatePagamentosPendentes();
    setupDateMask();
    setupTooltips();
}

// ===== CONFIGURAÇÃO DE EVENT LISTENERS =====
function setupEventListeners() {
    // Botão processar lote
    document.getElementById('btnProcessarLote').addEventListener('click', showProcessarLoteModal);
    
    // Filtros
    document.getElementById('filterStatus').addEventListener('change', handleFilterChange);
    document.getElementById('filterTipo').addEventListener('change', handleFilterChange);
    document.getElementById('filterMes').addEventListener('change', handleFilterChange);
    document.getElementById('filterBanco').addEventListener('change', handleFilterChange);
    
    // Botão limpar filtros
    document.getElementById('btnLimparFiltros')?.addEventListener('click', clearFilters);
    
    // Modals
    setupModalEventListeners();
    
    // Busca
    const searchInput = document.querySelector('#searchPagamentos');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(handleSearch, 300));
    }
}

// ===== CONFIGURAÇÃO DE TOOLTIPS =====
function setupTooltips() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
}

// ===== CONFIGURAÇÃO DE MÁSCARAS =====
function setupDateMask() {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        input.addEventListener('input', function() {
            // Formatação automática se necessário
        });
    });
}

// ===== ATUALIZAÇÃO DE ESTATÍSTICAS =====
function updateStats() {
    const stats = calculateStats();
    
    document.querySelector('.stats-card.pagamentos-pendentes .number').textContent = stats.pendentes;
    document.querySelector('.stats-card.valor-pendente .number').textContent = formatMoney(stats.valorPendente);
    document.querySelector('.stats-card.pagamentos-processados .number').textContent = stats.processados;
    document.querySelector('.stats-card.valor-processado .number').textContent = formatMoney(stats.valorProcessado);
}

function calculateStats() {
    const pendentes = pagamentosData.filter(p => p.status === 'pendente').length;
    const processados = pagamentosData.filter(p => p.status === 'concluido').length;
    const valorPendente = pagamentosData
        .filter(p => p.status === 'pendente')
        .reduce((sum, p) => sum + p.valor, 0);
    const valorProcessado = pagamentosData
        .filter(p => p.status === 'concluido')
        .reduce((sum, p) => sum + p.valor, 0);
    
    return {
        pendentes,
        processados,
        valorPendente,
        valorProcessado
    };
}

// ===== ATUALIZAÇÃO DE PAGAMENTOS PENDENTES URGENTES =====
function updatePagamentosPendentes() {
    const container = document.getElementById('pagamentosPendentesContainer');
    const pagamentosPendentes = pagamentosData
        .filter(p => p.status === 'pendente')
        .sort((a, b) => new Date(a.vencimento) - new Date(b.vencimento))
        .slice(0, 3); // Apenas os 3 mais urgentes
    
    if (pagamentosPendentes.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-check-circle empty-state-icon"></i>
                <h5 class="empty-state-title">Nenhum pagamento pendente urgente</h5>
                <p class="empty-state-text">Todos os pagamentos estão em dia!</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = pagamentosPendentes.map(pagamento => `
        <div class="pagamento-pendente-item">
            <div class="row align-items-center">
                <div class="col-md-3">
                    <div class="pagamento-info">
                        <h6>${pagamento.aluno}</h6>
                        <small>Mat: ${pagamento.matricula}</small>
                    </div>
                </div>
                <div class="col-md-2">
                    <span class="badge bg-primary">${pagamento.tipo}</span>
                </div>
                <div class="col-md-2">
                    <span class="valor-destaque">R$ ${formatMoney(pagamento.valor)}</span>
                </div>
                <div class="col-md-2">
                    <span class="data-vencimento ${getVencimentoClass(pagamento.vencimento)}">
                        ${formatDate(pagamento.vencimento)}
                    </span>
                </div>
                <div class="col-md-3">
                    <div class="action-buttons">
                        <button class="btn btn-sm btn-success" onclick="processarPagamento(${pagamento.id})" 
                                data-bs-toggle="tooltip" title="Processar Pagamento">
                            <i class="fas fa-check"></i>
                        </button>
                        <button class="btn btn-sm btn-primary" onclick="editarPagamento(${pagamento.id})" 
                                data-bs-toggle="tooltip" title="Editar">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-info" onclick="visualizarPagamento(${pagamento.id})" 
                                data-bs-toggle="tooltip" title="Visualizar">
                            <i class="fas fa-eye"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
    
    // Reativar tooltips
    setupTooltips();
}

// ===== CARREGAMENTO DE PAGAMENTOS =====
function loadPagamentos() {
    const filteredData = applyFilters(pagamentosData);
    totalItems = filteredData.length;
    
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const pageData = filteredData.slice(startIndex, endIndex);
    
    renderPagamentosTable(pageData);
    updatePagination();
}

function renderPagamentosTable(data) {
    const tbody = document.getElementById('pagamentosTableBody');
    
    if (data.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="8" class="text-center py-4">
                    <div class="empty-state">
                        <i class="fas fa-search empty-state-icon"></i>
                        <h5 class="empty-state-title">Nenhum pagamento encontrado</h5>
                        <p class="empty-state-text">Tente ajustar os filtros de busca</p>
                    </div>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = data.map(pagamento => `
        <tr>
            <td>
                <div>
                    <strong>${pagamento.aluno}</strong><br>
                    <small class="text-muted">Mat: ${pagamento.matricula}</small>
                </div>
            </td>
            <td>
                <span class="badge bg-primary">${pagamento.tipo}</span>
            </td>
            <td>
                <strong class="text-success">R$ ${formatMoney(pagamento.valor)}</strong>
            </td>
            <td>${formatDate(pagamento.vencimento)}</td>
            <td>
                <span class="status-badge ${pagamento.status}">${getStatusText(pagamento.status)}</span>
            </td>
            <td>
                <span class="bank-badge ${getBankClass(pagamento.banco)}">${pagamento.banco}</span><br>
                <small class="text-muted">Ag: ${pagamento.agencia} | CC: ${pagamento.conta}</small>
            </td>
            <td>
                <div class="action-buttons">
                    ${pagamento.status === 'pendente' ? `
                        <button class="btn btn-sm btn-success" onclick="processarPagamento(${pagamento.id})" 
                                data-bs-toggle="tooltip" title="Processar">
                            <i class="fas fa-play"></i>
                        </button>
                    ` : ''}
                    <button class="btn btn-sm btn-primary" onclick="editarPagamento(${pagamento.id})" 
                            data-bs-toggle="tooltip" title="Editar">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-info" onclick="visualizarPagamento(${pagamento.id})" 
                            data-bs-toggle="tooltip" title="Visualizar">
                        <i class="fas fa-eye"></i>
                    </button>
                    ${pagamento.status === 'erro' ? `
                        <button class="btn btn-sm btn-warning" onclick="reprocessarPagamento(${pagamento.id})" 
                                data-bs-toggle="tooltip" title="Reprocessar">
                            <i class="fas fa-redo"></i>
                        </button>
                    ` : ''}
                </div>
            </td>
        </tr>
    `).join('');
    
    // Reativar tooltips
    setupTooltips();
}

// ===== APLICAÇÃO DE FILTROS =====
function applyFilters(data) {
    return data.filter(pagamento => {
        if (currentFilters.status && pagamento.status !== currentFilters.status) return false;
        if (currentFilters.tipo && pagamento.tipo !== currentFilters.tipo) return false;
        if (currentFilters.banco && pagamento.banco !== currentFilters.banco) return false;
        if (currentFilters.mes) {
            const pagamentoMes = new Date(pagamento.vencimento).getMonth() + 1;
            if (pagamentoMes.toString().padStart(2, '0') !== currentFilters.mes) return false;
        }
        return true;
    });
}

// ===== MANIPULAÇÃO DE FILTROS =====
function handleFilterChange(event) {
    const filterId = event.target.id;
    const value = event.target.value;
    
    switch(filterId) {
        case 'filterStatus':
            currentFilters.status = value;
            break;
        case 'filterTipo':
            currentFilters.tipo = value;
            break;
        case 'filterMes':
            currentFilters.mes = value;
            break;
        case 'filterBanco':
            currentFilters.banco = value;
            break;
    }
    
    currentPage = 1;
    loadPagamentos();
}

function clearFilters() {
    currentFilters = {
        status: '',
        tipo: '',
        mes: '',
        banco: ''
    };
    
    document.getElementById('filterStatus').value = '';
    document.getElementById('filterTipo').value = '';
    document.getElementById('filterMes').value = '';
    document.getElementById('filterBanco').value = '';
    
    currentPage = 1;
    loadPagamentos();
    
    showToast('Filtros limpos com sucesso!', 'success');
}

// ===== BUSCA =====
function handleSearch(event) {
    const searchTerm = event.target.value.toLowerCase();
    
    if (searchTerm === '') {
        loadPagamentos();
        return;
    }
    
    const filteredData = pagamentosData.filter(pagamento => 
        pagamento.aluno.toLowerCase().includes(searchTerm) ||
        pagamento.matricula.toLowerCase().includes(searchTerm) ||
        pagamento.tipo.toLowerCase().includes(searchTerm) ||
        pagamento.banco.toLowerCase().includes(searchTerm)
    );
    
    totalItems = filteredData.length;
    currentPage = 1;
    
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const pageData = filteredData.slice(startIndex, endIndex);
    
    renderPagamentosTable(pageData);
    updatePagination();
}

// ===== PAGINAÇÃO =====
function updatePagination() {
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    const pagination = document.getElementById('pagination');
    
    if (totalPages <= 1) {
        pagination.style.display = 'none';
        return;
    }
    
    pagination.style.display = 'flex';
    
    let paginationHTML = `
        <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
            <a class="page-link" href="#" onclick="changePage(${currentPage - 1})">Anterior</a>
        </li>
    `;
    
    const startPage = Math.max(1, currentPage - 2);
    const endPage = Math.min(totalPages, currentPage + 2);
    
    if (startPage > 1) {
        paginationHTML += `<li class="page-item"><a class="page-link" href="#" onclick="changePage(1)">1</a></li>`;
        if (startPage > 2) {
            paginationHTML += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
        }
    }
    
    for (let i = startPage; i <= endPage; i++) {
        paginationHTML += `
            <li class="page-item ${i === currentPage ? 'active' : ''}">
                <a class="page-link" href="#" onclick="changePage(${i})">${i}</a>
            </li>
        `;
    }
    
    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            paginationHTML += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
        }
        paginationHTML += `<li class="page-item"><a class="page-link" href="#" onclick="changePage(${totalPages})">${totalPages}</a></li>`;
    }
    
    paginationHTML += `
        <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
            <a class="page-link" href="#" onclick="changePage(${currentPage + 1})">Próximo</a>
        </li>
    `;
    
    pagination.innerHTML = paginationHTML;
}

function changePage(page) {
    if (page < 1 || page > Math.ceil(totalItems / itemsPerPage)) return;
    currentPage = page;
    loadPagamentos();
}

// ===== AÇÕES DE PAGAMENTO =====
function processarPagamento(id) {
    const pagamento = pagamentosData.find(p => p.id === id);
    if (!pagamento) return;
    
    showConfirmDialog(
        'Processar Pagamento',
        `Confirma o processamento do pagamento de R$ ${formatMoney(pagamento.valor)} para ${pagamento.aluno}?`,
        () => {
            // Simular processamento
            pagamento.status = 'processando';
            updateStats();
            updatePagamentosPendentes();
            loadPagamentos();
            
            showToast('Pagamento enviado para processamento!', 'success');
            
            // Simular conclusão após 3 segundos
            setTimeout(() => {
                pagamento.status = 'concluido';
                updateStats();
                updatePagamentosPendentes();
                loadPagamentos();
                showToast('Pagamento processado com sucesso!', 'success');
            }, 3000);
        }
    );
}

function editarPagamento(id) {
    const pagamento = pagamentosData.find(p => p.id === id);
    if (!pagamento) return;
    
    // Preencher modal de edição
    document.getElementById('editPagamentoId').value = pagamento.id;
    document.getElementById('editAluno').value = pagamento.aluno;
    document.getElementById('editMatricula').value = pagamento.matricula;
    document.getElementById('editTipo').value = pagamento.tipo;
    document.getElementById('editValor').value = pagamento.valor;
    document.getElementById('editVencimento').value = pagamento.vencimento;
    document.getElementById('editBanco').value = pagamento.banco;
    document.getElementById('editAgencia').value = pagamento.agencia;
    document.getElementById('editConta').value = pagamento.conta;
    
    const modal = new bootstrap.Modal(document.getElementById('editPagamentoModal'));
    modal.show();
}

function visualizarPagamento(id) {
    const pagamento = pagamentosData.find(p => p.id === id);
    if (!pagamento) return;
    
    // Preencher modal de visualização
    document.getElementById('viewAluno').textContent = pagamento.aluno;
    document.getElementById('viewMatricula').textContent = pagamento.matricula;
    document.getElementById('viewTipo').textContent = pagamento.tipo;
    document.getElementById('viewValor').textContent = `R$ ${formatMoney(pagamento.valor)}`;
    document.getElementById('viewVencimento').textContent = formatDate(pagamento.vencimento);
    document.getElementById('viewStatus').innerHTML = `<span class="status-badge ${pagamento.status}">${getStatusText(pagamento.status)}</span>`;
    document.getElementById('viewBanco').textContent = pagamento.banco;
    document.getElementById('viewAgencia').textContent = pagamento.agencia;
    document.getElementById('viewConta').textContent = pagamento.conta;
    
    const modal = new bootstrap.Modal(document.getElementById('viewPagamentoModal'));
    modal.show();
}

function reprocessarPagamento(id) {
    const pagamento = pagamentosData.find(p => p.id === id);
    if (!pagamento) return;
    
    showConfirmDialog(
        'Reprocessar Pagamento',
        `Confirma o reprocessamento do pagamento para ${pagamento.aluno}?`,
        () => {
            pagamento.status = 'processando';
            updateStats();
            updatePagamentosPendentes();
            loadPagamentos();
            
            showToast('Pagamento enviado para reprocessamento!', 'warning');
            
            // Simular conclusão após 3 segundos
            setTimeout(() => {
                pagamento.status = 'concluido';
                updateStats();
                updatePagamentosPendentes();
                loadPagamentos();
                showToast('Pagamento reprocessado com sucesso!', 'success');
            }, 3000);
        }
    );
}

// ===== PROCESSAMENTO EM LOTE =====
function showProcessarLoteModal() {
    const modal = new bootstrap.Modal(document.getElementById('processarLoteModal'));
    modal.show();
}

function processarLote() {
    const banco = document.querySelector('input[name="bancoLote"]:checked')?.value;
    const dataProcessamento = document.getElementById('dataProcessamento').value;
    
    if (!banco) {
        showToast('Selecione um banco para processamento!', 'error');
        return;
    }
    
    if (!dataProcessamento) {
        showToast('Selecione a data de processamento!', 'error');
        return;
    }
    
    const pagamentosPendentes = pagamentosData.filter(p => 
        p.status === 'pendente' && p.banco === banco
    );
    
    if (pagamentosPendentes.length === 0) {
        showToast('Nenhum pagamento pendente encontrado para este banco!', 'warning');
        return;
    }
    
    showConfirmDialog(
        'Processar Lote',
        `Confirma o processamento de ${pagamentosPendentes.length} pagamentos do ${banco}?`,
        () => {
            // Simular processamento em lote
            const progressModal = new bootstrap.Modal(document.getElementById('progressModal'));
            progressModal.show();
            
            let processed = 0;
            const total = pagamentosPendentes.length;
            
            const processNext = () => {
                if (processed < total) {
                    pagamentosPendentes[processed].status = 'concluido';
                    processed++;
                    
                    const progress = (processed / total) * 100;
                    document.getElementById('progressBar').style.width = `${progress}%`;
                    document.getElementById('progressText').textContent = `${processed}/${total} pagamentos processados`;
                    
                    setTimeout(processNext, 500);
                } else {
                    updateStats();
                    updatePagamentosPendentes();
                    loadPagamentos();
                    
                    setTimeout(() => {
                        progressModal.hide();
                        showToast(`${total} pagamentos processados com sucesso!`, 'success');
                        
                        // Fechar modal de processamento em lote
                        const loteModal = bootstrap.Modal.getInstance(document.getElementById('processarLoteModal'));
                        loteModal.hide();
                    }, 1000);
                }
            };
            
            processNext();
        }
    );
}

// ===== CONFIGURAÇÃO DE MODALS =====
function setupModalEventListeners() {
    // Botão salvar pagamento editado
    document.getElementById('btnSalvarPagamento').addEventListener('click', salvarPagamentoEditado);
    
    // Botão processar lote
    document.getElementById('btnConfirmarLote').addEventListener('click', processarLote);
    
    // Seleção de banco no modal de lote
    document.querySelectorAll('input[name="bancoLote"]').forEach(radio => {
        radio.addEventListener('change', function() {
            document.querySelectorAll('.bank-option').forEach(option => {
                option.classList.remove('selected');
            });
            this.closest('.bank-option').classList.add('selected');
        });
    });
}

function salvarPagamentoEditado() {
    const id = parseInt(document.getElementById('editPagamentoId').value);
    const pagamento = pagamentosData.find(p => p.id === id);
    
    if (!pagamento) return;
    
    // Atualizar dados
    pagamento.aluno = document.getElementById('editAluno').value;
    pagamento.matricula = document.getElementById('editMatricula').value;
    pagamento.tipo = document.getElementById('editTipo').value;
    pagamento.valor = parseFloat(document.getElementById('editValor').value);
    pagamento.vencimento = document.getElementById('editVencimento').value;
    pagamento.banco = document.getElementById('editBanco').value;
    pagamento.agencia = document.getElementById('editAgencia').value;
    pagamento.conta = document.getElementById('editConta').value;
    
    updateStats();
    updatePagamentosPendentes();
    loadPagamentos();
    
    // Fechar modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('editPagamentoModal'));
    modal.hide();
    
    showToast('Pagamento atualizado com sucesso!', 'success');
}

// ===== FUNÇÕES UTILITÁRIAS =====
function formatMoney(value) {
    return parseFloat(value).toLocaleString('pt-BR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}

function getStatusText(status) {
    const statusMap = {
        'pendente': 'Pendente',
        'processando': 'Processando',
        'concluido': 'Concluído',
        'erro': 'Erro'
    };
    return statusMap[status] || status;
}

function getVencimentoClass(vencimento) {
    const hoje = new Date();
    const dataVencimento = new Date(vencimento);
    const diffDays = Math.ceil((dataVencimento - hoje) / (1000 * 60 * 60 * 24));
    
    if (diffDays < 0) return 'urgente'; // Vencido
    if (diffDays <= 3) return 'urgente'; // Vence em até 3 dias
    if (diffDays <= 7) return 'proximo'; // Vence em até 7 dias
    return 'normal'; // Vence em mais de 7 dias
}

function getBankClass(banco) {
    const bankClasses = {
        'Banco do Brasil': 'banco-brasil',
        'Caixa Econômica': 'caixa',
        'Santander': 'santander',
        'Itaú': 'itau'
    };
    return bankClasses[banco] || '';
}

function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer') || createToastContainer();
    
    const toastId = 'toast_' + Date.now();
    const bgClass = type === 'success' ? 'bg-success' : 
                   type === 'error' ? 'bg-danger' : 
                   type === 'warning' ? 'bg-warning' : 'bg-info';
    
    const toastHTML = `
        <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header ${bgClass} text-white">
                <i class="fas fa-info-circle me-2"></i>
                <strong class="me-auto">Sistema</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remover toast após ser ocultado
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

function showConfirmDialog(title, message, onConfirm) {
    const modalHTML = `
        <div class="modal fade" id="confirmModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p>${message}</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" id="confirmBtn">Confirmar</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remover modal existente se houver
    const existingModal = document.getElementById('confirmModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    const modal = new bootstrap.Modal(document.getElementById('confirmModal'));
    modal.show();
    
    document.getElementById('confirmBtn').addEventListener('click', () => {
        modal.hide();
        onConfirm();
    });
    
    // Remover modal do DOM quando for fechado
    document.getElementById('confirmModal').addEventListener('hidden.bs.modal', () => {
        document.getElementById('confirmModal').remove();
    });
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ===== EXPORTAÇÃO DE DADOS =====
function exportarRelatorio() {
    const filteredData = applyFilters(pagamentosData);
    
    // Preparar dados para exportação
    const csvData = [
        ['Aluno', 'Matrícula', 'Tipo', 'Valor', 'Vencimento', 'Status', 'Banco', 'Agência', 'Conta'],
        ...filteredData.map(p => [
            p.aluno,
            p.matricula,
            p.tipo,
            p.valor,
            p.vencimento,
            getStatusText(p.status),
            p.banco,
            p.agencia,
            p.conta
        ])
    ];
    
    const csvContent = csvData.map(row => row.join(',')).join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `relatorio_pagamentos_${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showToast('Relatório exportado com sucesso!', 'success');
}

// ===== EVENTO GLOBAL PARA EXPORTAÇÃO =====
if (document.getElementById('btnExportarRelatorio')) {
    document.getElementById('btnExportarRelatorio').addEventListener('click', exportarRelatorio);
}
