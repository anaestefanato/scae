// Alunos - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar funcionalidades da página
    initializePageFunctions();
    loadAlunos();
    setupEventListeners();
});

// Configuração da paginação
const ITEMS_PER_PAGE = 20;
let currentPage = 1;
let currentFilter = 'todos';
let currentSearch = '';
let allAlunos = [];

// Função para inicializar as funcionalidades da página
function initializePageFunctions() {
    console.log('Página de alunos carregada');
    
    // Gerar dados simulados
    allAlunos = generateAlunosData();
    
    // Configurar filtros
    setupFilters();
    
    // Configurar busca
    setupSearch();
    
    // Animar elementos
    animateElements();
}

// Função para gerar dados simulados de centenas de alunos
function generateAlunosData() {
    const nomes = [
        'Ana Silva Santos', 'João Pedro Oliveira', 'Maria Carolina Costa', 'Carlos Eduardo Lima',
        'Fernanda Alves Souza', 'Rafael Santos Pereira', 'Juliana Moreira Lima', 'Bruno Costa Silva',
        'Camila Rodrigues Alves', 'Lucas Gabriel Santos', 'Amanda Ferreira Costa', 'Diego Henrique Lima',
        'Gabriela Santos Oliveira', 'Matheus Almeida Silva', 'Larissa Pereira Costa', 'Felipe Rodrigues Santos',
        'Isabela Costa Ferreira', 'Victor Hugo Alves', 'Natália Silva Pereira', 'Eduardo Santos Lima',
        'Priscila Oliveira Costa', 'Thiago Alves Santos', 'Mariana Lima Silva', 'Rodrigo Costa Pereira',
        'Carolina Santos Alves', 'André Lima Costa', 'Beatriz Silva Santos', 'Gustavo Pereira Lima',
        'Letícia Costa Silva', 'Daniel Santos Alves', 'Vanessa Lima Pereira', 'Marcelo Silva Costa',
        'Adriana Santos Lima', 'Paulo Costa Alves', 'Renata Silva Pereira', 'Leonardo Lima Santos',
        'Patrícia Costa Silva', 'Ricardo Santos Lima', 'Sandra Pereira Costa', 'Antônio Silva Santos'
    ];
    
    const cursos = [
        'Técnico em Informática', 'Técnico em Eletromecânica'
    ];
    
    const auxiliosTipos = ['Transporte', 'Moradia', 'Alimentação', 'Material Didático'];
    const situacoes = ['Ativo', 'Suspenso'];
    const periodos = ['1º Período', '2º Período', '3º Período', '4º Período'];
    
    const alunos = [];
    
    // Gerar 300 alunos
    for (let i = 1; i <= 300; i++) {
        const nome = nomes[Math.floor(Math.random() * nomes.length)];
        const curso = cursos[Math.floor(Math.random() * cursos.length)];
        const periodo = periodos[Math.floor(Math.random() * periodos.length)];
        const situacao = situacoes[Math.floor(Math.random() * situacoes.length)];
        
        // Gerar auxilios aleatórios (1 a 4 auxílios)
        const numAuxilios = Math.floor(Math.random() * 4) + 1;
        const auxiliosAluno = [];
        const auxiliosSelecionados = [...auxiliosTipos].sort(() => 0.5 - Math.random()).slice(0, numAuxilios);
        
        let valorTotal = 0;
        auxiliosSelecionados.forEach(auxilio => {
            let valor = 0;
            switch(auxilio) {
                case 'Transporte':
                    valor = 180;
                    break;
                case 'Alimentação':
                    valor = 100;
                    break;
                case 'Moradia':
                    valor = 300;
                    break;
                case 'Material Didático':
                    valor = 150;
                    break;
            }
            auxiliosAluno.push({ nome: auxilio, valor: valor });
            valorTotal += valor;
        });
        
        const aluno = {
            id: i,
            nome: nome,
            matricula: `2023${String(i).padStart(6, '0')}`,
            curso: curso,
            periodo: periodo,
            auxilios: auxiliosAluno,
            valorTotal: valorTotal,
            situacao: situacao,
            email: `${nome.toLowerCase().replace(/\s+/g, '.')}@aluno.ifes.edu.br`
        };
        
        alunos.push(aluno);
    }
    
    return alunos;
}

// Função para carregar e exibir alunos
function loadAlunos() {
    showLoadingState();
    
    // Simular carregamento
    setTimeout(() => {
        const alunosFiltrados = filterAlunos(allAlunos);
        const alunosPaginados = paginateAlunos(alunosFiltrados);
        
        renderAlunos(alunosPaginados);
        updatePagination(alunosFiltrados.length);
        updateResultsCount(alunosFiltrados.length);
        
        hideLoadingState();
        
        if (alunosFiltrados.length === 0) {
            showNoResults();
        } else {
            hideNoResults();
        }
    }, 500);
}

// Função para filtrar alunos
function filterAlunos(alunos) {
    let filtered = [...alunos];
    
    // Filtrar por situação/tipo
    if (currentFilter !== 'todos') {
        filtered = filtered.filter(aluno => {
            switch(currentFilter) {
                case 'ativos':
                    return aluno.situacao === 'Ativo';
                case 'suspensos':
                    return aluno.situacao === 'Suspenso';
                case 'transporte':
                    return aluno.auxilios.some(aux => aux.nome === 'Transporte');
                case 'alimentacao':
                    return aluno.auxilios.some(aux => aux.nome === 'Alimentação');
                case 'moradia':
                    return aluno.auxilios.some(aux => aux.nome === 'Moradia');
                case 'material':
                    return aluno.auxilios.some(aux => aux.nome === 'Material Didático');
                default:
                    return true;
            }
        });
    }
    
    // Filtrar por busca
    if (currentSearch.trim() !== '') {
        const searchTerm = currentSearch.toLowerCase();
        filtered = filtered.filter(aluno => 
            aluno.nome.toLowerCase().includes(searchTerm) ||
            aluno.matricula.includes(searchTerm) ||
            aluno.curso.toLowerCase().includes(searchTerm)
        );
    }
    
    return filtered;
}

// Função para paginar alunos
function paginateAlunos(alunos) {
    const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
    const endIndex = startIndex + ITEMS_PER_PAGE;
    return alunos.slice(startIndex, endIndex);
}

// Função para renderizar alunos na tabela
function renderAlunos(alunos) {
    const tbody = document.getElementById('alunosTableBody');
    tbody.innerHTML = '';
    
    alunos.forEach((aluno, index) => {
        const row = createAlunoRow(aluno);
        tbody.appendChild(row);
        
        // Animação de entrada
        setTimeout(() => {
            row.style.opacity = '1';
            row.style.transform = 'translateY(0)';
        }, index * 50);
    });
}

// Função para criar linha do aluno
function createAlunoRow(aluno) {
    const row = document.createElement('tr');
    row.style.opacity = '0';
    row.style.transform = 'translateY(20px)';
    row.style.transition = 'all 0.3s ease-out';
    row.onclick = () => verDetalhesAluno(aluno.id);
    
    const auxiliosBadges = aluno.auxilios.map(auxilio => {
        const badgeClass = getBadgeClass(auxilio.nome);
        return `<span class="auxilio-badge ${badgeClass}">${auxilio.nome}</span>`;
    }).join('');
    
    const situacaoClass = aluno.situacao === 'Ativo' ? 'ativo' : 'suspenso';
    
    row.innerHTML = `
        <td data-label="Nome">
            <span class="aluno-nome" onclick="event.stopPropagation(); verDetalhesAluno(${aluno.id})">${aluno.nome}</span>
        </td>
        <td data-label="Matrícula">
            <span class="aluno-matricula">${aluno.matricula}</span>
        </td>
        <td data-label="Curso">${aluno.curso}</td>
        <td data-label="Período">${aluno.periodo}</td>
        <td data-label="Auxílios">
            <div class="auxilios-badges">
                ${auxiliosBadges}
            </div>
        </td>
        <td data-label="Valor Mensal">
            <span class="valor-mensal">R$ ${aluno.valorTotal.toFixed(2).replace('.', ',')}</span>
        </td>
        <td data-label="Situação">
            <span class="status-badge ${situacaoClass}">${aluno.situacao}</span>
        </td>
        <td data-label="Ações">
            <button class="btn btn-acao btn-detalhes" onclick="event.stopPropagation(); verDetalhesAluno(${aluno.id})">
                <i class="bi bi-eye"></i>
            </button>
        </td>
    `;
    
    return row;
}

// Função para obter classe do badge baseada no tipo de auxílio
function getBadgeClass(auxilio) {
    const classes = {
        'Transporte': 'transporte',
        'Alimentação': 'alimentacao',
        'Moradia': 'moradia',
        'Material Didático': 'material'
    };
    return classes[auxilio] || 'secondary';
}

// Função para configurar event listeners
function setupEventListeners() {
    // Busca
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            currentSearch = this.value;
            currentPage = 1; // Reset para primeira página
            loadAlunos();
        });
    }
    
    // Filtro
    const filterSelect = document.getElementById('filterSelect');
    if (filterSelect) {
        filterSelect.addEventListener('change', function() {
            currentFilter = this.value;
            currentPage = 1; // Reset para primeira página
            loadAlunos();
        });
    }
}

// Função para configurar filtros
function setupFilters() {
    // Configurações iniciais já feitas no HTML
}

// Função para configurar busca
function setupSearch() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        // Focus automático na busca com Ctrl+F
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'f') {
                e.preventDefault();
                searchInput.focus();
            }
        });
    }
}

// Função para limpar filtros
function clearFilters() {
    // Limpar busca
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.value = '';
        currentSearch = '';
    }
    
    // Resetar filtro
    const filterSelect = document.getElementById('filterSelect');
    if (filterSelect) {
        filterSelect.value = 'todos';
        currentFilter = 'todos';
    }
    
    // Reset página
    currentPage = 1;
    
    // Recarregar alunos
    loadAlunos();
    
    showNotification('Filtros limpos!', 'info');
}

// Função para atualizar estatísticas
function updateStats(alunos) {
    const totalAlunos = alunos.length;
    const alunosAtivos = alunos.filter(a => a.situacao === 'Ativo').length;
    const valorTotalAuxilios = alunos.reduce((sum, a) => sum + a.valorTotal, 0);
    
    // Atualizar elementos da página
    animateCounter(document.getElementById('totalAlunos'), totalAlunos);
    animateCounter(document.getElementById('alunosAtivos'), alunosAtivos);
    
    const valorElement = document.getElementById('valorTotal');
    if (valorElement) {
        valorElement.textContent = `R$ ${valorTotalAuxilios.toFixed(2).replace('.', ',').replace(/\B(?=(\d{3})+(?!\d))/g, '.')}`;
    }
}

// Função para animar contador
function animateCounter(element, targetValue) {
    if (!element || typeof targetValue !== 'number') return;
    
    const startValue = 0;
    const duration = 1000;
    const startTime = performance.now();
    
    function updateCounter(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const currentValue = Math.floor(startValue + (targetValue - startValue) * progress);
        element.textContent = currentValue;
        
        if (progress < 1) {
            requestAnimationFrame(updateCounter);
        }
    }
    
    requestAnimationFrame(updateCounter);
}

// Função para atualizar paginação
function updatePagination(totalItems) {
    const totalPages = Math.ceil(totalItems / ITEMS_PER_PAGE);
    const paginationContainer = document.getElementById('pagination');
    
    if (!paginationContainer) return;
    
    paginationContainer.innerHTML = '';
    
    if (totalPages <= 1) return;
    
    // Botão anterior
    const prevButton = createPaginationButton('Anterior', currentPage > 1, () => {
        if (currentPage > 1) {
            currentPage--;
            loadAlunos();
        }
    });
    paginationContainer.appendChild(prevButton);
    
    // Números das páginas
    const startPage = Math.max(1, currentPage - 2);
    const endPage = Math.min(totalPages, currentPage + 2);
    
    for (let i = startPage; i <= endPage; i++) {
        const pageButton = createPaginationButton(i, true, () => {
            currentPage = i;
            loadAlunos();
        }, i === currentPage);
        paginationContainer.appendChild(pageButton);
    }
    
    // Botão próximo
    const nextButton = createPaginationButton('Próximo', currentPage < totalPages, () => {
        if (currentPage < totalPages) {
            currentPage++;
            loadAlunos();
        }
    });
    paginationContainer.appendChild(nextButton);
}

// Função para criar botão de paginação
function createPaginationButton(text, enabled, onClick, isActive = false) {
    const li = document.createElement('li');
    li.className = `page-item ${!enabled ? 'disabled' : ''} ${isActive ? 'active' : ''}`;
    
    const a = document.createElement('a');
    a.className = 'page-link';
    a.href = '#';
    a.textContent = text;
    
    if (enabled) {
        a.addEventListener('click', (e) => {
            e.preventDefault();
            onClick();
        });
    }
    
    li.appendChild(a);
    return li;
}

// Função para atualizar contador de resultados
function updateResultsCount(totalItems) {
    const resultsCount = document.getElementById('resultsCount');
    if (!resultsCount) return;
    
    const startItem = (currentPage - 1) * ITEMS_PER_PAGE + 1;
    const endItem = Math.min(currentPage * ITEMS_PER_PAGE, totalItems);
    
    if (totalItems === 0) {
        resultsCount.textContent = 'Nenhum aluno encontrado';
    } else {
        resultsCount.textContent = `Mostrando ${startItem}-${endItem} de ${totalItems} alunos`;
    }
}

// Função para mostrar/esconder estados
function showLoadingState() {
    const loadingState = document.getElementById('loadingState');
    const tableBody = document.getElementById('alunosTableBody');
    
    if (loadingState) loadingState.style.display = 'block';
    if (tableBody) tableBody.style.display = 'none';
}

function hideLoadingState() {
    const loadingState = document.getElementById('loadingState');
    const tableBody = document.getElementById('alunosTableBody');
    
    if (loadingState) loadingState.style.display = 'none';
    if (tableBody) tableBody.style.display = 'table-row-group';
}

function showNoResults() {
    const noResults = document.getElementById('noResultsState');
    const tableBody = document.getElementById('alunosTableBody');
    
    if (noResults) noResults.style.display = 'block';
    if (tableBody) tableBody.style.display = 'none';
}

function hideNoResults() {
    const noResults = document.getElementById('noResultsState');
    if (noResults) noResults.style.display = 'none';
}

// Função para ver detalhes do aluno
function verDetalhesAluno(alunoId) {
    // Redirecionar para página de detalhes
    window.location.href = `/assistente/detalhes_alunos.html?id=${alunoId}`;
}

// Função para animar elementos na entrada
function animateElements() {
    const statsCards = document.querySelectorAll('.stats-card');
    
    statsCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease-out';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Função para exportar dados
function exportarDados() {
    const alunosFiltrados = filterAlunos(allAlunos);
    
    if (alunosFiltrados.length === 0) {
        showNotification('Nenhum dado para exportar!', 'warning');
        return;
    }
    
    // Simular exportação
    showNotification('Preparando exportação...', 'info');
    
    setTimeout(() => {
        showNotification(`${alunosFiltrados.length} registros exportados com sucesso!`, 'success');
    }, 2000);
}

// Função para mostrar notificações
function showNotification(message, type = 'info') {
    // Criar elemento de notificação
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} notification-toast`;
    notification.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="bi bi-info-circle-fill me-2"></i>
            <span>${message}</span>
        </div>
    `;
    
    // Adicionar estilos
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        animation: slideInRight 0.3s ease-out;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border-radius: 10px;
        border: none;
    `;
    
    document.body.appendChild(notification);
    
    // Remover após 3 segundos
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Adicionar estilos de animação
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Exportar funções para uso global
window.verDetalhesAluno = verDetalhesAluno;
window.clearFilters = clearFilters;
window.exportarDados = exportarDados;