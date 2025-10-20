/* =========================
   DÚVIDAS ALUNO - JAVASCRIPT
   ========================= */

// Menu toggle functionality - Igual ao dashboard assistente
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    const menuToggle = document.getElementById('menuToggle');
    const closeSidebar = document.getElementById('closeSidebar');
    
    // Criar backdrop igual ao assistente
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

    // Close sidebar when pressing ESC key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && sidebar && sidebar.classList.contains('open')) {
            closeSidebarFunction();
        }
    });

    // Filter functionality para os selects
    const filterCategory = document.getElementById('filterCategory');
    const filterPopularity = document.getElementById('filterPopularity');
    const faqCards = document.querySelectorAll('.accordion-item');
    
    if (filterCategory) {
        filterCategory.addEventListener('change', function() {
            const category = this.value;
            
            faqCards.forEach(card => {
                if (category === 'todas') {
                    card.style.display = 'block';
                } else {
                    if (card.getAttribute('data-category') === category) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                }
            });
        });
    }

    // Search functionality
    const searchInput = document.getElementById('searchQuestion');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            
            faqCards.forEach(card => {
                const questionText = card.querySelector('.accordion-button').textContent.toLowerCase();
                const answerText = card.querySelector('.accordion-body').textContent.toLowerCase();
                
                if (questionText.includes(searchTerm) || answerText.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
});

// Funções para os filtros e controles da página
function clearFilters() {
    document.getElementById('filterCategory').value = 'todas';
    document.getElementById('filterPopularity').value = '';
    document.getElementById('searchQuestion').value = '';
    
    // Mostrar todas as FAQs
    const faqCards = document.querySelectorAll('.accordion-item');
    faqCards.forEach(card => {
        card.style.display = 'block';
    });
    
    alert('Filtros limpos!');
}

function filterQuestions() {
    // Esta função será chamada quando os filtros mudarem
    const category = document.getElementById('filterCategory').value;
    const popularity = document.getElementById('filterPopularity').value;
    
    // Implementar lógica de filtros aqui
    console.log('Filtrando por categoria:', category, 'popularidade:', popularity);
}

function searchQuestions() {
    const searchTerm = document.getElementById('searchQuestion').value;
    if (searchTerm.trim() === '') {
        alert('Digite um termo de busca');
        return;
    }
    // A busca já é feita em tempo real pelo event listener
    console.log('Buscando por:', searchTerm);
}

function expandAll() {
    const collapseElements = document.querySelectorAll('.accordion-collapse');
    collapseElements.forEach(element => {
        element.classList.add('show');
        const button = document.querySelector(`[data-bs-target="#${element.id}"]`);
        if (button) {
            button.classList.remove('collapsed');
            button.setAttribute('aria-expanded', 'true');
        }
    });
}

function collapseAll() {
    const collapseElements = document.querySelectorAll('.accordion-collapse.show');
    collapseElements.forEach(element => {
        element.classList.remove('show');
        const button = document.querySelector(`[data-bs-target="#${element.id}"]`);
        if (button) {
            button.classList.add('collapsed');
            button.setAttribute('aria-expanded', 'false');
        }
    });
}
