document.addEventListener('DOMContentLoaded', function() {
    // Funcionalidades específicas da página já implementadas
});

function toggleEdit(formId) {
    const form = document.getElementById('form' + formId.charAt(0).toUpperCase() + formId.slice(1));
    const inputs = form.getElementsByTagName('input');
    const button = form.closest('.card').querySelector('.btn-outline-success');
    if (inputs[0].disabled) {
        // Habilitar edição
        for (let input of inputs) {
            input.disabled = false;
        }
        button.innerHTML = '<i class="bi bi-check-lg"></i> Salvar';
        button.classList.add('active');
    } else {
        // Salvar alterações
        saveChanges(formId);
        for (let input of inputs) {
            input.disabled = true;
        }
        button.innerHTML = '<i class="bi bi-pencil"></i> Editar';
        button.classList.remove('active');
    }
}

function saveChanges(formId) {
    // Aqui você pode adicionar a lógica para salvar as alterações no backend
    alert('Alterações salvas com sucesso!');
    // Adiciona o registro no histórico
    const today = new Date().toLocaleDateString('pt-BR');
    const historyContainer = document.querySelector('.history-item').parentElement;
    const newHistoryItem = document.createElement('div');
    newHistoryItem.className = 'history-item';
    newHistoryItem.innerHTML = `
        <div class="d-flex justify-content-between align-items-start">
            <div>
                <h6 class="mb-1">Atualização de ${formId === 'pessoal' ? 'Dados Pessoais' : 'Endereço'}</h6>
                <p class="mb-0 text-muted small">Alteração nos dados</p>
            </div>
            <span class="history-date">${today}</span>
        </div>
    `;
    historyContainer.insertBefore(newHistoryItem, historyContainer.firstChild);
}

function savePhoto() {
    // Aqui você pode adicionar a lógica para salvar a nova foto no backend
    alert('Foto atualizada com sucesso!');
    // Fecha o modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('changePhotoModal'));
    modal.hide();
}
