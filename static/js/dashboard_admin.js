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

    // ===== CRIAR MODAL PARA NOVO EDITAL =====
    function createNovoEditalModal() {
        const modalHTML = `
        <div class="modal fade" id="novoEditalModal" tabindex="-1" aria-labelledby="novoEditalModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="novoEditalModalLabel">
                            <i class="bi bi-file-earmark-plus me-2"></i>Criar Novo Edital
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form id="novoEditalForm">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="numeroEdital" class="form-label">
                                            <i class="bi bi-hash me-1"></i>Número do Edital
                                        </label>
                                        <input type="text" class="form-control" id="numeroEdital" placeholder="Ex: 001/2025" required>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="tipoAuxilio" class="form-label">
                                            <i class="bi bi-tags me-1"></i>Tipo de Auxílio
                                        </label>
                                        <select class="form-select" id="tipoAuxilio" required>
                                            <option value="">Selecione o tipo...</option>
                                            <option value="alimentacao">Auxílio Alimentação</option>
                                            <option value="transporte">Auxílio Transporte</option>
                                            <option value="material">Auxílio Material Didático</option>
                                            <option value="moradia">Auxílio Moradia</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-4">
                                    <div class="mb-3">
                                        <label for="dataInicioInscricoes" class="form-label">
                                            <i class="bi bi-calendar-check me-1"></i>Início das Inscrições
                                        </label>
                                        <input type="date" class="form-control" id="dataInicioInscricoes" required>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="mb-3">
                                        <label for="dataFimInscricoes" class="form-label">
                                            <i class="bi bi-calendar-x me-1"></i>Fim das Inscrições
                                        </label>
                                        <input type="date" class="form-control" id="dataFimInscricoes" required>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="mb-3">
                                        <label for="valorAuxilio" class="form-label">
                                            <i class="bi bi-currency-dollar me-1"></i>Valor do Auxílio (R$)
                                        </label>
                                        <input type="number" class="form-control" id="valorAuxilio" placeholder="0,00" step="0.01" required>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="quantidadeBolsas" class="form-label">
                                            <i class="bi bi-people me-1"></i>Quantidade de Bolsas
                                        </label>
                                        <input type="number" class="form-control" id="quantidadeBolsas" placeholder="Ex: 100" required>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="statusEdital" class="form-label">
                                            <i class="bi bi-toggle-on me-1"></i>Status do Edital
                                        </label>
                                        <select class="form-select" id="statusEdital" required>
                                            <option value="rascunho">Rascunho</option>
                                            <option value="ativo" selected>Ativo</option>
                                            <option value="suspenso">Suspenso</option>
                                            <option value="encerrado">Encerrado</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <label for="descricaoEdital" class="form-label">
                                    <i class="bi bi-file-text me-1"></i>Descrição do Edital
                                </label>
                                <textarea class="form-control" id="descricaoEdital" rows="4" placeholder="Descreva os objetivos e critérios do edital..."></textarea>
                            </div>
                            
                            <div class="mb-3">
                                <label for="documentosNecessarios" class="form-label">
                                    <i class="bi bi-file-earmark-check me-1"></i>Documentos Necessários
                                </label>
                                <textarea class="form-control" id="documentosNecessarios" rows="3" placeholder="Liste os documentos necessários para inscrição..."></textarea>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-check mb-3">
                                        <input class="form-check-input" type="checkbox" id="requisitoRendaFamiliar">
                                        <label class="form-check-label" for="requisitoRendaFamiliar">
                                            <i class="bi bi-cash-stack me-1"></i>Exigir comprovante de renda familiar
                                        </label>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="form-check mb-3">
                                        <input class="form-check-input" type="checkbox" id="requisitoMatricula">
                                        <label class="form-check-label" for="requisitoMatricula">
                                            <i class="bi bi-card-text me-1"></i>Exigir comprovante de matrícula
                                        </label>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="form-check mb-3">
                                <input class="form-check-input" type="checkbox" id="notificarAlunos">
                                <label class="form-check-label" for="notificarAlunos">
                                    <i class="bi bi-bell me-1"></i>Notificar todos os alunos sobre o novo edital
                                </label>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            <i class="bi bi-x-circle me-1"></i>Cancelar
                        </button>
                        <button type="button" class="btn btn-success" id="salvarEdital">
                            <i class="bi bi-check-circle me-1"></i>Criar Edital
                        </button>
                    </div>
                </div>
            </div>
        </div>`;

        // Adicionar modal ao body se não existir
        if (!document.getElementById('novoEditalModal')) {
            document.body.insertAdjacentHTML('beforeend', modalHTML);
        }
    }

    // ===== FUNÇÃO PARA PROCESSAR PAGAMENTOS =====
    function processarPagamentos() {
        const btn = document.getElementById('processarPagamentosBtn');
        const originalText = btn.innerHTML;
        
        // Mostrar loading
        btn.innerHTML = '<i class="bi bi-hourglass-split me-1"></i>Processando...';
        btn.disabled = true;
        
        // Simular processamento (substituir por requisição real)
        setTimeout(() => {
            // Mostrar sucesso
            btn.innerHTML = '<i class="bi bi-check-circle me-1"></i>Processado!';
            btn.classList.remove('btn-warning');
            btn.classList.add('btn-success');
            
            // Atualizar status dos pagamentos
            document.querySelectorAll('.pagamento-item .badge').forEach(badge => {
                badge.textContent = 'Processado';
                badge.classList.remove('bg-warning', 'text-dark');
                badge.classList.add('bg-success');
            });
            
            // Voltar ao estado original após 3 segundos
            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.disabled = false;
                btn.classList.remove('btn-success');
                btn.classList.add('btn-warning');
            }, 3000);
        }, 2000);
    }

    // ===== FUNÇÃO PARA SALVAR EDITAL =====
    function salvarEdital() {
        const btn = document.getElementById('salvarEdital');
        const form = document.getElementById('novoEditalForm');
        const originalText = btn.innerHTML;
        
        // Validar formulário
        if (!form.checkValidity()) {
            form.classList.add('was-validated');
            return;
        }
        
        // Mostrar loading
        btn.innerHTML = '<i class="bi bi-hourglass-split me-1"></i>Criando Edital...';
        btn.disabled = true;
        
        // Coletar dados do formulário
        const dadosEdital = {
            numero: document.getElementById('numeroEdital').value,
            tipoAuxilio: document.getElementById('tipoAuxilio').value,
            dataInicioInscricoes: document.getElementById('dataInicioInscricoes').value,
            dataFimInscricoes: document.getElementById('dataFimInscricoes').value,
            valorAuxilio: document.getElementById('valorAuxilio').value,
            quantidadeBolsas: document.getElementById('quantidadeBolsas').value,
            statusEdital: document.getElementById('statusEdital').value,
            descricaoEdital: document.getElementById('descricaoEdital').value,
            documentosNecessarios: document.getElementById('documentosNecessarios').value,
            requisitoRendaFamiliar: document.getElementById('requisitoRendaFamiliar').checked,
            requisitoMatricula: document.getElementById('requisitoMatricula').checked,
            notificarAlunos: document.getElementById('notificarAlunos').checked
        };
        
        // Simular salvamento (substituir por requisição real)
        setTimeout(() => {
            // Mostrar sucesso
            btn.innerHTML = '<i class="bi bi-check-circle me-1"></i>Edital Criado!';
            btn.classList.remove('btn-success');
            btn.classList.add('btn-primary');
            
            // Fechar modal após 2 segundos
            setTimeout(() => {
                const modal = bootstrap.Modal.getInstance(document.getElementById('novoEditalModal'));
                modal.hide();
                
                // Reset do formulário e botão
                form.reset();
                form.classList.remove('was-validated');
                btn.innerHTML = originalText;
                btn.disabled = false;
                btn.classList.remove('btn-primary');
                btn.classList.add('btn-success');
                
                // Mostrar toast de sucesso
                showToast('Sucesso!', 'Edital criado com sucesso!', 'success');
            }, 2000);
        }, 1500);
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
        
        // Criar modal se não existir
        createNovoEditalModal();
        
        // Animar stats cards
        animateStatsCards();
        
        // Event listeners para botões
        const criarEditalBtn = document.querySelector('.btn-criar-edital');
        if (criarEditalBtn) {
            criarEditalBtn.addEventListener('click', function() {
                const modal = new bootstrap.Modal(document.getElementById('novoEditalModal'));
                modal.show();
            });
        }
        
        const processarPagamentosBtn = document.getElementById('processarPagamentosBtn');
        if (processarPagamentosBtn) {
            processarPagamentosBtn.addEventListener('click', processarPagamentos);
        }
        
        // Event listener para salvar edital
        document.addEventListener('click', function(e) {
            if (e.target && e.target.id === 'salvarEdital') {
                salvarEdital();
            }
        });

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

// ===== FUNÇÃO GLOBAL PARA ATUALIZAR DADOS DO DASHBOARD =====
function atualizarDashboard() {
    // Esta função pode ser chamada para atualizar os dados do dashboard
    // via AJAX sem recarregar a página
    console.log('Atualizando dados do dashboard...');
    
    // Implementar lógica de atualização via API
    // fetch('/api/dashboard-data')
    //     .then(response => response.json())
    //     .then(data => {
    //         // Atualizar elementos do DOM com os novos dados
    //     });
}

// ===== FUNÇÃO GLOBAL PARA EXPORTAR RELATÓRIO =====
function exportarRelatorio(tipo) {
    console.log('Exportando relatório:', tipo);
    
    // Implementar lógica de exportação
    // window.open(`/admin/relatorio/${tipo}/export`, '_blank');
}
