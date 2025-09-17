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


// Preview de foto de perfil
document.addEventListener('DOMContentLoaded', function() {
    const fotoInput = document.getElementById('foto');
    const fotoAtual = document.getElementById('foto-atual');
    const previewContainer = document.getElementById('preview-foto-container');
    const previewFoto = document.getElementById('preview-foto');
    const btnAlterar = document.getElementById('btn-alterar');
    const btnCancelar = document.getElementById('btn-cancelar');

    fotoInput.addEventListener('change', function(e) {
        const file = e.target.files[0];

        if (file) {
            // Verificar se é uma imagem
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();

                reader.onload = function(e) {
                    // Esconder foto atual e mostrar preview
                    fotoAtual.style.display = 'none';
                    previewFoto.src = e.target.result;
                    previewContainer.style.display = 'block';

                    // Habilitar botão e mostrar opções
                    btnAlterar.disabled = false;
                    btnAlterar.innerHTML = '<i class="bi-check"></i> Confirmar Alteração';
                    btnCancelar.style.display = 'inline-block';
                };

                reader.readAsDataURL(file);  // ← Converte arquivo em URL para preview
            } else {
                alert('Por favor, selecione apenas arquivos de imagem.');
                cancelarSelecao();
            }
        } else {
            cancelarSelecao();
        }
    });
});

function cancelarSelecao() {
    const fotoInput = document.getElementById('foto');
    const fotoAtual = document.getElementById('foto-atual');
    const previewContainer = document.getElementById('preview-foto-container');
    const btnAlterar = document.getElementById('btn-alterar');
    const btnCancelar = document.getElementById('btn-cancelar');

    // Limpar seleção e voltar ao estado inicial
    fotoInput.value = '';
    fotoAtual.style.display = 'block';
    previewContainer.style.display = 'none';
    btnAlterar.disabled = true;
    btnAlterar.innerHTML = '<i class="bi-camera"></i> Alterar Foto';
    btnCancelar.style.display = 'none';
}