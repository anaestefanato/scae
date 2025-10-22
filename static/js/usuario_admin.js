/* ==========================================
   GERENCIAR ADMINISTRADORES - JAVASCRIPT
   ========================================== */

document.addEventListener('DOMContentLoaded', function() {
    // Configurar eventos dos formulários
    setupFormValidation();
    console.log('Sistema de gerenciamento de administradores inicializado');
});

// ===== VARIÁVEIS GLOBAIS =====
let adminToDeleteId = null;

// ===== BUSCAR ADMINISTRADOR =====
function searchAdmin() {
    const searchTerm = document.getElementById('searchAdmin').value.trim().toLowerCase();
    
    if (!searchTerm) {
        location.reload();
        return;
    }
    
    // Buscar na tabela existente
    const rows = document.querySelectorAll('#adminsTableBody tr');
    let visibleCount = 0;
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        if (text.includes(searchTerm)) {
            row.style.display = '';
            visibleCount++;
        } else {
            row.style.display = 'none';
        }
    });
    
    // Atualizar contagem
    document.getElementById('adminsCount').textContent = visibleCount;
    
    // Mostrar mensagem se não houver resultados
    if (visibleCount === 0) {
        const tbody = document.getElementById('adminsTableBody');
        const emptyRow = document.createElement('tr');
        emptyRow.id = 'noResultsRow';
        emptyRow.innerHTML = `
            <td colspan="4" class="text-center text-muted py-4">
                <i class="bi bi-search fs-1 d-block mb-2"></i>
                Nenhum administrador encontrado com "${searchTerm}"
            </td>
        `;
        tbody.appendChild(emptyRow);
    }
}

// ===== LIMPAR BUSCA =====
function clearSearch() {
    // Limpar campo de busca
    document.getElementById('searchAdmin').value = '';
    
    // Remover linha de "sem resultados" se existir
    const noResultsRow = document.getElementById('noResultsRow');
    if (noResultsRow) {
        noResultsRow.remove();
    }
    
    // Mostrar todas as linhas novamente
    const rows = document.querySelectorAll('#adminsTableBody tr');
    rows.forEach(row => {
        row.style.display = '';
    });
    
    // Restaurar contagem original
    const totalRows = document.querySelectorAll('#adminsTableBody tr:not(#noResultsRow)').length;
    document.getElementById('adminsCount').textContent = totalRows;
}

// ===== VISUALIZAR ADMINISTRADOR =====
function viewAdmin(adminId) {
    // Buscar dados da linha correspondente na tabela
    const rows = document.querySelectorAll('#adminsTableBody tr');
    let adminData = null;
    
    rows.forEach(row => {
        const viewButton = row.querySelector(`button[onclick*="viewAdmin('${adminId}')"]`);
        if (viewButton) {
            const cells = row.querySelectorAll('td');
            adminData = {
                nome: cells[0].textContent.trim(),
                email: cells[1].textContent.trim(),
                matricula: cells[2].textContent.trim()
            };
        }
    });
    
    if (adminData) {
        // Preencher os campos do modal
        document.getElementById('viewNome').textContent = adminData.nome;
        document.getElementById('viewMatricula').textContent = adminData.matricula;
        document.getElementById('viewEmail').textContent = adminData.email;
        document.getElementById('viewPerfil').textContent = 'Administrador';
        
        // Abrir o modal
        const modal = new bootstrap.Modal(document.getElementById('viewAdminModal'));
        modal.show();
    } else {
        alert('Erro ao carregar dados do administrador.');
    }
}

// ===== EXCLUIR ADMINISTRADOR =====
function deleteAdmin(adminId) {
    // Guardar o ID para exclusão
    adminToDeleteId = adminId;
    
    // Buscar dados da linha correspondente na tabela
    const rows = document.querySelectorAll('#adminsTableBody tr');
    let adminData = null;
    
    rows.forEach(row => {
        const deleteButton = row.querySelector(`button[onclick*="deleteAdmin('${adminId}')"]`);
        if (deleteButton) {
            const cells = row.querySelectorAll('td');
            adminData = {
                nome: cells[0].textContent.trim(),
                email: cells[1].textContent.trim(),
                matricula: cells[2].textContent.trim()
            };
        }
    });
    
    if (adminData) {
        // Preencher informações no modal
        document.getElementById('deleteAdminName').textContent = adminData.nome;
        document.getElementById('deleteAdminMatricula').textContent = adminData.matricula;
        document.getElementById('deleteAdminEmail').textContent = adminData.email;
        
        // Abrir o modal
        const modal = new bootstrap.Modal(document.getElementById('deleteAdminModal'));
        modal.show();
    } else {
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
    alert('Funcionalidade de exportação será implementada.');
}

// ===== ATUALIZAR LISTA =====
function refreshAdminsList() {
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
        const searchField = document.getElementById('searchAdmin');
        if (searchField && searchField.value) {
            clearSearch();
        }
    }
});