// ============================================================================
// TEMPORIZADOR PARA MENSAGENS DE SUCESSO E ERRO
// ============================================================================
document.addEventListener('DOMContentLoaded', function() {
    // Mensagem de sucesso - desaparece após 5 segundos
    const mensagemSucesso = document.getElementById('mensagem-sucesso');
    if (mensagemSucesso) {
        setTimeout(function() {
            // Usar o método fade do Bootstrap para suavizar o desaparecimento
            const alert = new bootstrap.Alert(mensagemSucesso);
            mensagemSucesso.style.transition = 'opacity 0.5s ease';
            mensagemSucesso.style.opacity = '0';
            
            setTimeout(function() {
                alert.close();
            }, 500);
        }, 5000); // 5 segundos
    }

    // Mensagem de erro - desaparece após 8 segundos (mais tempo para ler)
    const mensagemErro = document.getElementById('mensagem-erro');
    if (mensagemErro) {
        setTimeout(function() {
            const alert = new bootstrap.Alert(mensagemErro);
            mensagemErro.style.transition = 'opacity 0.5s ease';
            mensagemErro.style.opacity = '0';
            
            setTimeout(function() {
                alert.close();
            }, 500);
        }, 8000); // 8 segundos
    }
});

// ============================================================================
// FUNCIONALIDADE DE CONSULTA DE CEP
// ============================================================================
document.addEventListener('DOMContentLoaded', function() {
    const cepInput = document.getElementById('cep');
    const btnBuscarCep = document.getElementById('btn-buscar-cep');
    const cepLoading = document.getElementById('cep-loading');
    const cepError = document.getElementById('cep-error');
    const cidadeInput = document.getElementById('cidade');
    const bairroInput = document.getElementById('bairro');
    const ruaInput = document.getElementById('rua');
    const estadoInput = document.getElementById('estado');

    // Verificar se os elementos existem antes de continuar
    if (!cepInput || !btnBuscarCep) return;

    // Função para formatar CEP
    function formatarCEP(cep) {
        cep = cep.replace(/\D/g, ''); // Remove tudo que não é dígito
        if (cep.length > 5) {
            cep = cep.substring(0, 5) + '-' + cep.substring(5, 8);
        }
        return cep;
    }

    // Função para validar CEP
    function validarCEP(cep) {
        const cepLimpo = cep.replace(/\D/g, '');
        return cepLimpo.length === 8 && /^\d{8}$/.test(cepLimpo);
    }

    // Função para limpar campos de endereço
    function limparEndereco() {
        ruaInput.value = '';
        bairroInput.value = '';
        cidadeInput.value = '';
        estadoInput.value = '';
    }

    // Função para buscar CEP na API ViaCEP
    async function buscarCEP(cep) {
        const cepLimpo = cep.replace(/\D/g, '');
        
        try {
            cepLoading.style.display = 'block';
            cepError.style.display = 'none';
            btnBuscarCep.disabled = true;

            const response = await fetch(`https://viacep.com.br/ws/${cepLimpo}/json/`);
            const data = await response.json();

            if (data.erro) {
                throw new Error('CEP não encontrado');
            }

            // Preencher campos automaticamente com animação
            if (data.logradouro) {
                ruaInput.value = data.logradouro;
                ruaInput.classList.add('campo-preenchido');
                setTimeout(() => ruaInput.classList.remove('campo-preenchido'), 2000);
            }
            
            if (data.bairro) {
                bairroInput.value = data.bairro;
                bairroInput.classList.add('campo-preenchido');
                setTimeout(() => bairroInput.classList.remove('campo-preenchido'), 2000);
            }
            
            if (data.localidade) {
                cidadeInput.value = data.localidade;
                cidadeInput.classList.add('campo-preenchido');
                setTimeout(() => cidadeInput.classList.remove('campo-preenchido'), 2000);
            }
            
            if (data.uf) {
                estadoInput.value = data.uf;
                estadoInput.classList.add('campo-preenchido');
                setTimeout(() => estadoInput.classList.remove('campo-preenchido'), 2000);
            }

            // Mostrar mensagem de sucesso temporariamente
            cepLoading.innerHTML = '<i class="bi bi-check-circle"></i> CEP encontrado!';
            cepLoading.className = 'form-text text-success';
            
            setTimeout(() => {
                cepLoading.style.display = 'none';
                cepLoading.innerHTML = '<i class="bi bi-hourglass-split"></i> Buscando CEP...';
                cepLoading.className = 'form-text text-primary';
            }, 2000);

        } catch (error) {
            cepError.style.display = 'block';
            cepLoading.style.display = 'none';
            limparEndereco();
        } finally {
            btnBuscarCep.disabled = false;
        }
    }

    // Event listener para formatação automática do CEP
    cepInput.addEventListener('input', function(e) {
        e.target.value = formatarCEP(e.target.value);
        
        const cepValido = validarCEP(e.target.value);
        btnBuscarCep.disabled = !cepValido;
        
        // Mudar ícone do botão baseado na validade do CEP
        if (cepValido) {
            btnBuscarCep.innerHTML = '<i class="bi bi-search"></i>';
            btnBuscarCep.classList.remove('btn-outline-secondary');
            btnBuscarCep.classList.add('btn-outline-primary');
        } else {
            btnBuscarCep.innerHTML = '<i class="bi bi-search"></i>';
            btnBuscarCep.classList.remove('btn-outline-primary');
            btnBuscarCep.classList.add('btn-outline-secondary');
        }
        
        // Esconder mensagens de erro quando o usuário digita
        cepError.style.display = 'none';
        cepLoading.style.display = 'none';
    });

    // Event listener para busca automática ao sair do campo
    cepInput.addEventListener('blur', function(e) {
        if (validarCEP(e.target.value)) {
            buscarCEP(e.target.value);
        }
    });

    // Event listener para o botão de busca
    btnBuscarCep.addEventListener('click', function() {
        if (validarCEP(cepInput.value)) {
            buscarCEP(cepInput.value);
        }
    });

    // Event listener para busca com Enter
    cepInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            if (validarCEP(e.target.value)) {
                buscarCEP(e.target.value);
            }
        }
    });
});

// ============================================================================
// PREVIEW DE FOTO DE PERFIL NO MODAL
// ============================================================================
document.addEventListener('DOMContentLoaded', function() {
    const fotoInput = document.getElementById('foto');
    const previewContainer = document.getElementById('preview-foto-container');
    const previewFoto = document.getElementById('preview-foto');
    const btnAlterarFoto = document.getElementById('btn-alterar-foto');
    const modal = document.getElementById('changePhotoModal');
    const fotoAtual = document.getElementById('foto-atual');

    // Verificar se os elementos existem antes de continuar
    if (!fotoInput || !modal) return;

    console.log('Modal script carregado'); // Debug
    
    // Verificar se todos os elementos foram encontrados
    console.log('Elementos encontrados:');
    console.log('fotoInput:', fotoInput);
    console.log('previewContainer:', previewContainer);
    console.log('previewFoto:', previewFoto);
    console.log('btnAlterarFoto:', btnAlterarFoto);
    console.log('modal:', modal);

    // Função para atualizar a foto atual com cache busting
    function atualizarFotoAtual() {
        if (fotoAtual) {
            const timestamp = new Date().getTime();
            const srcAtual = fotoAtual.src.split('?')[0]; // Remove query string existente
            fotoAtual.src = srcAtual + '?v=' + timestamp;
        }
    }

    // Função para cancelar seleção
    function cancelarSelecao() {
        console.log('Cancelando seleção'); // Debug
        fotoInput.value = '';
        previewContainer.style.display = 'none';
        btnAlterarFoto.disabled = true;
        btnAlterarFoto.innerHTML = '<i class="bi bi-camera"></i> Alterar Foto';
    }

    // Reset modal quando fechar
    modal.addEventListener('hidden.bs.modal', function() {
        cancelarSelecao();
    });

    fotoInput.addEventListener('change', function(e) {
        console.log('Arquivo selecionado:', e.target.files[0]); // Debug
        const file = e.target.files[0];

        if (file) {
            // Verificar se é uma imagem
            if (file.type.startsWith('image/')) {
                console.log('Arquivo é uma imagem válida'); // Debug
                const reader = new FileReader();

                reader.onload = function(e) {
                    console.log('FileReader carregou a imagem'); // Debug
                    // Mostrar preview
                    previewFoto.src = e.target.result;
                    previewContainer.style.display = 'block';

                    // Habilitar botão
                    btnAlterarFoto.disabled = false;
                    btnAlterarFoto.innerHTML = '<i class="bi bi-check"></i> Confirmar Alteração';
                    console.log('Botão habilitado'); // Debug
                };

                reader.readAsDataURL(file);
            } else {
                alert('Por favor, selecione apenas arquivos de imagem.');
                cancelarSelecao();
            }
        } else {
            cancelarSelecao();
        }
    });

    // Expor função globalmente para uso do botão cancelar
    window.cancelarSelecao = cancelarSelecao;
});

// ============================================================================
// FUNÇÕES ANTIGAS (MANTIDAS PARA COMPATIBILIDADE)
// ============================================================================
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