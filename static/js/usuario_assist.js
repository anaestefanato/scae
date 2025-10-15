// =========================
// GERENCIAR ASSISTENTES - JAVASCRIPT
// =========================

// ===== DADOS DOS ASSISTENTES (INJETADOS DO BACKEND) =====
// A variável 'assistentes' é injetada pelo template Jinja2 no HTML
// e está disponível globalmente

// ===== FUNÇÕES DE INICIALIZAÇÃO =====
document.addEventListener('DOMContentLoaded', function() {
    // Adicionar evento de busca ao pressionar Enter
    const searchInput = document.getElementById('searchAssistant');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchAssistant();
            }
        });
    }
});


// ===== FUNÇÃO PARA VISUALIZAR ASSISTENTE =====
function viewAssistant(id) {
    // Buscar o assistente pelo id (comparação flexível para string e número)
    const assistente = assistentes.find(a => a.id_usuario == id);
    
    if (assistente) {
        // Preencher os campos do modal
        document.getElementById('viewNome').textContent = assistente.nome || '';
        document.getElementById('viewMatricula').textContent = assistente.matricula || '';
        document.getElementById('viewSiape').textContent = assistente.siape || '';
        document.getElementById('viewEmail').textContent = assistente.email || '';
        document.getElementById('viewPerfil').textContent = assistente.perfil || 'Assistente Social';
        
        // Abrir o modal
        const modal = new bootstrap.Modal(document.getElementById('viewAssistantModal'));
        modal.show();
    } else {
        console.error('Assistente não encontrado:', id);
        console.log('IDs disponíveis:', assistentes.map(a => a.id_usuario));
    }
}

// ===== FUNÇÃO PARA EDITAR ASSISTENTE =====
function editAssistant(id) {
    // Redirecionar para página de edição
    window.location.href = `/admin/usuarios/assistente/editar/${id}`;
}

// ===== FUNÇÃO PARA EDITAR A PARTIR DO MODAL =====
function editAssistantFromModal() {
    // Buscar o assistente atual
    const assistente = assistentes.find(a => 
        a.nome === document.getElementById('viewNome').textContent
    );
    
    if (assistente) {
        // Fechar modal e redirecionar para edição
        const modal = bootstrap.Modal.getInstance(document.getElementById('viewAssistantModal'));
        modal.hide();
        window.location.href = `/admin/usuarios/assistente/editar/${assistente.id_usuario}`;
    }
}

// ===== VARIÁVEL PARA ARMAZENAR ID DO ASSISTENTE A SER EXCLUÍDO =====
let assistantToDeleteId = null;

// ===== FUNÇÃO PARA EXCLUIR ASSISTENTE =====
function deleteAssistant(id) {
    // Buscar o assistente pelo id (comparação flexível para string e número)
    const assistente = assistentes.find(a => a.id_usuario == id);
    
    if (assistente) {
        // Guardar o ID para exclusão
        assistantToDeleteId = id;
        
        // Preencher informações no modal
        document.getElementById('deleteAssistantName').textContent = assistente.nome;
        document.getElementById('deleteAssistantSiape').textContent = assistente.siape;
        document.getElementById('deleteAssistantEmail').textContent = assistente.email;
        
        // Abrir o modal
        const modal = new bootstrap.Modal(document.getElementById('deleteAssistantModal'));
        modal.show();
    }
}

// ===== FUNÇÃO PARA CONFIRMAR EXCLUSÃO =====
function confirmDeleteAssistant() {
    if (assistantToDeleteId) {
        // Criar formulário para enviar requisição DELETE via POST
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/admin/usuarios/assistente/excluir/${assistantToDeleteId}`;
        document.body.appendChild(form);
        form.submit();
    }
}

// ===== FUNÇÃO DE BUSCA =====
function searchAssistant() {
    const searchTerm = document.getElementById('searchAssistant').value.toLowerCase().trim();
    
    if (!searchTerm) {
        // Se não há termo de busca, mostrar todos
        location.reload();
        return;
    }
    
    // Buscar assistente por nome, matrícula ou SIAPE
    const results = assistentes.filter(a => 
        a.nome.toLowerCase().includes(searchTerm) ||
        a.matricula.toLowerCase().includes(searchTerm) ||
        a.siape.toLowerCase().includes(searchTerm) ||
        a.email.toLowerCase().includes(searchTerm)
    );
    
    // Atualizar tabela com resultados
    const tbody = document.getElementById('assistantsTableBody');
    tbody.innerHTML = '';
    
    if (results.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="4" class="text-center text-muted py-4">
                    <i class="bi bi-search fs-1 d-block mb-2"></i>
                    Nenhum assistente encontrado com "${searchTerm}"
                </td>
            </tr>
        `;
    } else {
        results.forEach(assistente => {
            tbody.innerHTML += `
                <tr>
                    <td><strong>${assistente.nome}</strong></td>
                    <td>${assistente.siape}</td>
                    <td>${assistente.email}</td>
                    <td>
                        <div class="action-buttons">
                            <button class="btn btn-sm btn-outline-info" onclick="viewAssistant(${assistente.id_usuario})" title="Visualizar">
                                <i class="bi bi-eye"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-secondary" onclick="editAssistant(${assistente.id_usuario})" title="Editar">
                                <i class="bi bi-pencil"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-danger" onclick="deleteAssistant(${assistente.id_usuario})" title="Excluir">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `;
        });
    }
    
    // Atualizar contagem
    document.getElementById('assistantsCount').textContent = results.length;
}

// ===== FUNÇÃO PARA LIMPAR BUSCA =====
function clearSearch() {
    // Limpar campo de busca
    document.getElementById('searchAssistant').value = '';
    
    // Mostrar todos os assistentes novamente
    const tbody = document.getElementById('assistantsTableBody');
    tbody.innerHTML = '';
    
    assistentes.forEach(assistente => {
        tbody.innerHTML += `
            <tr>
                <td><strong>${assistente.nome}</strong></td>
                <td>${assistente.siape}</td>
                <td>${assistente.email}</td>
                <td>
                    <div class="action-buttons">
                        <button class="btn btn-sm btn-outline-info" onclick="viewAssistant(${assistente.id_usuario})" title="Visualizar">
                            <i class="bi bi-eye"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-secondary" onclick="editAssistant(${assistente.id_usuario})" title="Editar">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteAssistant(${assistente.id_usuario})" title="Excluir">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    });
    
    // Atualizar contagem
    document.getElementById('assistantsCount').textContent = assistentes.length;
}

// ===== FUNÇÃO PARA EXPORTAR LISTA =====
function exportAssistantsList() {
    alert('Funcionalidade de exportação em desenvolvimento.');
}

// ===== FUNÇÃO PARA ATUALIZAR LISTA =====
function refreshAssistantsList() {
    location.reload();
}
