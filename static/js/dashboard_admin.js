/* ==========================================
   DASHBOARD ADMINISTRADOR - JAVASCRIPT
   ========================================== */

document.addEventListener('DOMContentLoaded', function() {
    // ===== ELEMENTOS DOM =====
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    const menuToggle = document.getElementById('menuToggle');
    const closeSidebar = document.getElementById('closeSidebar');
    const body = document.body;

    // ===== CRIAR BACKDROP =====
    const backdrop = document.createElement('div');
    backdrop.className = 'sidebar-backdrop';
    body.appendChild(backdrop);

    // ===== FUNÇÕES DE CONTROLE DA SIDEBAR =====
    function openSidebar() {
        sidebar.classList.add('open');
        mainContent.classList.add('shifted');
        backdrop.classList.add('visible');
        menuToggle.classList.add('hidden');
    }

    function closeSidebarFunc() {
        sidebar.classList.remove('open');
        mainContent.classList.remove('shifted');
        backdrop.classList.remove('visible');
        menuToggle.classList.remove('hidden');
    }

    // ===== EVENT LISTENERS =====
    menuToggle.addEventListener('click', openSidebar);
    closeSidebar.addEventListener('click', closeSidebarFunc);
    backdrop.addEventListener('click', closeSidebarFunc);

    // ===== FECHAR SIDEBAR COM ESC =====
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && sidebar.classList.contains('open')) {
            closeSidebarFunc();
        }
    });

    // ===== ANIMAÇÃO DOS STATS CARDS =====
    function animateStatsCards() {
        const statsCards = document.querySelectorAll('.stats-card');
        
        statsCards.forEach((card, index) => {
            setTimeout(() => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                
                setTimeout(() => {
                    card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, 100);
            }, index * 150);
        });
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
                         type === 'error' ? 'bi-exclamation-triangle' : 'bi-info-circle';
        const bgClass = type === 'success' ? 'bg-success' : 
                       type === 'error' ? 'bg-danger' : 'bg-primary';

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

    // ===== CONTROLE DO SUBMENU =====
    function initSubmenu() {
        const submenuToggles = document.querySelectorAll('.submenu-toggle');
        
        submenuToggles.forEach(toggle => {
            // Adicionar evento apenas na seta, não no link todo
            const arrow = toggle.querySelector('.submenu-arrow');
            
            if (arrow) {
                arrow.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation(); // Impede que o link seja ativado
                    
                    const submenuId = toggle.getAttribute('data-submenu');
                    const submenu = document.getElementById(`submenu-${submenuId}`);
                    
                    // Toggle classes
                    toggle.classList.toggle('expanded');
                    submenu.classList.toggle('expanded');
                    
                    // Fechar outros submenus
                    submenuToggles.forEach(otherToggle => {
                        if (otherToggle !== toggle) {
                            const otherSubmenuId = otherToggle.getAttribute('data-submenu');
                            const otherSubmenu = document.getElementById(`submenu-${otherSubmenuId}`);
                            otherToggle.classList.remove('expanded');
                            if (otherSubmenu) {
                                otherSubmenu.classList.remove('expanded');
                            }
                        }
                    });
                });
            }
        });
    }

    // ===== INICIALIZAÇÃO =====
    function init() {
        // Inicializar submenu
        initSubmenu();
        
        // Animar stats cards
        animateStatsCards();

        // Adicionar efeito hover nos cards da tabela
        const tableRows = document.querySelectorAll('.table tbody tr');
        tableRows.forEach(row => {
            row.addEventListener('mouseenter', function() {
                this.style.backgroundColor = 'var(--ifes-hover-bg)';
            });
            
            row.addEventListener('mouseleave', function() {
                this.style.backgroundColor = '';
            });
        });

        // Adicionar efeito de click nos stats cards
        const statsCards = document.querySelectorAll('.stats-card');
        statsCards.forEach(card => {
            card.addEventListener('click', function() {
                // Adicionar efeito de ripple
                const ripple = document.createElement('span');
                ripple.className = 'ripple-effect';
                ripple.style.position = 'absolute';
                ripple.style.borderRadius = '50%';
                ripple.style.background = 'rgba(46, 125, 50, 0.3)';
                ripple.style.transform = 'scale(0)';
                ripple.style.animation = 'ripple 0.6s linear';
                ripple.style.left = '50%';
                ripple.style.top = '50%';
                ripple.style.width = '20px';
                ripple.style.height = '20px';
                ripple.style.marginLeft = '-10px';
                ripple.style.marginTop = '-10px';
                
                this.style.position = 'relative';
                this.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });

        // Adicionar animação de entrada para os cards
        const cards = document.querySelectorAll('.card, .stats-card');
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const cardObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        cards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            cardObserver.observe(card);
        });
    }

    // ===== CSS PARA ANIMAÇÃO DE RIPPLE =====
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);

    // Inicializar tudo quando o DOM estiver carregado
    init();
});

// ===== INICIALIZAR FUNCIONALIDADES ESPECÍFICAS DO DASHBOARD ADMIN =====
document.addEventListener('DOMContentLoaded', function() {
    // Event listeners para os botões do modal de detalhes do aluno
    const confirmarBtn = document.getElementById('confirmarCadastro');
    const recusarBtn = document.getElementById('recusarCadastro');
    const motivoSection = document.getElementById('motivoRecusaSection');

    if (confirmarBtn) {
        // Botão confirmar cadastro
        confirmarBtn.addEventListener('click', function() {
            if (confirm('Deseja confirmar o cadastro deste aluno?')) {
                alert('Cadastro confirmado com sucesso! O aluno receberá um e-mail de confirmação.');
                bootstrap.Modal.getInstance(document.getElementById('detalhesAlunoModal')).hide();
                // Aqui você faria a requisição para o backend
            }
        });
    }

    if (recusarBtn && motivoSection) {
        // Botão recusar - mostrar campo de motivo
        recusarBtn.addEventListener('click', function() {
            if (motivoSection.classList.contains('d-none')) {
                motivoSection.classList.remove('d-none');
                recusarBtn.innerHTML = '<i class="bi bi-send me-2"></i>Enviar Recusa';
                recusarBtn.classList.remove('btn-danger');
                recusarBtn.classList.add('btn-warning');
            } else {
                const motivo = document.getElementById('motivoRecusa').value.trim();
                if (motivo === '') {
                    alert('Por favor, digite o motivo da recusa.');
                    return;
                }
                
                if (confirm('Deseja recusar o cadastro deste aluno? O motivo será enviado por e-mail.')) {
                    alert('Cadastro recusado. O aluno receberá um e-mail com o motivo da recusa.');
                    bootstrap.Modal.getInstance(document.getElementById('detalhesAlunoModal')).hide();
                    // Aqui você faria a requisição para o backend
                }
            }
        });

        // Reset do botão recusar quando modal fechar
        const detalhesAlunoModal = document.getElementById('detalhesAlunoModal');
        if (detalhesAlunoModal) {
            detalhesAlunoModal.addEventListener('hidden.bs.modal', function() {
                recusarBtn.innerHTML = '<i class="bi bi-x-lg me-2"></i>Recusar';
                recusarBtn.classList.remove('btn-warning');
                recusarBtn.classList.add('btn-danger');
            });
        }
    }

    // Funcionalidade para marcar notificações como lidas
    const marcarTodasLidasBtn = document.getElementById('marcarTodasLidas');
    const notificationBadge = document.querySelector('.notification-badge');
    
    if (marcarTodasLidasBtn) {
        marcarTodasLidasBtn.addEventListener('click', function() {
            // Marcar todas as notificações como lidas
            const unreadNotifications = document.querySelectorAll('.notification-item.unread');
            
            unreadNotifications.forEach(function(notification) {
                // Remover classe unread e adicionar read
                notification.classList.remove('unread');
                notification.classList.add('read');
                
                // Remover indicador visual de não lida
                const indicator = notification.querySelector('.unread-indicator');
                if (indicator) {
                    indicator.remove();
                }
                
                // Adicionar opacidade para indicar que foi lida
                notification.style.opacity = '0.7';
            });
            
            // Esconder badge de notificação
            if (notificationBadge) {
                notificationBadge.style.display = 'none';
            }
            
            // Atualizar badge da sidebar
            const sidebarBadge = document.getElementById('mensagensBadge');
            if (sidebarBadge) {
                sidebarBadge.style.display = 'none';
            }
            
            // Mostrar mensagem de confirmação
            marcarTodasLidasBtn.innerHTML = '<i class="bi bi-check-lg me-2"></i>Marcadas como lidas';
            marcarTodasLidasBtn.classList.remove('btn-outline-primary');
            marcarTodasLidasBtn.classList.add('btn-success');
            marcarTodasLidasBtn.disabled = true;
            
            // Fechar modal após 1 segundo
            setTimeout(function() {
                bootstrap.Modal.getInstance(document.getElementById('notificacoesModal')).hide();
            }, 1000);
        });
    }
    
    // Reset do botão quando modal de notificações abrir novamente
    const notificacoesModal = document.getElementById('notificacoesModal');
    if (notificacoesModal && marcarTodasLidasBtn) {
        notificacoesModal.addEventListener('show.bs.modal', function() {
            const unreadCount = document.querySelectorAll('.notification-item.unread').length;
            if (unreadCount === 0) {
                marcarTodasLidasBtn.innerHTML = 'Todas as notificações foram lidas';
                marcarTodasLidasBtn.classList.remove('btn-outline-primary');
                marcarTodasLidasBtn.classList.add('btn-secondary');
                marcarTodasLidasBtn.disabled = true;
            } else {
                marcarTodasLidasBtn.innerHTML = 'Marcar todas como lidas';
                marcarTodasLidasBtn.classList.remove('btn-success', 'btn-secondary');
                marcarTodasLidasBtn.classList.add('btn-outline-primary');
                marcarTodasLidasBtn.disabled = false;
            }
        });
    }
});
