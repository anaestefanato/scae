/* =========================
   EDITAIS ALUNO - JAVASCRIPT
   ========================= */

// Menu toggle functionality - Igual ao dashboard e recebimentos
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    const menuToggle = document.getElementById('menuToggle');
    const closeSidebar = document.getElementById('closeSidebar');
    
    // Criar backdrop igual ao dashboard
    const sidebarBackdrop = document.createElement('div');
    sidebarBackdrop.className = 'sidebar-backdrop';
    document.body.appendChild(sidebarBackdrop);
    
    function closeSidebarFunction() {
        if (sidebar) {
            sidebar.classList.remove('open');
            sidebar.classList.add('collapsed');
        }
        if (mainContent) mainContent.classList.remove('shifted');
        if (menuToggle) menuToggle.classList.remove('hidden');
        if (sidebarBackdrop) sidebarBackdrop.classList.remove('visible');
        document.body.style.overflow = ''; // Permite scroll novamente
    }
    
    function openSidebarFunction() {
        if (sidebar) {
            sidebar.classList.add('open');
            sidebar.classList.remove('collapsed');
        }
        if (mainContent) mainContent.classList.add('shifted');
        if (menuToggle) menuToggle.classList.add('hidden');
        if (sidebarBackdrop) sidebarBackdrop.classList.add('visible');
        document.body.style.overflow = 'hidden'; // Impede scroll da página
    }
    
    // Close sidebar button
    if (closeSidebar) {
        closeSidebar.addEventListener('click', closeSidebarFunction);
    }
    
    // Open sidebar button
    if (menuToggle) {
        menuToggle.addEventListener('click', openSidebarFunction);
    }

    // Close sidebar when clicking on backdrop
    if (sidebarBackdrop) {
        sidebarBackdrop.addEventListener('click', closeSidebarFunction);
    }

    // Close sidebar on ESC key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar && sidebar.classList.contains('open')) {
            closeSidebarFunction();
        }
    });

    // Função para garantir que a sidebar esteja sempre fechada ao carregar
    function initializeSidebar() {
        if (sidebar) {
            sidebar.classList.remove('open');
            sidebar.classList.add('collapsed');
        }
        if (mainContent) mainContent.classList.remove('shifted');
        if (menuToggle) menuToggle.classList.remove('hidden');
        if (sidebarBackdrop) sidebarBackdrop.classList.remove('visible');
    }

    // Inicializar sidebar fechada
    initializeSidebar();

    // Funcionalidade das tabs de editais
    initializeEditalTabs();
});

// Função para inicializar as tabs de editais
function initializeEditalTabs() {
    const tabs = document.querySelectorAll('.edital-tab');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Remove active de todas as tabs
            tabs.forEach(t => t.classList.remove('active'));
            
            // Adiciona active na tab clicada
            this.classList.add('active');
            
            // Aqui você pode adicionar lógica para filtrar editais
            const tabText = this.textContent.trim();
            filterEditaisByTab(tabText);
        });
    });
}

// Função para filtrar editais por tab (pode ser expandida conforme necessário)
function filterEditaisByTab(tabName) {
    console.log('Filtrando editais por:', tabName);
    
    // Exemplo básico de filtro - pode ser expandido
    const editals = document.querySelectorAll('.edital-card');
    
    if (tabName === 'Todas as Páginas') {
        // Mostrar todos os editais
        editals.forEach(edital => {
            edital.style.display = 'block';
        });
    } else {
        // Lógica específica para cada ano ou categoria
        editals.forEach(edital => {
            const title = edital.querySelector('h3').textContent;
            
            if (tabName.includes('2025') && title.includes('2025')) {
                edital.style.display = 'block';
            } else if (tabName.includes('2024') && title.includes('2024')) {
                edital.style.display = 'block';
            } else if (tabName.includes('2023') && title.includes('2023')) {
                edital.style.display = 'block';
            } else if (tabName.includes('Assistência Estudantil') && title.includes('Assistência')) {
                edital.style.display = 'block';
            } else if (tabName !== 'Edital 2025') {
                edital.style.display = 'none';
            }
        });
    }
}

// Função para mostrar detalhes do edital no modal
function mostrarDetalhesEdital(titulo, descricao) {
    const modalTitle = document.querySelector('#modalDetalhes .modal-title');
    const modalBody = document.querySelector('#modalDetalhes .modal-body p');
    
    if (modalTitle) modalTitle.textContent = `Detalhes do ${titulo}`;
    if (modalBody) modalBody.textContent = descricao || 'Aqui estão as informações detalhadas do edital selecionado.';
}

// Função para download de anexos (simulada)
function downloadAnexo(nomeAnexo) {
    alert(`Download do ${nomeAnexo} será iniciado em instantes...`);
    // Aqui você implementaria a lógica real de download
}
