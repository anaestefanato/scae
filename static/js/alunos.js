// Alunos - JavaScript

// Carregar dados dos alunos do elemento script (injetado pelo template Jinja2)
const alunosDataElement = document.getElementById('alunos-data');
const alunosData = alunosDataElement ? JSON.parse(alunosDataElement.textContent) : [];
let filteredAlunos = [...alunosData];

// Obter total de alunos a partir do elemento metadata (inserido no template)
const metadataEl = document.getElementById('alunos-metadata');
const TOTAL_ALUNOS = metadataEl ? parseInt(metadataEl.dataset.total || '0', 10) : (alunosData.length || 0);

// Função para filtrar alunos
function filtrarAlunos() {
    const searchTerm = document.getElementById('searchInput') ? document.getElementById('searchInput').value.toLowerCase() : '';
    const filterValue = document.getElementById('filterSelect') ? document.getElementById('filterSelect').value : 'todos';

    filteredAlunos = alunosData.filter(aluno => {
        const matchesSearch = aluno.nome.toLowerCase().includes(searchTerm) ||
                            (aluno.matricula && aluno.matricula.toLowerCase().includes(searchTerm)) ||
                            (aluno.curso && aluno.curso.toLowerCase().includes(searchTerm));

        let matchesFilter = true;
        switch(filterValue) {
            case 'ativos':
                matchesFilter = aluno.situacao === 'Ativo';
                break;
            case 'suspensos':
                matchesFilter = aluno.situacao === 'Suspenso';
                break;
            case 'transporte':
                matchesFilter = Array.isArray(aluno.auxilios) && aluno.auxilios.includes('Transporte');
                break;
            case 'alimentacao':
                matchesFilter = Array.isArray(aluno.auxilios) && aluno.auxilios.includes('Alimentação');
                break;
            case 'moradia':
                matchesFilter = Array.isArray(aluno.auxilios) && aluno.auxilios.includes('Moradia');
                break;
            case 'material':
                matchesFilter = Array.isArray(aluno.auxilios) && aluno.auxilios.includes('Material Didático');
                break;
        }

        return matchesSearch && matchesFilter;
    });

    // Esconder/mostrar linhas da tabela (renderização feita pelo Jinja2 no servidor)
    const tbody = document.getElementById('alunosTableBody');
    if (!tbody) return;
    const rows = tbody.querySelectorAll('tr');

    rows.forEach(row => {
        const alunoId = parseInt(row.dataset.alunoId);
        const shouldShow = filteredAlunos.some(aluno => Number(aluno.id_usuario) === alunoId);
        row.style.display = shouldShow ? '' : 'none';
    });

    // Atualizar contador
    const resultsCountEl = document.getElementById('resultsCount');
    if (resultsCountEl) {
        resultsCountEl.textContent = `Mostrando ${filteredAlunos.length} de ${TOTAL_ALUNOS} alunos`;
    }

    // Mostrar estado de "sem resultados" se necessário
    const noResults = document.getElementById('noResultsState');
    if (filteredAlunos.length === 0 && searchTerm) {
        if (noResults) noResults.style.display = 'block';
        tbody.style.display = 'none';
    } else {
        if (noResults) noResults.style.display = 'none';
        tbody.style.display = '';
    }
}

// Event listeners para busca e filtros
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const filterSelect = document.getElementById('filterSelect');
    if (searchInput) searchInput.addEventListener('input', filtrarAlunos);
    if (filterSelect) filterSelect.addEventListener('change', filtrarAlunos);

    // Inicializar filtro para aplicar qualquer valor inicial
    filtrarAlunos();
});

// Função para limpar filtros
function clearFilters() {
    const searchInput = document.getElementById('searchInput');
    const filterSelect = document.getElementById('filterSelect');
    if (searchInput) searchInput.value = '';
    if (filterSelect) filterSelect.value = 'todos';
    filtrarAlunos();
}

// Funções para ações dos botões (mantemos simples placeholders para serem implementados)
function visualizarAluno(id) {
    // redirecionamento para rota de detalhes (ajuste conforme sua rota)
    window.location.href = `/assistente/alunos/detalhes?id=${id}`;
}

function editarAluno(id) {
    window.location.href = `/assistente/alunos/editar?id=${id}`;
}

function historicoAluno(id) {
    window.location.href = `/assistente/alunos/historico?id=${id}`;
}

// Função para exportar dados
function exportarDados() {
    const csvContent = "data:text/csv;charset=utf-8," 
        + "Nome,Matrícula,Curso,Auxílios,Valor Mensal,Situação\n"
        + filteredAlunos.map(aluno => 
            `"${aluno.nome}","${aluno.matricula}","${aluno.curso}","${(aluno.auxilios||[]).join('; ')}","R$ ${Number(aluno.valor_mensal || aluno.valorTotal || 0).toFixed(2)}","${aluno.situacao}"`
        ).join("\n");

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "alunos_auxilios.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Exportar funções para uso global pelo template (botões inline chamam essas funções)
window.visualizarAluno = visualizarAluno;
window.editarAluno = editarAluno;
window.historicoAluno = historicoAluno;
window.clearFilters = clearFilters;
window.exportarDados = exportarDados;
