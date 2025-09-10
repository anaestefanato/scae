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
    let message = '';
    let historyTitle = '';
    
    switch(formId) {
        case 'pessoal':
            message = 'Dados pessoais salvos com sucesso!';
            historyTitle = 'Atualização de Dados Pessoais';
            break;
        case 'endereco':
            message = 'Dados de endereço salvos com sucesso!';
            historyTitle = 'Atualização de Endereço';
            break;
        case 'bancario':
            message = 'Dados bancários salvos com sucesso!';
            historyTitle = 'Atualização de Dados Bancários';
            break;
        case 'todos_os_dados':
            message = 'Todas as alterações foram salvas com sucesso!';
            historyTitle = 'Atualização Geral do Perfil';
            break;
        default:
            message = 'Alterações salvas com sucesso!';
            historyTitle = 'Atualização nos dados';
    }
    
    alert(message);
    
    // Adiciona o registro no histórico
    const today = new Date().toLocaleDateString('pt-BR');
    const historyContainer = document.querySelector('.history-item').parentElement;
    const newHistoryItem = document.createElement('div');
    newHistoryItem.className = 'history-item';
    newHistoryItem.innerHTML = `
        <div class="d-flex justify-content-between align-items-start">
            <div>
                <h6 class="mb-1">${historyTitle}</h6>
                <p class="mb-0 text-muted small">Alteração nos dados</p>
            </div>
            <span class="history-date">${today}</span>
        </div>
    `;
    historyContainer.insertBefore(newHistoryItem, historyContainer.firstChild);
}

function saveAllChanges() {
    // Coleta dados de todos os formulários
    const forms = ['pessoal', 'endereco', 'bancario'];
    let allData = {};
    
    forms.forEach(formId => {
        const form = document.getElementById('form' + formId.charAt(0).toUpperCase() + formId.slice(1));
        if (form) {
            const fields = form.querySelectorAll('input, select, textarea');
            fields.forEach(field => {
                if (field.name) {
                    allData[field.name] = field.value;
                } else {
                    // Se não tem name, usa o label como identificador
                    const label = field.closest('.col-md-6, .col-md-4')?.querySelector('label')?.textContent || 'campo_sem_nome';
                    allData[label.toLowerCase().replace(/\s+/g, '_')] = field.value;
                }
            });
        }
    });
    
    console.log('Dados coletados:', allData);
    
    // Chama a função saveChanges original
    saveChanges('todos_os_dados');
    
    // Adiciona feedback visual
    const button = document.querySelector('button[onclick="saveAllChanges()"]');
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="bi bi-check-circle"></i> Salvando...';
    button.disabled = true;
    
    setTimeout(() => {
        button.innerHTML = '<i class="bi bi-check-circle-fill"></i> Salvo!';
        setTimeout(() => {
            button.innerHTML = originalText;
            button.disabled = false;
        }, 1500);
    }, 1000);
}

function savePhoto() {
    // Aqui você pode adicionar a lógica para salvar a nova foto no backend
    alert('Foto atualizada com sucesso!');
    // Fecha o modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('changePhotoModal'));
    modal.hide();
}
