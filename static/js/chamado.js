// Funções de filtro
function submitFilters() {
    document.getElementById('filterForm').submit();
}

function clearFilters() {
    window.location.href = '/admin/chamados';
}

function refreshTickets() {
    window.location.reload();
}

// Ticket management functions
function viewTicket(ticketId) {
    // Buscar detalhes do chamado via AJAX
    fetch(`/admin/chamados/${ticketId}/detalhes`)
        .then(response => response.json())
        .then(data => {
            // Preencher modal com dados
            document.getElementById('modalTicketId').textContent = `#${data.chamado.id_chamado}`;
            document.getElementById('modalTicketTitle').textContent = data.chamado.titulo;
            document.getElementById('modalTicketDescription').textContent = data.chamado.descricao;
            
            // Status badge
            const statusBadge = document.getElementById('modalTicketStatus');
            statusBadge.textContent = data.chamado.status;
            statusBadge.className = `badge ${getStatusBadgeClass(data.chamado.status)}`;
            
            // Categoria badge
            const categoriaBadge = document.getElementById('modalTicketCategory');
            categoriaBadge.textContent = data.chamado.categoria;
            categoriaBadge.className = `badge ${getCategoriaBadgeClass(data.chamado.categoria)}`;
            
            // Dados do usuário
            if (data.usuario) {
                document.getElementById('modalUserName').textContent = data.usuario.nome;
                document.getElementById('modalUserEmail').textContent = data.usuario.email;
            }
            
            // Data de criação
            const dataFormatada = new Date(data.chamado.data_criacao).toLocaleDateString('pt-BR');
            document.getElementById('modalTicketDate').textContent = dataFormatada;
            
            // Mostrar modal
            const modal = new bootstrap.Modal(document.getElementById('viewTicketModal'));
            modal.show();
        })
        .catch(error => {
            console.error('Erro ao carregar detalhes do chamado:', error);
            alert('Erro ao carregar detalhes do chamado');
        });
}

function respondTicket(ticketId) {
    // Configurar o formulário de resposta
    const form = document.getElementById('responseForm');
    form.action = `/admin/chamados/${ticketId}/responder`;
    
    // Armazenar ID do ticket para uso na resposta
    window.currentTicketId = ticketId;
    const modal = new bootstrap.Modal(document.getElementById('respondTicketModal'));
    modal.show();
}

function closeTicket(ticketId) {
    if (confirm('Tem certeza que deseja marcar este chamado como resolvido?')) {
        // Enviar requisição para atualizar status
        const formData = new FormData();
        formData.append('status', 'resolvido');
        
        fetch(`/admin/chamados/${ticketId}/status`, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                alert('Erro ao atualizar status do chamado');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao atualizar status do chamado');
        });
    }
}

function reopenTicket(ticketId) {
    if (confirm('Tem certeza que deseja reabrir este chamado?')) {
        // Enviar requisição para atualizar status
        const formData = new FormData();
        formData.append('status', 'aberto');
        
        fetch(`/admin/chamados/${ticketId}/status`, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                alert('Erro ao reabrir chamado');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao reabrir chamado');
        });
    }
}

function exportTickets() {
    alert('Funcionalidade de exportação será implementada em breve...');
}

function respondTicketFromModal() {
    // Close view modal and open response modal
    bootstrap.Modal.getInstance(document.getElementById('viewTicketModal')).hide();
    setTimeout(() => {
        const ticketIdText = document.getElementById('modalTicketId').textContent;
        const ticketId = ticketIdText.replace('#', '');
        respondTicket(ticketId);
    }, 300);
}

function closeTicketFromModal() {
    if (confirm('Tem certeza que deseja marcar este chamado como resolvido?')) {
        bootstrap.Modal.getInstance(document.getElementById('viewTicketModal')).hide();
        
        // Buscar ID do ticket do modal
        const ticketIdText = document.getElementById('modalTicketId').textContent;
        const ticketId = ticketIdText.replace('#', '');
        closeTicket(ticketId);
    }
}

// Funções auxiliares para badges
function getStatusBadgeClass(status) {
    switch(status) {
        case 'aberto': return 'bg-primary';
        case 'em-andamento': return 'bg-warning';
        case 'resolvido': return 'bg-success';
        default: return 'bg-secondary';
    }
}

function getCategoriaBadgeClass(categoria) {
    switch(categoria) {
        case 'erro': return 'bg-danger';
        case 'duvida': return 'bg-info';
        case 'outros': return 'bg-secondary';
        default: return 'bg-light text-dark';
    }
}
