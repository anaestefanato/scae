/* ==========================================
   GERENCIAR ALUNOS - JAVASCRIPT
   ========================================== */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Inicializando gerenciamento de alunos...');
    console.log('Total de alunos carregados:', window.alunos ? window.alunos.length : 0);
});
// ===== FUNÇÕES DE PAGINAÇÃO =====
function gerarPaginacao(paginaAtual, totalPaginas) {
    const paginationControls = document.getElementById('paginationControls');
    if (!paginationControls) return;
    
    paginationControls.innerHTML = '';

    // Botão Anterior
    const liAnterior = document.createElement('li');
    liAnterior.className = `page-item ${paginaAtual === 1 ? 'disabled' : ''}`;
    liAnterior.innerHTML = `<a class="page-link" href="${paginaAtual === 1 ? '#' : '?pagina=' + (paginaAtual - 1)}">Anterior</a>`;
    paginationControls.appendChild(liAnterior);

    // Lógica para mostrar páginas
    let startPage = Math.max(1, paginaAtual - 2);
    let endPage = Math.min(totalPaginas, paginaAtual + 2);

    // Primeira página
    if (startPage > 1) {
        const li = document.createElement('li');
        li.className = 'page-item';
        li.innerHTML = `<a class="page-link" href="?pagina=1">1</a>`;
        paginationControls.appendChild(li);

        if (startPage > 2) {
            const liEllipsis = document.createElement('li');
            liEllipsis.className = 'page-item disabled';
            liEllipsis.innerHTML = '<a class="page-link">...</a>';
            paginationControls.appendChild(liEllipsis);
        }
    }

    // Páginas do meio
    for (let i = startPage; i <= endPage; i++) {
        const li = document.createElement('li');
        li.className = `page-item ${i === paginaAtual ? 'active' : ''}`;
        li.innerHTML = `<a class="page-link" href="?pagina=${i}">${i}</a>`;
        paginationControls.appendChild(li);
    }

    // Última página
    if (endPage < totalPaginas) {
        if (endPage < totalPaginas - 1) {
            const liEllipsis = document.createElement('li');
            liEllipsis.className = 'page-item disabled';
            liEllipsis.innerHTML = '<a class="page-link">...</a>';
            paginationControls.appendChild(liEllipsis);
        }

        const li = document.createElement('li');
        li.className = 'page-item';
        li.innerHTML = `<a class="page-link" href="?pagina=${totalPaginas}">${totalPaginas}</a>`;
        paginationControls.appendChild(li);
    }

    // Botão Próximo
    const liProximo = document.createElement('li');
    liProximo.className = `page-item ${paginaAtual === totalPaginas ? 'disabled' : ''}`;
    liProximo.innerHTML = `<a class="page-link" href="${paginaAtual === totalPaginas ? '#' : '?pagina=' + (paginaAtual + 1)}">Próximo</a>`;
    paginationControls.appendChild(liProximo);
}

// ===== FUNÇÕES DE GERENCIAMENTO DE ALUNOS =====

// Visualizar detalhes do aluno
function viewStudentReal(id) {
    const aluno = window.alunos.find(a => a.id_usuario === id);
    
    if (aluno) {
        // Preencher dados pessoais
        document.getElementById('viewNome').textContent = aluno.nome || '-';
        document.getElementById('viewCpf').textContent = aluno.cpf || '-';
        document.getElementById('viewMatricula').textContent = aluno.matricula || '-';
        document.getElementById('viewEmail').textContent = aluno.email || '-';
        document.getElementById('viewTelefone').textContent = aluno.telefone || '-';
        document.getElementById('viewDataNascimento').textContent = aluno.data_nascimento || '-';
        document.getElementById('viewFiliacao').textContent = aluno.filiacao || '-';
        
        // Dados Acadêmicos
        document.getElementById('viewCurso').textContent = aluno.curso || '-';
        document.getElementById('viewPeriodo').textContent = aluno.periodo || '-';
        
        // Dados de Endereço
        document.getElementById('viewCep').textContent = aluno.cep || '-';
        document.getElementById('viewRua').textContent = aluno.logradouro || '-';
        document.getElementById('viewBairro').textContent = aluno.bairro || '-';
        document.getElementById('viewCidade').textContent = aluno.cidade || '-';
        document.getElementById('viewEstado').textContent = aluno.estado || '-';
        document.getElementById('viewNumero').textContent = aluno.numero || '-';
        document.getElementById('viewComplemento').textContent = aluno.complemento || '-';
        document.getElementById('viewSituacaoMoradia').textContent = aluno.situacao_moradia || '-';
        
        // Dados Bancários
        document.getElementById('viewNomeBanco').textContent = aluno.nome_banco || '-';
        document.getElementById('viewAgenciaBancaria').textContent = aluno.agencia_bancaria || '-';
        document.getElementById('viewNumeroContaBancaria').textContent = aluno.numero_conta_bancaria || '-';
        
        // Dados Socioeconômicos
        document.getElementById('viewRendaFamiliar').textContent = aluno.renda_familiar ? `R$ ${parseFloat(aluno.renda_familiar).toFixed(2)}` : '-';
        document.getElementById('viewQuantidadePessoas').textContent = aluno.quantidade_pessoas || '-';
        document.getElementById('viewRendaPerCapita').textContent = aluno.renda_per_capita ? `R$ ${parseFloat(aluno.renda_per_capita).toFixed(2)}` : '-';
        
        // Auxílios Ativos
        const auxiliosContainer = document.getElementById('viewAuxilios');
        if (aluno.auxilios && aluno.auxilios.length > 0) {
            const auxiliosList = aluno.auxilios.split(',').map(aux => 
                `<span class="badge bg-primary me-2">${aux.trim().toUpperCase()}</span>`
            ).join('');
            auxiliosContainer.innerHTML = auxiliosList;
        } else {
            auxiliosContainer.innerHTML = '<span class="text-muted">Nenhum auxílio ativo</span>';
        }
        
        // Abrir o modal
        const modal = new bootstrap.Modal(document.getElementById('viewStudentModal'));
        modal.show();
    } else {
        console.error('Aluno não encontrado:', id);
    }
}

// Editar aluno
function editStudentReal(id) {
    window.location.href = `/admin/usuarios/aluno/editar/${id}`;
}

// Excluir aluno
let studentToDeleteId = null;
function deleteStudentReal(id) {
    // Buscar o aluno pelo id
    const aluno = window.alunos.find(a => a.id_usuario == id);
    
    if (aluno) {
        // Guardar o ID para exclusão
        studentToDeleteId = id;
        
        // Preencher informações no modal
        document.getElementById('deleteStudentName').textContent = aluno.nome;
        document.getElementById('deleteStudentMatricula').textContent = aluno.matricula;
        document.getElementById('deleteStudentCpf').textContent = aluno.cpf || '-';
        
        // Abrir o modal
        const modal = new bootstrap.Modal(document.getElementById('deleteStudentModal'));
        modal.show();
    }
}

function confirmDeleteStudent() {
    if (studentToDeleteId) {
        // Criar formulário para enviar requisição DELETE via POST
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/admin/usuarios/aluno/excluir/${studentToDeleteId}`;
        document.body.appendChild(form);
        form.submit();
    }
}

// Buscar aluno
function searchStudentReal() {
    const searchTerm = document.getElementById('searchStudent').value.toLowerCase().trim();
    
    if (!searchTerm) {
        clearSearchReal();
        return;
    }
    
    const results = window.alunos.filter(a => 
        a.nome.toLowerCase().includes(searchTerm) ||
        a.matricula.toLowerCase().includes(searchTerm) ||
        (a.cpf && a.cpf.toLowerCase().includes(searchTerm))
    );
    
    const tbody = document.getElementById('studentsTableBody');
    tbody.innerHTML = '';
    
    if (results.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="text-center text-muted py-4">
                    <i class="bi bi-search fs-1 d-block mb-2"></i>
                    Nenhum aluno encontrado com "${searchTerm}"
                </td>
            </tr>
        `;
    } else {
        results.forEach(aluno => {
            tbody.innerHTML += `
                <tr>
                    <td style="padding: 15px;"><strong>${aluno.nome}</strong></td>
                    <td style="padding: 15px;">${aluno.matricula}</td>
                    <td style="padding: 15px;">${aluno.cpf || '-'}</td>
                    <td style="padding: 15px;">
                        <span class="text-muted">-</span>
                    </td>
                    <td style="padding: 15px;">
                        <div class="action-buttons" style="display: flex; gap: 8px; justify-content: center;">
                            <button class="btn btn-sm btn-outline-info" onclick="viewStudentReal(${aluno.id_usuario})">
                                <i class="bi bi-eye"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-secondary" onclick="editStudentReal(${aluno.id_usuario})">
                                <i class="bi bi-pencil"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-danger" onclick="deleteStudentReal(${aluno.id_usuario})">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `;
        });
    }
    
    document.getElementById('studentsCount').textContent = results.length;
}

// Limpar busca
function clearSearchReal() {
    document.getElementById('searchStudent').value = '';
    
    const tbody = document.getElementById('studentsTableBody');
    tbody.innerHTML = '';
    
    window.alunos.forEach(aluno => {
        tbody.innerHTML += `
            <tr>
                <td style="padding: 15px;"><strong>${aluno.nome}</strong></td>
                <td style="padding: 15px;">${aluno.matricula}</td>
                <td style="padding: 15px;">${aluno.cpf || '-'}</td>
                <td style="padding: 15px;">
                    <span class="text-muted">-</span>
                </td>
                <td style="padding: 15px;">
                    <div class="action-buttons" style="display: flex; gap: 8px; justify-content: center;">
                        <button class="btn btn-sm btn-outline-info" onclick="viewStudentReal(${aluno.id_usuario})">
                            <i class="bi bi-eye"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-secondary" onclick="editStudentReal(${aluno.id_usuario})">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteStudentReal(${aluno.id_usuario})">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    });
    
    document.getElementById('studentsCount').textContent = window.alunos.length;
}

// Filtrar alunos
function filterStudentsReal() {
    const filtro = document.getElementById('filterCategory').value;
    const urlParams = new URLSearchParams(window.location.search);
    
    if (filtro) {
        urlParams.set('filtro', filtro);
    } else {
        urlParams.delete('filtro');
    }
    
    urlParams.delete('pagina');
    window.location.search = urlParams.toString();
}

// ===== INICIALIZAÇÃO =====
if (typeof window.paginaAtual !== 'undefined' && typeof window.totalPaginas !== 'undefined') {
    document.addEventListener('DOMContentLoaded', function() {
        gerarPaginacao(window.paginaAtual, window.totalPaginas);
        
        // Configurar event listener para busca
        const searchInput = document.getElementById('searchStudent');
        if (searchInput) {
            searchInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    searchStudentReal();
                }
            });
        }
    });
}
