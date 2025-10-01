// =========================
// ENTREVISTAS - JAVASCRIPT
// =========================

document.addEventListener('DOMContentLoaded', function() {
    initializeSidebar();
    initializeFilters();
    initializeActions();
    initializeTooltips();
    updateDateTime();
});

// ===== SIDEBAR FUNCTIONALITY =====
function initializeSidebar() {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    const closeSidebar = document.getElementById('closeSidebar');
    const mainContent = document.getElementById('mainContent');

    // Create backdrop
    const backdrop = document.createElement('div');
    backdrop.className = 'sidebar-backdrop';
    document.body.appendChild(backdrop);

    // Toggle sidebar
    menuToggle.addEventListener('click', function() {
        sidebar.classList.add('open');
        backdrop.classList.add('visible');
        menuToggle.classList.add('hidden');
        mainContent.classList.add('shifted');
    });

    // Close sidebar
    function closeSidebarFunction() {
        sidebar.classList.remove('open');
        backdrop.classList.remove('visible');
        menuToggle.classList.remove('hidden');
        mainContent.classList.remove('shifted');
    }

    closeSidebar.addEventListener('click', closeSidebarFunction);
    backdrop.addEventListener('click', closeSidebarFunction);

    // Close sidebar on ESC key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar.classList.contains('open')) {
            closeSidebarFunction();
        }
    });
}

// ===== FILTERS FUNCTIONALITY =====
function initializeFilters() {
    const filtroData = document.getElementById('filtroData');
    const filtroTipo = document.getElementById('filtroTipo');
    const filtroPrioridade = document.getElementById('filtroPrioridade');
    const filtroAluno = document.getElementById('filtroAluno');

    // Set today's date as default
    const today = new Date().toISOString().split('T')[0];
    filtroData.value = today;

    // Add event listeners
    [filtroData, filtroTipo, filtroPrioridade, filtroAluno].forEach(filter => {
        filter.addEventListener('change', applyFilters);
        filter.addEventListener('input', debounce(applyFilters, 300));
    });
}

function applyFilters() {
    const filtroData = document.getElementById('filtroData').value;
    const filtroTipo = document.getElementById('filtroTipo').value.toLowerCase();
    const filtroPrioridade = document.getElementById('filtroPrioridade').value.toLowerCase();
    const filtroAluno = document.getElementById('filtroAluno').value.toLowerCase();

    const entrevistaCards = document.querySelectorAll('.entrevista-card');

    entrevistaCards.forEach(card => {
        const aluno = card.querySelector('.entrevista-aluno').textContent.toLowerCase();
        const tipo = card.querySelector('.entrevista-tipo').textContent.toLowerCase();
        const prioridade = card.querySelector('.priority-badge').textContent.toLowerCase();

        let showCard = true;

        // Filter by student name
        if (filtroAluno && !aluno.includes(filtroAluno)) {
            showCard = false;
        }

        // Filter by interview type
        if (filtroTipo && !tipo.includes(filtroTipo)) {
            showCard = false;
        }

        // Filter by priority
        if (filtroPrioridade && !prioridade.includes(filtroPrioridade)) {
            showCard = false;
        }

        // Apply filter animation
        if (showCard) {
            card.classList.remove('filtered-out');
            card.classList.add('filtered-in');
            card.style.display = '';
        } else {
            card.classList.remove('filtered-in');
            card.classList.add('filtered-out');
            setTimeout(() => {
                if (card.classList.contains('filtered-out')) {
                    card.style.display = 'none';
                }
            }, 300);
        }
    });

    updateFilterResults();
}

function updateFilterResults() {
    const visibleCards = document.querySelectorAll('.entrevista-card:not(.filtered-out)');
    const totalCards = document.querySelectorAll('.entrevista-card');
    
    // You can add a results counter here if needed
    console.log(`Showing ${visibleCards.length} of ${totalCards.length} interviews`);
}

// ===== ACTIONS FUNCTIONALITY =====
function initializeActions() {
    // Initialize all action buttons
    initializeStartButtons();
    initializeRescheduleButtons();
    initializeNotificationButtons();
    initializeDropdownActions();
}

function initializeStartButtons() {
    const startButtons = document.querySelectorAll('.btn-success');
    
    startButtons.forEach(button => {
        if (button.innerHTML.includes('Iniciar')) {
            button.addEventListener('click', function() {
                const entrevistaCard = this.closest('.entrevista-card');
                const alunoNome = entrevistaCard.querySelector('.entrevista-aluno').textContent;
                
                if (confirm(`Deseja iniciar a entrevista com ${alunoNome}?`)) {
                    startInterview(entrevistaCard);
                }
            });
        }
    });
}

function initializeRescheduleButtons() {
    const rescheduleButtons = document.querySelectorAll('.btn-outline-secondary');
    
    rescheduleButtons.forEach(button => {
        if (button.innerHTML.includes('Reagendar')) {
            button.addEventListener('click', function() {
                const entrevistaCard = this.closest('.entrevista-card');
                const alunoNome = entrevistaCard.querySelector('.entrevista-aluno').textContent;
                
                rescheduleInterview(entrevistaCard);
            });
        }
    });
}

function initializeNotificationButtons() {
    const notificationButtons = document.querySelectorAll('.btn-outline-secondary, .btn-outline-info');
    
    notificationButtons.forEach(button => {
        if (button.innerHTML.includes('Notificar') || button.innerHTML.includes('Enviar Link')) {
            button.addEventListener('click', function() {
                const entrevistaCard = this.closest('.entrevista-card');
                const alunoNome = entrevistaCard.querySelector('.entrevista-aluno').textContent;
                
                sendNotification(entrevistaCard);
            });
        }
    });
}

function initializeDropdownActions() {
    const dropdownItems = document.querySelectorAll('.dropdown-item');
    
    dropdownItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            const action = this.textContent.trim();
            const entrevistaCard = this.closest('.entrevista-card');
            const alunoNome = entrevistaCard.querySelector('.entrevista-aluno').textContent;
            
            switch(action) {
                case 'Visualizar':
                    viewInterview(entrevistaCard);
                    break;
                case 'Editar':
                    editInterview(entrevistaCard);
                    break;
                case 'Reagendar':
                    rescheduleInterview(entrevistaCard);
                    break;
                case 'Notificar Aluno':
                    sendNotification(entrevistaCard);
                    break;
                case 'Cancelar':
                    if (confirm(`Deseja realmente cancelar a entrevista com ${alunoNome}?`)) {
                        cancelInterview(entrevistaCard);
                    }
                    break;
            }
        });
    });
}

// ===== ACTION FUNCTIONS =====
function startInterview(card) {
    const button = card.querySelector('.btn-success');
    const originalText = button.innerHTML;
    
    // Show loading state
    button.classList.add('loading');
    button.disabled = true;
    
    // Simulate API call
    setTimeout(() => {
        button.classList.remove('loading');
        button.disabled = false;
        
        // Update status
        const statusBadge = card.querySelector('.status-badge');
        statusBadge.textContent = 'Em Andamento';
        statusBadge.className = 'status-badge status-em-andamento';
        
        // Update button
        button.innerHTML = '<i class="bi bi-stop-circle me-1"></i>Finalizar';
        
        showNotification('Entrevista iniciada com sucesso!', 'success');
    }, 1500);
}

function rescheduleInterview(card) {
    // This would typically open a modal or redirect to a form
    showNotification('Funcionalidade de reagendamento em desenvolvimento', 'info');
}

function sendNotification(card) {
    const button = card.querySelector('.btn-outline-secondary, .btn-outline-info');
    const originalText = button.innerHTML;
    
    button.classList.add('loading');
    button.disabled = true;
    
    setTimeout(() => {
        button.classList.remove('loading');
        button.disabled = false;
        
        showNotification('Notificação enviada com sucesso!', 'success');
    }, 1000);
}

function viewInterview(card) {
    const alunoNome = card.querySelector('.entrevista-aluno').textContent;
    showNotification(`Visualizando entrevista de ${alunoNome}`, 'info');
    // This would typically redirect to a details page
}

function editInterview(card) {
    const alunoNome = card.querySelector('.entrevista-aluno').textContent;
    showNotification(`Editando entrevista de ${alunoNome}`, 'info');
    // This would typically redirect to an edit form
}

function cancelInterview(card) {
    const statusBadge = card.querySelector('.status-badge');
    statusBadge.textContent = 'Cancelada';
    statusBadge.className = 'status-badge status-cancelada';
    
    // Disable action buttons
    const buttons = card.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.disabled = true;
        btn.classList.add('disabled');
    });
    
    // Add visual indication
    card.style.opacity = '0.6';
    
    showNotification('Entrevista cancelada', 'warning');
}

// ===== UTILITY FUNCTIONS =====
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

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show notification-toast`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        max-width: 350px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border-radius: 8px;
    `;
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 3000);
}

function initializeTooltips() {
    // Initialize Bootstrap tooltips if needed
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function updateDateTime() {
    // Update any dynamic date/time displays
    const now = new Date();
    const options = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    
    // You can use this to update dynamic dates in the interface
    console.log('Current date:', now.toLocaleDateString('pt-BR', options));
}

// ===== EXPORT FOR GLOBAL ACCESS =====
window.EntrevistasManager = {
    applyFilters,
    startInterview,
    rescheduleInterview,
    sendNotification,
    showNotification
};