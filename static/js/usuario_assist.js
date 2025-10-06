// =========================
// GERENCIAR ASSISTENTES - JAVASCRIPT
// =========================

// ===== DADOS MOCK DOS ASSISTENTES =====
let assistants = [
    {
        id: 1,
        nome: "Dra. Maria Silva Costa",
        matricula: "AS001",
        email: "maria.costa@ifes.edu.br",
        siape: "12345678"
    },
    {
        id: 2,
        nome: "Dr. João Pedro Santos",
        matricula: "AS002",
        email: "joao.santos@ifes.edu.br",
        siape: "87654321"
    },
    {
        id: 3,
        nome: "Dra. Ana Beatriz Lima",
        matricula: "AS003",
        email: "ana.lima@ifes.edu.br",
        siape: "45678912"
    },
    {
        id: 4,
        nome: "Dra. Carla Fernandes",
        matricula: "AS004",
        email: "carla.fernandes@ifes.edu.br",
        siape: "78912345"
    },
    {
        id: 5,
        nome: "Dr. Rafael Oliveira",
        matricula: "AS005",
        email: "rafael.oliveira@ifes.edu.br",
        siape: "32165498"
    }
];

let filteredAssistants = [...assistants];

// ===== FUNÇÕES DE INICIALIZAÇÃO =====
document.addEventListener('DOMContentLoaded', function() {
    loadAssistantsList();
    updateStatistics();
});

// ===== FUNÇÃO PARA CARREGAR LISTA DE ASSISTENTES =====
function loadAssistantsList() {
    const tableBody = document.getElementById('assistantsTableBody');
    if (!tableBody) return;

    tableBody.innerHTML = '';

    filteredAssistants.forEach(assistant => {
        const row = createAssistantRow(assistant);
        tableBody.appendChild(row);
    });

    updateAssistantsCount();
}

// ===== FUNÇÃO PARA CRIAR LINHA DA TABELA =====
function createAssistantRow(assistant) {
    const row = document.createElement('tr');
    
    row.innerHTML = `
        <td><strong>${assistant.nome}</strong></td>
        <td>${assistant.matricula}</td>
        <td>${assistant.email}</td>
        <td>${assistant.siape}</td>
        <td>
            <div class="action-buttons">
                <button class="btn btn-sm btn-outline-info" onclick="viewAssistant(${assistant.id})" title="Visualizar">
                    <i class="bi bi-eye"></i>
                </button>
                <button class="btn btn-sm btn-outline-secondary" onclick="editAssistant(${assistant.id})" title="Editar">
                    <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="deleteAssistant(${assistant.id})" title="Excluir">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        </td>
    `;
    
    return row;
}

// ===== FUNÇÃO PARA ATUALIZAR ESTATÍSTICAS =====
function updateStatistics() {
    const totalAssistentes = assistants.length;
    const totalEmails = assistants.filter(a => a.email).length;
    const totalMatriculas = assistants.filter(a => a.matricula).length;
    const totalSiape = assistants.filter(a => a.siape).length;
    
    // Atualizar cards de estatísticas
    document.querySelector('.assistentes-ativos .number').textContent = totalAssistentes;
    document.querySelector('.casos-atendidos .number').textContent = totalEmails;
    document.querySelector('.inscricoes-analisadas .number').textContent = totalMatriculas;
    document.querySelector('.media-produtividade .number').textContent = totalSiape;
}

// ===== FUNÇÃO PARA ATUALIZAR CONTADOR =====
function updateAssistantsCount() {
    const count = document.getElementById('assistantsCount');
    if (count) {
        count.textContent = filteredAssistants.length;
    }
}

// ===== FUNÇÃO DE BUSCA =====
function searchAssistant() {
    const searchTerm = document.getElementById('searchAssistant').value.toLowerCase().trim();
    
    if (!searchTerm) {
        showToast('Por favor, digite um termo para buscar.', 'warning');
        return;
    }

    const results = assistants.filter(assistant => 
        assistant.nome.toLowerCase().includes(searchTerm) ||
        assistant.matricula.toLowerCase().includes(searchTerm) ||
        assistant.email.toLowerCase().includes(searchTerm) ||
        assistant.siape.toLowerCase().includes(searchTerm)
    );

    if (results.length === 0) {
        showToast('Nenhum assistente encontrado com o termo pesquisado.', 'info');
        clearSearch();
        return;
    }

    if (results.length === 1) {
        showSearchResult(results[0]);
    } else {
        filteredAssistants = results;
        loadAssistantsList();
        showToast(`${results.length} assistentes encontrados.`, 'success');
    }
}

// ===== FUNÇÃO PARA MOSTRAR RESULTADO DA BUSCA =====
function showSearchResult(assistant) {
    const searchResult = document.getElementById('searchResult');
    const searchContent = document.getElementById('searchResultContent');
    
    searchContent.innerHTML = `
        <div class="assistant-detail-card">
            <h6><i class="bi bi-person-gear me-2"></i>Informações do Assistente</h6>
            <div class="row">
                <div class="col-md-6">
                    <div class="info-row">
                        <div class="info-label">Nome Completo:</div>
                        <div class="info-value">${assistant.nome}</div>
                    </div>
                    <div class="info-row">
                        <div class="info-label">Matrícula:</div>
                        <div class="info-value">${assistant.matricula}</div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-row">
                        <div class="info-label">Email:</div>
                        <div class="info-value">${assistant.email}</div>
                    </div>
                    <div class="info-row">
                        <div class="info-label">siape:</div>
                        <div class="info-value">${assistant.siape}</div>
                    </div>
                </div>
            </div>
            <div class="mt-3">
                <button class="btn btn-outline-secondary me-2" onclick="editAssistant(${assistant.id})">
                    <i class="bi bi-pencil me-1"></i>Editar
                </button>
                <button class="btn btn-outline-danger" onclick="deleteAssistant(${assistant.id})">
                    <i class="bi bi-trash me-1"></i>Excluir
                </button>
            </div>
        </div>
    `;
    
    searchResult.style.display = 'block';
    searchResult.scrollIntoView({ behavior: 'smooth' });
}

// ===== FUNÇÃO PARA LIMPAR BUSCA =====
function clearSearch() {
    document.getElementById('searchAssistant').value = '';
    document.getElementById('searchResult').style.display = 'none';
    filteredAssistants = [...assistants];
    loadAssistantsList();
}

// ===== FUNÇÃO PARA ABRIR MODAL DE NOVO ASSISTENTE =====
function openNewAssistantModal() {
    const modalHtml = `
        <div class="modal fade" id="newAssistantModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="bi bi-person-plus me-2"></i>Cadastrar Novo Assistente
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="newAssistantForm">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-floating mb-3">
                                        <input type="text" class="form-control" id="newNome" required>
                                        <label for="newNome">Nome Completo</label>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="form-floating mb-3">
                                        <input type="text" class="form-control" id="newMatricula" required>
                                        <label for="newMatricula">Matrícula</label>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-floating mb-3">
                                        <input type="email" class="form-control" id="newEmail" required>
                                        <label for="newEmail">Email</label>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="form-floating mb-3">
                                        <input type="text" class="form-control" id="newSiap" required>
                                        <label for="newSiap">siape</label>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-success" onclick="saveNewAssistant()">
                            <i class="bi bi-check-lg me-1"></i>Cadastrar Assistente
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('newAssistantModal'));
    modal.show();
    
    // Remove o modal do DOM quando fechado
    document.getElementById('newAssistantModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

// ===== FUNÇÃO PARA SALVAR NOVO ASSISTENTE =====
function saveNewAssistant() {
    const form = document.getElementById('newAssistantForm');
    
    // Validar formulário
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const newAssistant = {
        id: Date.now(), // ID temporário
        nome: document.getElementById('newNome').value,
        matricula: document.getElementById('newMatricula').value,
        email: document.getElementById('newEmail').value,
        siape: document.getElementById('newSiap').value
    };
    
    // Verificar se matrícula já existe
    if (assistants.find(a => a.matricula === newAssistant.matricula)) {
        showToast('Matrícula já cadastrada no sistema.', 'error');
        return;
    }
    
    // Verificar se SIAPE já existe
    if (assistants.find(a => a.siape === newAssistant.siape)) {
        showToast('SIAPE já cadastrado no sistema.', 'error');
        return;
    }
    
    // Adicionar à lista
    assistants.push(newAssistant);
    filteredAssistants = [...assistants];
    
    // Atualizar interface
    loadAssistantsList();
    updateStatistics();
    
    // Fechar modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('newAssistantModal'));
    modal.hide();
    
    showToast('Assistente cadastrado com sucesso!', 'success');
}

// ===== FUNÇÃO PARA VISUALIZAR ASSISTENTE =====
function viewAssistant(id) {
    const assistant = assistants.find(a => a.id === id);
    if (!assistant) return;
    
    const modalHtml = `
        <div class="modal fade" id="viewAssistantModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="bi bi-person-gear me-2"></i>Detalhes do Assistente
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="assistant-detail-card">
                            <h6><i class="bi bi-person me-2"></i>Informações do Assistente</h6>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="info-row">
                                        <div class="info-label">Nome Completo:</div>
                                        <div class="info-value">${assistant.nome}</div>
                                    </div>
                                    <div class="info-row">
                                        <div class="info-label">Matrícula:</div>
                                        <div class="info-value">${assistant.matricula}</div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="info-row">
                                        <div class="info-label">Email:</div>
                                        <div class="info-value">${assistant.email}</div>
                                    </div>
                                    <div class="info-row">
                                        <div class="info-label">siape:</div>
                                        <div class="info-value">${assistant.siape}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                        <button type="button" class="btn btn-outline-primary" onclick="editAssistant(${assistant.id}); bootstrap.Modal.getInstance(document.getElementById('viewAssistantModal')).hide();">
                            <i class="bi bi-pencil me-1"></i>Editar
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('viewAssistantModal'));
    modal.show();
    
    // Remove o modal do DOM quando fechado
    document.getElementById('viewAssistantModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

// ===== FUNÇÃO PARA EDITAR ASSISTENTE =====
function editAssistant(id) {
    const assistant = assistants.find(a => a.id === id);
    if (!assistant) return;
    
    const modalHtml = `
        <div class="modal fade" id="editAssistantModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="bi bi-pencil me-2"></i>Editar Assistente
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="editAssistantForm">
                            <div class="form-floating mb-3">
                                <input type="text" class="form-control" id="editNome" value="${assistant.nome}" required>
                                <label for="editNome">Nome Completo</label>
                            </div>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-floating mb-3">
                                        <input type="text" class="form-control" id="editMatricula" value="${assistant.matricula}" required>
                                        <label for="editMatricula">Matrícula</label>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="form-floating mb-3">
                                        <input type="email" class="form-control" id="editEmail" value="${assistant.email}" required>
                                        <label for="editEmail">Email</label>
                                    </div>
                                </div>
                            </div>
                            <div class="form-floating mb-3">
                                <input type="text" class="form-control" id="editSiap" value="${assistant.siape}" required>
                                <label for="editSiap">siape</label>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-success" onclick="saveEditAssistant(${assistant.id})">
                            <i class="bi bi-check-lg me-1"></i>Salvar Alterações
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('editAssistantModal'));
    modal.show();
    
    // Remove o modal do DOM quando fechado
    document.getElementById('editAssistantModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

// ===== FUNÇÃO PARA SALVAR EDIÇÃO =====
function saveEditAssistant(id) {
    const form = document.getElementById('editAssistantForm');
    
    // Validar formulário
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const assistantIndex = assistants.findIndex(a => a.id === id);
    if (assistantIndex === -1) return;
    
    // Atualizar dados
    assistants[assistantIndex] = {
        ...assistants[assistantIndex],
        nome: document.getElementById('editNome').value,
        matricula: document.getElementById('editMatricula').value,
        email: document.getElementById('editEmail').value,
        siape: document.getElementById('editSiap').value
    };
    
    // Atualizar lista filtrada
    filteredAssistants = [...assistants];
    
    // Atualizar interface
    loadAssistantsList();
    updateStatistics();
    
    // Fechar modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('editAssistantModal'));
    modal.hide();
    
    showToast('Dados do assistente atualizados com sucesso!', 'success');
}

// ===== FUNÇÃO PARA EXCLUIR ASSISTENTE =====
function deleteAssistant(id) {
    const assistant = assistants.find(a => a.id === id);
    if (!assistant) return;
    
    const modalHtml = `
        <div class="modal fade" id="deleteAssistantModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header bg-danger text-white">
                        <h5 class="modal-title">
                            <i class="bi bi-exclamation-triangle me-2"></i>Confirmar Exclusão
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p>Tem certeza que deseja excluir o assistente <strong>${assistant.nome}</strong>?</p>
                        <p class="text-muted">Esta ação não pode ser desfeita. Todos os dados relacionados a este assistente serão removidos permanentemente.</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-danger" onclick="confirmDeleteAssistant(${assistant.id})">
                            <i class="bi bi-trash me-1"></i>Excluir Assistente
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById('deleteAssistantModal'));
    modal.show();
    
    // Remove o modal do DOM quando fechado
    document.getElementById('deleteAssistantModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

// ===== FUNÇÃO PARA CONFIRMAR EXCLUSÃO =====
function confirmDeleteAssistant(id) {
    const assistantIndex = assistants.findIndex(a => a.id === id);
    if (assistantIndex === -1) return;
    
    const assistantName = assistants[assistantIndex].nome;
    
    // Remover da lista
    assistants.splice(assistantIndex, 1);
    filteredAssistants = [...assistants];
    
    // Atualizar interface
    loadAssistantsList();
    updateStatistics();
    
    // Fechar modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('deleteAssistantModal'));
    modal.hide();
    
    showToast(`Assistente ${assistantName} excluído com sucesso.`, 'success');
}

// ===== FUNÇÃO PARA EXPORTAR LISTA =====
function exportAssistantsList() {
    showToast('Exportação iniciada. O arquivo será baixado em breve.', 'info');
    
    // Simular delay de exportação
    setTimeout(() => {
        showToast('Lista de assistentes exportada com sucesso!', 'success');
    }, 2000);
}

// ===== FUNÇÃO PARA ATUALIZAR LISTA =====
function refreshAssistantsList() {
    showToast('Atualizando lista de assistentes...', 'info');
    
    // Simular delay de carregamento
    setTimeout(() => {
        loadAssistantsList();
        updateStatistics();
        showToast('Lista atualizada com sucesso!', 'success');
    }, 1000);
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
