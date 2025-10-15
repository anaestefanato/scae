/* ==========================================
   GERENCIAR ADMINISTRADORES - JAVASCRIPT
   Dados dinâmicos carregados via Jinja2
   ========================================== */

// ===== CARREGAR DADOS DO HTML =====
// Buscar dados dos administradores do atributo data-administradores
const mainContent = document.getElementById('mainContent');
const administradores = mainContent ? JSON.parse(mainContent.getAttribute('data-administradores') || '[]') : [];

document.addEventListener('DOMContentLoaded', function() {
    // ===== INICIALIZAÇÃO =====
    initializeAdminManagement();
});

// ===== VARIÁVEIS GLOBAIS =====
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

// ===== BUSCAR ADMINISTRADOR =====
function searchAdmin() {
    const searchTerm = document.getElementById('searchAdmin').value.trim().toLowerCase();
    
    if (!searchTerm) {
        // Se não há termo de busca, mostrar todos
        location.reload();
        return;
    }
    
    // Buscar administrador por nome, matrícula ou email
    const results = administradores.filter(a => 
        a.nome.toLowerCase().includes(searchTerm) ||
        a.matricula.toLowerCase().includes(searchTerm) ||
        a.email.toLowerCase().includes(searchTerm)
    );
    
    // Atualizar tabela com resultados
    const tbody = document.getElementById('adminsTableBody');
    tbody.innerHTML = '';
    
    if (results.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="4" class="text-center text-muted py-4">
                    <i class="bi bi-search fs-1 d-block mb-2"></i>
                    Nenhum administrador encontrado com "${searchTerm}"
                </td>
            </tr>
        `;
    } else {
        results.forEach(administrador => {
            tbody.innerHTML += `
                <tr>
                    <td><strong>${administrador.nome}</strong></td>
                    <td>${administrador.email}</td>
                    <td>${administrador.matricula}</td>
                    <td>
                        <div class="action-buttons">
                            <button class="btn btn-sm btn-outline-info" onclick="viewAdmin(${administrador.id_usuario})" title="Visualizar">
                                <i class="bi bi-eye"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-danger" onclick="deleteAdmin(${administrador.id_usuario})" title="Excluir">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `;
        });
    }
    
    // Atualizar contagem
    document.getElementById('adminsCount').textContent = results.length;
}

// ===== LIMPAR BUSCA =====
function clearSearch() {
    // Limpar campo de busca
    document.getElementById('searchAdmin').value = '';
    
    // Mostrar todos os administradores novamente
    const tbody = document.getElementById('adminsTableBody');
    tbody.innerHTML = '';
    
    administradores.forEach(administrador => {
        tbody.innerHTML += `
            <tr>
                <td><strong>${administrador.nome}</strong></td>
                <td>${administrador.email}</td>
                <td>${administrador.matricula}</td>
                <td>
                    <div class="action-buttons">
                        <button class="btn btn-sm btn-outline-info" onclick="viewAdmin(${administrador.id_usuario})" title="Visualizar">
                            <i class="bi bi-eye"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteAdmin(${administrador.id_usuario})" title="Excluir">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    });
    
    // Atualizar contagem
    document.getElementById('adminsCount').textContent = administradores.length;
}

// ===== VISUALIZAR ADMINISTRADOR =====
function viewAdmin(adminId) {
    console.log('Visualizar admin:', adminId);

    
    // Buscar o administrador pelo id (comparação flexível para string e número)
    const administrador = administradores.find(a => a.id_usuario == adminId);
    
    if (administrador) {
        // Preencher os campos do modal
        document.getElementById('viewNome').textContent = administrador.nome || '';
        document.getElementById('viewMatricula').textContent = administrador.matricula || '';
        document.getElementById('viewEmail').textContent = administrador.email || '';
        
        // Determinar o tipo de perfil
        let perfil = 'Administrador';
        if (administrador.tipo_admin === 'super') {
            perfil = 'Super Administrador';
        }
        document.getElementById('viewPerfil').textContent = perfil;
        
        // Abrir o modal
        const modal = new bootstrap.Modal(document.getElementById('viewAdminModal'));
        modal.show();
    } else {
        console.error('Administrador não encontrado:', adminId);
        console.log('IDs disponíveis:', administradores.map(a => a.id_usuario));
        alert('Erro ao carregar dados do administrador.');
    }
}

// ===== EDITAR ADMINISTRADOR =====
function editAdmin(adminId) {
    console.log('Editar admin:', adminId);
    alert(`Funcionalidade de edição do admin ID ${adminId} será implementada.`);
}

// ===== EXCLUIR ADMINISTRADOR =====
let adminToDeleteId = null;

function deleteAdmin(adminId) {
    // Buscar o administrador pelo id (comparação flexível para string e número)
    const administrador = administradores.find(a => a.id_usuario == adminId);
    
    if (administrador) {
        // Guardar o ID para exclusão
        adminToDeleteId = adminId;
        
        // Preencher informações no modal
        document.getElementById('deleteAdminName').textContent = administrador.nome;
        document.getElementById('deleteAdminMatricula').textContent = administrador.matricula;
        document.getElementById('deleteAdminEmail').textContent = administrador.email;
        
        // Abrir o modal
        const modal = new bootstrap.Modal(document.getElementById('deleteAdminModal'));
        modal.show();
    } else {
        console.error('Administrador não encontrado:', adminId);
        alert('Erro ao buscar dados do administrador.');
    }
}

// ===== CONFIRMAR EXCLUSÃO =====
function confirmDeleteAdmin() {
    if (adminToDeleteId) {
        // Criar formulário para enviar requisição DELETE via POST
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/admin/usuarios/admin/excluir/${adminToDeleteId}`;
        document.body.appendChild(form);
        form.submit();
    } else {
        alert('Nenhum administrador selecionado para exclusão.');
    }
}

// ===== EXPORTAR LISTA =====
function exportAdminsList() {
    console.log('Exportar lista de administradores');
    alert('Funcionalidade de exportação será implementada.');
}

// ===== ATUALIZAR LISTA =====
function refreshAdminsList() {
    console.log('Atualizando lista de administradores');
    location.reload();
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

console.log('Sistema de gerenciamento de administradores carregado com sucesso!');