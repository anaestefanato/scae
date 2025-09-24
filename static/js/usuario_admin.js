/* ==========================================
   GERENCIAR ADMINISTRADORES - JAVASCRIPT
   ========================================== */

document.addEventListener('DOMContentLoaded', function() {
    // ===== INICIALIZAÇÃO =====
    initializeAdminManagement();
    loadAdminsList();
    checkPendingRequests();
});

// ===== DADOS MOCK DOS ADMINISTRADORES =====
const mockAdminsData = [
    {
        id: 1,
        nome: "João Silva Santos",
        email: "joao.santos@ifes.edu.br",
        nivel: "superadmin",
        dataCriacao: "2024-01-15",
        status: "ativo",
        ultimoLogin: "2024-09-23 14:30",
        permissoes: ["usuarios", "relatorios", "chamados", "mensagens"]
    },
    {
        id: 2,
        nome: "Maria Oliveira Costa",
        email: "maria.oliveira@ifes.edu.br",
        nivel: "admin",
        dataCriacao: "2024-02-22",
        status: "ativo",
        ultimoLogin: "2024-09-22 10:15",
        permissoes: ["relatorios", "chamados"]
    },
    {
        id: 3,
        nome: "Pedro Henrique Lima",
        email: "pedro.lima@ifes.edu.br",
        nivel: "admin",
        dataCriacao: "2024-03-10",
        status: "ativo",
        ultimoLogin: "2024-09-21 16:45",
        permissoes: ["usuarios", "mensagens"]
    },
    {
        id: 4,
        nome: "Ana Carolina Ferreira",
        email: "ana.ferreira@ifes.edu.br",
        nivel: "admin",
        dataCriacao: "2024-04-05",
        status: "inativo",
        ultimoLogin: "2024-08-30 09:20",
        permissoes: ["chamados"]
    }
];

// ===== VARIÁVEIS GLOBAIS =====
let currentAdminsData = mockAdminsData;
let currentFilter = '';
let selectedAdminId = null;

// ===== INICIALIZAÇÃO =====
function initializeAdminManagement() {
    // Configurar tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Configurar eventos dos formulários
    setupFormValidation();
    
    console.log('Sistema de gerenciamento de administradores inicializado');
}

// ===== CARREGAR LISTA DE ADMINISTRADORES =====
function loadAdminsList() {
    const tableBody = document.getElementById('adminsTableBody');
    const adminsCount = document.getElementById('adminsCount');
    
    if (!tableBody) {
        console.error('Elemento adminsTableBody não encontrado');
        return;
    }

    // Atualizar contador
    if (adminsCount) {
        adminsCount.textContent = currentAdminsData.length;
    }

    // Limpar tabela
    tableBody.innerHTML = '';

    // Adicionar administradores
    currentAdminsData.forEach(admin => {
        const row = createAdminRow(admin);
        tableBody.appendChild(row);
    });

    console.log(`Carregados ${currentAdminsData.length} administradores`);
}

// ===== CRIAR LINHA DA TABELA =====
function createAdminRow(admin) {
    const row = document.createElement('tr');
    
    // Determinar badge do nível
    const nivelBadge = admin.nivel === 'superadmin' 
        ? '<span class="badge bg-warning">Super Admin</span>'
        : '<span class="badge bg-primary">Admin</span>';
    
    // Determinar badge do status
    const statusBadge = admin.status === 'ativo'
        ? '<span class="badge bg-success">Ativo</span>'
        : '<span class="badge bg-danger">Inativo</span>';
    
    // Formatar data
    const dataFormatada = new Date(admin.dataCriacao).toLocaleDateString('pt-BR');
    
    row.innerHTML = `
        <td><strong>${admin.nome}</strong></td>
        <td>${admin.email}</td>
        <td>${nivelBadge}</td>
        <td>${dataFormatada}</td>
        <td>${statusBadge}</td>
        <td>
            <div class="action-buttons">
                <button class="btn btn-sm btn-outline-info" onclick="viewAdmin(${admin.id})" data-bs-toggle="tooltip" title="Visualizar">
                    <i class="bi bi-eye"></i>
                </button>
                <button class="btn btn-sm btn-outline-secondary" onclick="editAdmin(${admin.id})" data-bs-toggle="tooltip" title="Editar">
                    <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="deleteAdmin(${admin.id})" data-bs-toggle="tooltip" title="Excluir">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        </td>
    `;
    
    return row;
}

// ===== BUSCAR ADMINISTRADOR =====
function searchAdmin() {
    const searchTerm = document.getElementById('searchAdmin').value.trim().toLowerCase();
    
    if (!searchTerm) {
        alert('Por favor, digite um email para buscar.');
        return;
    }

    const foundAdmin = mockAdminsData.find(admin => 
        admin.email.toLowerCase().includes(searchTerm)
    );

    const searchResult = document.getElementById('searchResult');
    const searchResultContent = document.getElementById('searchResultContent');

    if (foundAdmin) {
        displaySearchResult(foundAdmin);
        searchResult.style.display = 'block';
    } else {
        searchResultContent.innerHTML = `
            <div class="alert alert-warning" role="alert">
                <i class="bi bi-exclamation-triangle me-2"></i>
                Nenhum administrador encontrado com o email "<strong>${searchTerm}</strong>".
            </div>
        `;
        searchResult.style.display = 'block';
    }
}

// ===== EXIBIR RESULTADO DA BUSCA =====
function displaySearchResult(admin) {
    const searchResultContent = document.getElementById('searchResultContent');
    
    const nivelBadge = admin.nivel === 'superadmin' 
        ? '<span class="badge bg-warning">Super Admin</span>'
        : '<span class="badge bg-primary">Admin</span>';
    
    const statusBadge = admin.status === 'ativo'
        ? '<span class="badge bg-success">Ativo</span>'
        : '<span class="badge bg-danger">Inativo</span>';
    
    const dataFormatada = new Date(admin.dataCriacao).toLocaleDateString('pt-BR');
    const ultimoLoginFormatado = new Date(admin.ultimoLogin).toLocaleString('pt-BR');
    
    searchResultContent.innerHTML = `
        <div class="row">
            <div class="col-md-6">
                <h6><i class="bi bi-person-check me-2"></i>Informações Básicas</h6>
                <p><strong>Nome:</strong> ${admin.nome}</p>
                <p><strong>Email:</strong> ${admin.email}</p>
                <p><strong>Nível:</strong> ${nivelBadge}</p>
                <p><strong>Status:</strong> ${statusBadge}</p>
            </div>
            <div class="col-md-6">
                <h6><i class="bi bi-clock me-2"></i>Informações de Acesso</h6>
                <p><strong>Data de Criação:</strong> ${dataFormatada}</p>
                <p><strong>Último Login:</strong> ${ultimoLoginFormatado}</p>
                <p><strong>Permissões:</strong> ${admin.permissoes.length} configuradas</p>
            </div>
        </div>
        <div class="mt-3">
            <button class="btn btn-sm btn-outline-info me-2" onclick="viewAdmin(${admin.id})">
                <i class="bi bi-eye me-1"></i>Ver Detalhes
            </button>
            <button class="btn btn-sm btn-outline-secondary me-2" onclick="editAdmin(${admin.id})">
                <i class="bi bi-pencil me-1"></i>Editar
            </button>
            <button class="btn btn-sm btn-outline-danger" onclick="deleteAdmin(${admin.id})">
                <i class="bi bi-trash me-1"></i>Excluir
            </button>
        </div>
    `;
}

// ===== LIMPAR BUSCA =====
function clearSearch() {
    document.getElementById('searchAdmin').value = '';
    document.getElementById('searchResult').style.display = 'none';
}

// ===== FILTRAR ADMINISTRADORES =====
function filterAdmins() {
    const filterValue = document.getElementById('filterCategory').value;
    currentFilter = filterValue;
    
    let filteredData = mockAdminsData;
    
    switch (filterValue) {
        case 'ativos':
            filteredData = mockAdminsData.filter(admin => admin.status === 'ativo');
            break;
        case 'inativos':
            filteredData = mockAdminsData.filter(admin => admin.status === 'inativo');
            break;
        case 'superadmin':
            filteredData = mockAdminsData.filter(admin => admin.nivel === 'superadmin');
            break;
        default:
            filteredData = mockAdminsData;
    }
    
    currentAdminsData = filteredData;
    loadAdminsList();
    
    console.log(`Filtro aplicado: ${filterValue}, ${filteredData.length} administradores encontrados`);
}

// ===== EXIBIR MODAL NOVO ADMINISTRADOR =====
function showAddAdminModal() {
    const modal = new bootstrap.Modal(document.getElementById('addAdminModal'));
    clearAddAdminForm();
    modal.show();
}

// ===== LIMPAR FORMULÁRIO =====
function clearAddAdminForm() {
    document.getElementById('addAdminForm').reset();
    
    // Desmarcar todas as permissões
    const checkboxes = document.querySelectorAll('#addAdminForm input[type="checkbox"]');
    checkboxes.forEach(checkbox => checkbox.checked = false);
}

// ===== SALVAR NOVO ADMINISTRADOR =====
function saveNewAdmin() {
    const form = document.getElementById('addAdminForm');
    
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    // Coletar dados do formulário
    const adminData = {
        id: mockAdminsData.length + 1,
        nome: document.getElementById('adminName').value,
        email: document.getElementById('adminEmail').value,
        nivel: document.getElementById('adminLevel').value,
        dataCriacao: new Date().toISOString().split('T')[0],
        status: 'ativo',
        ultimoLogin: new Date().toISOString(),
        permissoes: []
    };
    
    // Coletar permissões selecionadas
    const permissionCheckboxes = document.querySelectorAll('#addAdminForm input[type="checkbox"]:checked');
    permissionCheckboxes.forEach(checkbox => {
        adminData.permissoes.push(checkbox.value);
    });
    
    // Adicionar ao mock data
    mockAdminsData.push(adminData);
    currentAdminsData = mockAdminsData;
    
    // Recarregar lista
    loadAdminsList();
    
    // Fechar modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('addAdminModal'));
    modal.hide();
    
    // Mostrar mensagem de sucesso
    showNotification('Administrador adicionado com sucesso!', 'success');
    
    console.log('Novo administrador adicionado:', adminData);
}

// ===== VISUALIZAR ADMINISTRADOR =====
function viewAdmin(adminId) {
    const admin = mockAdminsData.find(a => a.id === adminId);
    if (!admin) {
        alert('Administrador não encontrado!');
        return;
    }
    
    // Por enquanto, mostrar um alert com os dados
    const permissoesFormatadas = admin.permissoes.join(', ');
    const dataFormatada = new Date(admin.dataCriacao).toLocaleDateString('pt-BR');
    const ultimoLoginFormatado = new Date(admin.ultimoLogin).toLocaleString('pt-BR');
    
    const info = `
Nome: ${admin.nome}
Email: ${admin.email}
Nível: ${admin.nivel === 'superadmin' ? 'Super Administrador' : 'Administrador'}
Status: ${admin.status === 'ativo' ? 'Ativo' : 'Inativo'}
Data de Criação: ${dataFormatada}
Último Login: ${ultimoLoginFormatado}
Permissões: ${permissoesFormatadas || 'Nenhuma'}
    `;
    
    alert('Detalhes do Administrador:\n\n' + info);
}

// ===== EDITAR ADMINISTRADOR =====
function editAdmin(adminId) {
    const admin = mockAdminsData.find(a => a.id === adminId);
    if (!admin) {
        alert('Administrador não encontrado!');
        return;
    }
    
    // Por enquanto, mostrar um alert
    alert(`Funcionalidade de edição para ${admin.nome} será implementada em breve.`);
}

// ===== EXCLUIR ADMINISTRADOR =====
function deleteAdmin(adminId) {
    const admin = mockAdminsData.find(a => a.id === adminId);
    if (!admin) {
        alert('Administrador não encontrado!');
        return;
    }
    
    selectedAdminId = adminId;
    
    // Preencher informações no modal de confirmação
    const adminToDeleteInfo = document.getElementById('adminToDeleteInfo');
    adminToDeleteInfo.innerHTML = `
        <strong>Nome:</strong> ${admin.nome}<br>
        <strong>Email:</strong> ${admin.email}<br>
        <strong>Nível:</strong> ${admin.nivel === 'superadmin' ? 'Super Administrador' : 'Administrador'}
    `;
    
    // Mostrar modal de confirmação
    const modal = new bootstrap.Modal(document.getElementById('deleteAdminModal'));
    modal.show();
}

// ===== CONFIRMAR EXCLUSÃO =====
function confirmDeleteAdmin() {
    if (!selectedAdminId) return;
    
    // Encontrar índice do administrador
    const adminIndex = mockAdminsData.findIndex(admin => admin.id === selectedAdminId);
    
    if (adminIndex === -1) {
        alert('Administrador não encontrado!');
        return;
    }
    
    const adminName = mockAdminsData[adminIndex].nome;
    
    // Remover da lista
    mockAdminsData.splice(adminIndex, 1);
    currentAdminsData = mockAdminsData;
    
    // Recarregar lista
    loadAdminsList();
    
    // Fechar modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('deleteAdminModal'));
    modal.hide();
    
    // Limpar seleção
    selectedAdminId = null;
    
    // Mostrar mensagem de sucesso
    showNotification(`Administrador "${adminName}" excluído com sucesso!`, 'success');
    
    console.log('Administrador excluído:', adminName);
}

// ===== EXPORTAR LISTA =====
function exportAdminsList() {
    // Simular exportação
    showNotification('Exportação iniciada! O arquivo será baixado em breve.', 'info');
    
    // Aqui seria implementada a lógica real de exportação
    console.log('Exportando lista de administradores...');
}

// ===== ATUALIZAR LISTA =====
function refreshAdminsList() {
    // Simular recarregamento
    showNotification('Lista atualizada!', 'info');
    
    // Resetar filtros
    document.getElementById('filterCategory').value = '';
    currentFilter = '';
    currentAdminsData = mockAdminsData;
    
    // Recarregar lista
    loadAdminsList();
    
    console.log('Lista de administradores atualizada');
}

// ===== VERIFICAR SOLICITAÇÕES PENDENTES =====
function checkPendingRequests() {
    // Simular verificação de solicitações pendentes
    console.log('Verificando solicitações pendentes...');
}

// ===== CONFIGURAR VALIDAÇÃO DE FORMULÁRIOS =====
function setupFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

// ===== MOSTRAR NOTIFICAÇÕES =====
function showNotification(message, type = 'info') {
    // Criar elemento de notificação
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Adicionar ao body
    document.body.appendChild(notification);
    
    // Remover automaticamente após 5 segundos
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// ===== EVENTOS DE TECLADO =====
document.addEventListener('keydown', function(event) {
    // Enter para buscar
    if (event.key === 'Enter' && event.target.id === 'searchAdmin') {
        event.preventDefault();
        searchAdmin();
    }
    
    // Escape para limpar busca
    if (event.key === 'Escape') {
        clearSearch();
    }
});

// ===== LOG DE INICIALIZAÇÃO =====
console.log('=== SISTEMA DE GERENCIAMENTO DE ADMINISTRADORES ===');
console.log('Versão: 1.0.0');
console.log('Data: ' + new Date().toLocaleString('pt-BR'));
console.log('Administradores carregados:', mockAdminsData.length);