/* ==========================================
   GERENCIAR ALUNOS - JAVASCRIPT
   ========================================== */

document.addEventListener('DOMContentLoaded', function() {
    // ===== INICIALIZAÇÃO =====
    initializeStudentManagement();
    loadStudentsList();
    checkPendingRequests();
});

// ===== DADOS MOCK DOS ALUNOS =====
const mockStudentsData = [
    {
        id: 1,
        nome: "Ana Maria Silva",
        matricula: "2024001001",
        cpf: "123.456.789-10",
        email: "ana.silva@aluno.ifes.edu.br",
        auxilios: ["alimentacao", "transporte"],
        status: "ativo",
        curso: "Informática",
        periodo: "6º",
        dataCadastro: "2024-02-15"
    },
    {
        id: 2,
        nome: "Carlos Eduardo Santos",
        matricula: "2024001002",
        cpf: "987.654.321-00",
        email: "carlos.santos@aluno.ifes.edu.br",
        auxilios: ["moradia"],
        status: "ativo",
        curso: "Eletrônica",
        periodo: "4º",
        dataCadastro: "2024-01-20"
    },
    {
        id: 3,
        nome: "Fernanda Costa Lima",
        matricula: "2024001003",
        cpf: "456.789.123-45",
        email: "fernanda.lima@aluno.ifes.edu.br",
        auxilios: ["material", "alimentacao"],
        status: "ativo",
        curso: "Mecânica",
        periodo: "2º",
        dataCadastro: "2024-03-10"
    },
    {
        id: 4,
        nome: "João Pedro Oliveira",
        matricula: "2024001004",
        cpf: "789.123.456-78",
        email: "joao.oliveira@aluno.ifes.edu.br",
        auxilios: [],
        status: "ativo",
        curso: "Informática",
        periodo: "8º",
        dataCadastro: "2024-01-05"
    },
    {
        id: 5,
        nome: "Maria Fernanda Souza",
        matricula: "2024001005",
        cpf: "321.654.987-21",
        email: "maria.souza@aluno.ifes.edu.br",
        auxilios: ["transporte", "material"],
        status: "inativo",
        curso: "Química",
        periodo: "5º",
        dataCadastro: "2023-08-15"
    }
];

// ===== FUNÇÃO DE INICIALIZAÇÃO =====
function initializeStudentManagement() {
    console.log('Inicializando gerenciamento de alunos...');
    
    // Configurar eventos
    setupEventListeners();
    
    // Atualizar contadores
    updateStatistics();
    
    // Configurar notificações
    setupNotifications();
}

// ===== CONFIGURAR EVENT LISTENERS =====
function setupEventListeners() {
    // Busca por matrícula
    const searchInput = document.getElementById('searchStudent');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchStudent();
            }
        });
    }
    
    // Filtro de categoria
    const filterSelect = document.getElementById('filterCategory');
    if (filterSelect) {
        filterSelect.addEventListener('change', filterStudents);
    }
    
    // Clique no badge de notificação
    const notificationBadge = document.getElementById('notificationBadge');
    if (notificationBadge) {
        notificationBadge.addEventListener('click', showPendingRequests);
    }
}

// ===== FUNÇÕES DE SOLICITAÇÕES PENDENTES =====
function approveRequest(requestId) {
    const requestItem = document.querySelector(`[data-request-id="${requestId}"]`);
    if (!requestItem) return;
    
    // Mostrar loading
    requestItem.classList.add('loading');
    
    // Simular aprovação
    setTimeout(() => {
        // Remover item da lista
        requestItem.style.transition = 'all 0.5s ease';
        requestItem.style.opacity = '0';
        requestItem.style.transform = 'translateX(-100%)';
        
        setTimeout(() => {
            requestItem.remove();
            updatePendingCount();
            showToast('Sucesso!', 'Solicitação aprovada com sucesso!', 'success');
        }, 500);
    }, 1000);
}

function rejectRequest(requestId) {
    const requestItem = document.querySelector(`[data-request-id="${requestId}"]`);
    if (!requestItem) return;
    
    // Confirmar rejeição
    if (!confirm('Tem certeza que deseja rejeitar esta solicitação?')) {
        return;
    }
    
    // Mostrar loading
    requestItem.classList.add('loading');
    
    // Simular rejeição
    setTimeout(() => {
        // Remover item da lista
        requestItem.style.transition = 'all 0.5s ease';
        requestItem.style.opacity = '0';
        requestItem.style.transform = 'translateX(-100%)';
        
        setTimeout(() => {
            requestItem.remove();
            updatePendingCount();
            showToast('Solicitação Rejeitada', 'A solicitação foi rejeitada.', 'warning');
        }, 500);
    }, 1000);
}

function viewRequestDetails(requestId) {
    // Dados mock para detalhes da solicitação
    const requestDetails = {
        1: {
            nome: "João Carlos Silva",
            matricula: "2025001234",
            cpf: "123.456.789-10",
            email: "joao.silva@aluno.ifes.edu.br",
            telefone: "(27) 99999-1234",
            curso: "Técnico em Informática",
            periodo: "1º",
            turno: "Integral",
            documentos: ["RG", "CPF", "Comprovante de Renda", "Histórico Escolar"],
            observacoes: "Primeira solicitação de cadastro no sistema."
        },
        2: {
            nome: "Maria Fernanda Santos",
            matricula: "2025001235",
            cpf: "987.654.321-00",
            email: "maria.santos@aluno.ifes.edu.br",
            telefone: "(27) 99999-5678",
            curso: "Técnico em Eletrônica",
            periodo: "1º",
            turno: "Vespertino",
            documentos: ["RG", "CPF", "Comprovante de Renda"],
            observacoes: "Documentos anexados corretamente."
        },
        3: {
            nome: "Pedro Henrique Oliveira",
            matricula: "2025001236",
            cpf: "456.789.123-45",
            email: "pedro.oliveira@aluno.ifes.edu.br",
            telefone: "(27) 99999-9012",
            curso: "Técnico em Mecânica",
            periodo: "1º",
            turno: "Matutino",
            documentos: ["RG", "CPF", "Comprovante de Matrícula"],
            observacoes: "Falta comprovante de renda familiar."
        }
    };
    
    const details = requestDetails[requestId];
    if (!details) return;
    
    // Criar modal com detalhes
    const modalHTML = `
    <div class="modal fade" id="requestDetailsModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">
                        <i class="bi bi-person-vcard me-2"></i>Detalhes da Solicitação
                    </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-6">
                            <h6 class="text-muted">DADOS PESSOAIS</h6>
                            <p><strong>Nome:</strong> ${details.nome}</p>
                            <p><strong>CPF:</strong> ${details.cpf}</p>
                            <p><strong>Email:</strong> ${details.email}</p>
                            <p><strong>Telefone:</strong> ${details.telefone}</p>
                        </div>
                        <div class="col-md-6">
                            <h6 class="text-muted">DADOS ACADÊMICOS</h6>
                            <p><strong>Matrícula:</strong> ${details.matricula}</p>
                            <p><strong>Curso:</strong> ${details.curso}</p>
                            <p><strong>Período:</strong> ${details.periodo}</p>
                            <p><strong>Turno:</strong> ${details.turno}</p>
                        </div>
                    </div>
                    <hr>
                    <div class="row">
                        <div class="col-12">
                            <h6 class="text-muted">DOCUMENTOS ANEXADOS</h6>
                            <div class="d-flex flex-wrap gap-2">
                                ${details.documentos.map(doc => `
                                    <span class="badge bg-secondary">${doc}</span>
                                `).join('')}
                            </div>
                        </div>
                    </div>
                    <hr>
                    <div class="row">
                        <div class="col-12">
                            <h6 class="text-muted">OBSERVAÇÕES</h6>
                            <p class="bg-light p-3 rounded">${details.observacoes}</p>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                    <button type="button" class="btn btn-danger" onclick="rejectRequest(${requestId}); bootstrap.Modal.getInstance(document.getElementById('requestDetailsModal')).hide();">
                        <i class="bi bi-x-lg me-1"></i>Rejeitar
                    </button>
                    <button type="button" class="btn btn-success" onclick="approveRequest(${requestId}); bootstrap.Modal.getInstance(document.getElementById('requestDetailsModal')).hide();">
                        <i class="bi bi-check-lg me-1"></i>Aprovar
                    </button>
                </div>
            </div>
        </div>
    </div>`;
    
    // Remover modal anterior se existir
    const existingModal = document.getElementById('requestDetailsModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Adicionar modal ao body
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Mostrar modal
    const modal = new bootstrap.Modal(document.getElementById('requestDetailsModal'));
    modal.show();
}

// ===== FUNÇÕES DE BUSCA E FILTRO =====
function searchStudent() {
    const searchTerm = document.getElementById('searchStudent').value.trim();
    
    if (!searchTerm) {
        showToast('Atenção', 'Digite uma matrícula para buscar.', 'warning');
        return;
    }
    
    // Simular busca
    const student = mockStudentsData.find(s => s.matricula === searchTerm);
    
    if (student) {
        displaySearchResult(student);
    } else {
        showToast('Não encontrado', 'Nenhum aluno encontrado com esta matrícula.', 'error');
        clearSearch();
    }
}

function displaySearchResult(student) {
    const searchResult = document.getElementById('searchResult');
    const searchResultContent = document.getElementById('searchResultContent');
    
    const auxiliosHTML = student.auxilios.length > 0 
        ? student.auxilios.map(auxilio => {
            const auxilioLabels = {
                'alimentacao': 'Alimentação',
                'transporte': 'Transporte',
                'moradia': 'Moradia',
                'material': 'Material'
            };
            return `<span class="auxilio-badge ${auxilio}">${auxilioLabels[auxilio]}</span>`;
        }).join(' ')
        : '<span class="text-muted">Nenhum auxílio ativo</span>';
    
    searchResultContent.innerHTML = `
        <div class="row">
            <div class="col-md-6">
                <h5 class="mb-3">${student.nome}</h5>
                <p><strong>Matrícula:</strong> ${student.matricula}</p>
                <p><strong>CPF:</strong> ${student.cpf}</p>
                <p><strong>Email:</strong> ${student.email}</p>
            </div>
            <div class="col-md-6">
                <p><strong>Curso:</strong> ${student.curso}</p>
                <p><strong>Período:</strong> ${student.periodo}</p>
                <p><strong>Status:</strong> <span class="badge bg-${student.status === 'ativo' ? 'success' : 'secondary'}">${student.status}</span></p>
                <p><strong>Auxílios Ativos:</strong></p>
                <div>${auxiliosHTML}</div>
            </div>
        </div>
        <hr>
        <div class="text-end">
            <button class="btn btn-outline-info me-2" onclick="viewStudent(${student.id})">
                <i class="bi bi-eye me-1"></i>Ver Detalhes
            </button>
            <button class="btn btn-outline-secondary me-2" onclick="editStudent(${student.id})">
                <i class="bi bi-pencil me-1"></i>Editar
            </button>
            <button class="btn btn-outline-danger" onclick="deleteStudent(${student.id})">
                <i class="bi bi-trash me-1"></i>Excluir
            </button>
        </div>
    `;
    
    searchResult.style.display = 'block';
    searchResult.scrollIntoView({ behavior: 'smooth' });
}

function clearSearch() {
    document.getElementById('searchStudent').value = '';
    document.getElementById('searchResult').style.display = 'none';
}

function filterStudents() {
    const filterValue = document.getElementById('filterCategory').value;
    const tableBody = document.getElementById('studentsTableBody');
    
    // Simular filtro
    let filteredStudents = mockStudentsData;
    
    if (filterValue) {
        switch (filterValue) {
            case 'ativos':
                filteredStudents = mockStudentsData.filter(s => s.status === 'ativo');
                break;
            case 'beneficiados':
                filteredStudents = mockStudentsData.filter(s => s.auxilios.length > 0);
                break;
            case 'alimentacao':
                filteredStudents = mockStudentsData.filter(s => s.auxilios.includes('alimentacao'));
                break;
            case 'transporte':
                filteredStudents = mockStudentsData.filter(s => s.auxilios.includes('transporte'));
                break;
            case 'moradia':
                filteredStudents = mockStudentsData.filter(s => s.auxilios.includes('moradia'));
                break;
            case 'material':
                filteredStudents = mockStudentsData.filter(s => s.auxilios.includes('material'));
                break;
            case 'inativos':
                filteredStudents = mockStudentsData.filter(s => s.status === 'inativo');
                break;
        }
    }
    
    updateStudentsTable(filteredStudents);
    updateStudentsCount(filteredStudents.length);
}

// ===== FUNÇÕES DE GERENCIAMENTO DE ALUNOS =====
function viewStudent(studentId) {
    const student = mockStudentsData.find(s => s.id === studentId);
    if (!student) return;
    
    // Criar modal de visualização
    const modalHTML = `
    <div class="modal fade" id="viewStudentModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">
                        <i class="bi bi-person-badge me-2"></i>Detalhes do Aluno
                    </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-6">
                            <h6 class="text-muted">DADOS PESSOAIS</h6>
                            <p><strong>Nome:</strong> ${student.nome}</p>
                            <p><strong>CPF:</strong> ${student.cpf}</p>
                            <p><strong>Email:</strong> ${student.email}</p>
                        </div>
                        <div class="col-md-6">
                            <h6 class="text-muted">DADOS ACADÊMICOS</h6>
                            <p><strong>Matrícula:</strong> ${student.matricula}</p>
                            <p><strong>Curso:</strong> ${student.curso}</p>
                            <p><strong>Período:</strong> ${student.periodo}</p>
                        </div>
                    </div>
                    <hr>
                    <div class="row">
                        <div class="col-md-6">
                            <h6 class="text-muted">STATUS</h6>
                            <p><span class="badge bg-${student.status === 'ativo' ? 'success' : 'secondary'}">${student.status.toUpperCase()}</span></p>
                        </div>
                        <div class="col-md-6">
                            <h6 class="text-muted">DATA DE CADASTRO</h6>
                            <p>${new Date(student.dataCadastro).toLocaleDateString('pt-BR')}</p>
                        </div>
                    </div>
                    <hr>
                    <div class="row">
                        <div class="col-12">
                            <h6 class="text-muted">AUXÍLIOS ATIVOS</h6>
                            <div class="d-flex flex-wrap gap-2">
                                ${student.auxilios.length > 0 
                                    ? student.auxilios.map(auxilio => {
                                        const auxilioLabels = {
                                            'alimentacao': 'Alimentação',
                                            'transporte': 'Transporte',
                                            'moradia': 'Moradia',
                                            'material': 'Material'
                                        };
                                        return `<span class="auxilio-badge ${auxilio}">${auxilioLabels[auxilio]}</span>`;
                                    }).join('')
                                    : '<span class="text-muted">Nenhum auxílio ativo</span>'
                                }
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                    <button type="button" class="btn btn-primary" onclick="editStudent(${student.id}); bootstrap.Modal.getInstance(document.getElementById('viewStudentModal')).hide();">
                        <i class="bi bi-pencil me-1"></i>Editar
                    </button>
                </div>
            </div>
        </div>
    </div>`;
    
    // Remover modal anterior se existir
    const existingModal = document.getElementById('viewStudentModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Adicionar modal ao body
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Mostrar modal
    const modal = new bootstrap.Modal(document.getElementById('viewStudentModal'));
    modal.show();
}

function editStudent(studentId) {
    showToast('Em desenvolvimento', 'Funcionalidade de edição em desenvolvimento.', 'info');
}

function deleteStudent(studentId) {
    const student = mockStudentsData.find(s => s.id === studentId);
    if (!student) return;
    
    if (confirm(`Tem certeza que deseja excluir o aluno ${student.nome}?\n\nEsta ação não pode ser desfeita.`)) {
        // Simular exclusão
        showToast('Sucesso!', 'Aluno excluído com sucesso!', 'success');
        
        // Remover da lista mock (em um caso real, faria requisição para API)
        const index = mockStudentsData.findIndex(s => s.id === studentId);
        if (index > -1) {
            mockStudentsData.splice(index, 1);
            loadStudentsList();
            updateStatistics();
        }
    }
}

// ===== FUNÇÕES DE CARREGAMENTO E ATUALIZAÇÃO =====
function loadStudentsList() {
    updateStudentsTable(mockStudentsData);
}

function updateStudentsTable(students) {
    const tableBody = document.getElementById('studentsTableBody');
    
    tableBody.innerHTML = students.map(student => {
        const auxiliosHTML = student.auxilios.length > 0 
            ? student.auxilios.map(auxilio => {
                const auxilioLabels = {
                    'alimentacao': 'Alimentação',
                    'transporte': 'Transporte',
                    'moradia': 'Moradia',
                    'material': 'Material'
                };
                return `<span class="auxilio-badge ${auxilio}">${auxilioLabels[auxilio]}</span>`;
            }).join(' ')
            : '<span class="text-muted">Nenhum</span>';
        
        return `
            <tr>
                <td><strong>${student.nome}</strong></td>
                <td>${student.matricula}</td>
                <td>${student.cpf}</td>
                <td>${auxiliosHTML}</td>
                <td><span class="badge bg-${student.status === 'ativo' ? 'success' : 'secondary'}">${student.status}</span></td>
                <td>
                    <div class="action-buttons">
                        <button class="btn btn-sm btn-outline-info" onclick="viewStudent(${student.id})">
                            <i class="bi bi-eye"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-secondary" onclick="editStudent(${student.id})">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteStudent(${student.id})">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }).join('');
}

// ===== FUNÇÕES AUXILIARES =====
function updateStatistics() {
    const activeStudents = mockStudentsData.filter(s => s.status === 'ativo').length;
    const beneficiatedStudents = mockStudentsData.filter(s => s.auxilios.length > 0).length;
    const totalAuxilios = mockStudentsData.reduce((total, student) => total + student.auxilios.length, 0);
    
    // Atualizar cards de estatísticas
    const statsCards = document.querySelectorAll('.stats-card .number');
    if (statsCards[0]) statsCards[0].textContent = activeStudents;
    if (statsCards[2]) statsCards[2].textContent = beneficiatedStudents;
    if (statsCards[3]) statsCards[3].textContent = totalAuxilios;
}

function updateStudentsCount(count) {
    const studentsCount = document.getElementById('studentsCount');
    if (studentsCount) {
        studentsCount.textContent = count;
    }
}

function updatePendingCount() {
    const pendingItems = document.querySelectorAll('.pending-request-item').length;
    const pendingCountBadge = document.getElementById('pendingCount');
    const pendingRequestsCount = document.getElementById('pendingRequestsCount');
    
    if (pendingCountBadge) {
        pendingCountBadge.textContent = pendingItems;
        pendingCountBadge.style.display = pendingItems > 0 ? 'inline' : 'none';
    }
    
    if (pendingRequestsCount) {
        pendingRequestsCount.textContent = pendingItems;
    }
    
    // Atualizar card de estatísticas
    const statsCards = document.querySelectorAll('.stats-card .number');
    if (statsCards[1]) statsCards[1].textContent = pendingItems;
}

function checkPendingRequests() {
    // Simular verificação de novas solicitações
    setTimeout(() => {
        updatePendingCount();
    }, 1000);
}

function refreshPendingRequests() {
    showToast('Atualizado!', 'Lista de solicitações atualizada.', 'success');
}

function refreshStudentsList() {
    showToast('Atualizado!', 'Lista de alunos atualizada.', 'success');
    loadStudentsList();
}

function exportStudentsList() {
    showToast('Exportando...', 'Gerando arquivo para download.', 'info');
    // Simular export
    setTimeout(() => {
        showToast('Concluído!', 'Lista exportada com sucesso!', 'success');
    }, 2000);
}

function showPendingRequests() {
    const pendingSection = document.querySelector('.pending-requests-card');
    if (pendingSection) {
        pendingSection.scrollIntoView({ behavior: 'smooth' });
    }
}

// ===== FUNÇÃO PARA MOSTRAR TOAST =====
function showToast(title, message, type = 'info') {
    // Criar container de toasts se não existir
    let toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toastContainer';
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }

    const toastId = 'toast_' + Date.now();
    const iconClass = type === 'success' ? 'bi-check-circle' : 
                     type === 'error' ? 'bi-exclamation-triangle' : 
                     type === 'warning' ? 'bi-exclamation-triangle' : 'bi-info-circle';
    const bgClass = type === 'success' ? 'bg-success' : 
                   type === 'error' ? 'bg-danger' : 
                   type === 'warning' ? 'bg-warning' : 'bg-primary';

    const toastHTML = `
    <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header ${bgClass} text-white">
            <i class="${iconClass} me-2"></i>
            <strong class="me-auto">${title}</strong>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    </div>`;

    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 4000
    });
    
    toast.show();
    
    // Remover toast após ser escondido
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}
