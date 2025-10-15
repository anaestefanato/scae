// JavaScript para a página Analisar Cadastros

let currentUserId = null;

function visualizarDetalhes(id, nome, matricula, email, dataCadastro) {
    currentUserId = id;
    document.getElementById('modalNome').textContent = nome;
    document.getElementById('modalMatricula').textContent = matricula;
    document.getElementById('modalEmail').textContent = email;
    document.getElementById('modalDataCadastro').textContent = dataCadastro ? dataCadastro.replace('T', ' às ') : 'Não informado';
    
    const modal = new bootstrap.Modal(document.getElementById('detalhesUsuarioModal'));
    modal.show();
}

function atualizarLista() {
    location.reload();
}

function filtrarPor(tipo) {
    // Implementar filtros se necessário
    console.log('Filtrar por:', tipo);
}

function toggleSelectAll() {
    const selectAll = document.getElementById('selectAll');
    const checkboxes = document.querySelectorAll('.row-checkbox');
    checkboxes.forEach(cb => cb.checked = selectAll.checked);
    updateSelectedCount();
}

function updateSelectedCount() {
    const checkboxes = document.querySelectorAll('.row-checkbox:checked');
    const count = checkboxes.length;
    document.getElementById('selectedCount').textContent = count;
    
    const batchActions = document.getElementById('batchActions');
    if (count > 0) {
        batchActions.style.display = 'block';
    } else {
        batchActions.style.display = 'none';
    }
}

function aprovarSelecionados() {
    const checkboxes = document.querySelectorAll('.row-checkbox:checked');
    if (checkboxes.length === 0) return;
    
    const ids = Array.from(checkboxes).map(cb => cb.value);
    if (confirm(`Aprovar ${ids.length} cadastro(s) selecionado(s)?`)) {
        // Implementar aprovação em lote
        alert('Funcionalidade de aprovação em lote será implementada.');
    }
}

function rejeitarSelecionados() {
    const checkboxes = document.querySelectorAll('.row-checkbox:checked');
    if (checkboxes.length === 0) return;
    
    const ids = Array.from(checkboxes).map(cb => cb.value);
    if (confirm(`Rejeitar ${ids.length} cadastro(s) selecionado(s)? Esta ação é irreversível.`)) {
        // Implementar rejeição em lote
        alert('Funcionalidade de rejeição em lote será implementada.');
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Checkboxes individuais
    const checkboxes = document.querySelectorAll('.row-checkbox');
    checkboxes.forEach(cb => {
        cb.addEventListener('change', updateSelectedCount);
    });

    // Botões do modal
    document.getElementById('aprovarModalBtn').addEventListener('click', function() {
        if (currentUserId && confirm('Aprovar este cadastro?')) {
            // Criar form e submeter
            const form = document.createElement('form');
            form.method = 'post';
            form.action = `/admin/aprovar-usuario/${currentUserId}`;
            document.body.appendChild(form);
            form.submit();
        }
    });

    document.getElementById('rejeitarModalBtn').addEventListener('click', function() {
        if (currentUserId && confirm('Rejeitar este cadastro? Esta ação é irreversível.')) {
            // Criar form e submeter
            const form = document.createElement('form');
            form.method = 'post';
            form.action = `/admin/rejeitar-usuario/${currentUserId}`;
            document.body.appendChild(form);
            form.submit();
        }
    });
});
