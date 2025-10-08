/* ==========================================
   CADASTRAR NOVO ASSISTENTE - JAVASCRIPT
   ========================================== */

document.addEventListener('DOMContentLoaded', function() {
    // ===== INICIALIZAÇÃO =====
    initializeNewAssistantForm();
    setupFormValidation();
    setupMasks();
    setupFieldValidation();
});

// ===== VARIÁVEIS GLOBAIS =====
let formData = {};

// ===== INICIALIZAÇÃO =====
function initializeNewAssistantForm() {
    // Configurar tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Configurar data máxima para data de nascimento (18 anos atrás)
    const today = new Date();
    const minDate = new Date(today.getFullYear() - 70, today.getMonth(), today.getDate());
    const maxDate = new Date(today.getFullYear() - 18, today.getMonth(), today.getDate());
    
    const dataNascimento = document.getElementById('dataNascimento');
    if (dataNascimento) {
        dataNascimento.min = minDate.toISOString().split('T')[0];
        dataNascimento.max = maxDate.toISOString().split('T')[0];
    }
    
    // Configurar data de admissão (não pode ser futura)
    const dataAdmissao = document.getElementById('dataAdmissao');
    if (dataAdmissao) {
        dataAdmissao.max = today.toISOString().split('T')[0];
        dataAdmissao.min = '1990-01-01'; // Data mínima razoável
    }
    
    console.log('Formulário de novo assistente inicializado');
}

// ===== MÁSCARAS DE ENTRADA =====
function setupMasks() {
    // Máscara para CPF
    const cpfField = document.getElementById('cpf');
    if (cpfField) {
        cpfField.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
            e.target.value = value;
        });
    }
    
    // Máscara para telefone
    const telefoneField = document.getElementById('telefone');
    if (telefoneField) {
        telefoneField.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{2})(\d)/, '($1) $2');
            value = value.replace(/(\d{5})(\d)/, '$1-$2');
            e.target.value = value;
        });
    }
}

// ===== VALIDAÇÃO DE CAMPOS ===== 
function setupFieldValidation() {
    // Validação de CPF
    const cpfField = document.getElementById('cpf');
    if (cpfField) {
        cpfField.addEventListener('blur', function() {
            const cpf = this.value.replace(/\D/g, '');
            if (cpf.length === 11) {
                if (isValidCPF(cpf)) {
                    this.classList.add('is-valid');
                    this.classList.remove('is-invalid');
                } else {
                    this.classList.add('is-invalid');
                    this.classList.remove('is-valid');
                    this.nextElementSibling.textContent = 'CPF inválido.';
                }
            }
        });
    }
    
    // Validação de email
    const emailField = document.getElementById('email');
    if (emailField) {
        emailField.addEventListener('blur', function() {
            const email = this.value.toLowerCase();
            if (email && email.includes('@')) {
                this.classList.add('is-valid');
                this.classList.remove('is-invalid');
            } else if (email && !email.includes('@')) {
                this.classList.add('is-invalid');
                this.classList.remove('is-valid');
                this.nextElementSibling.textContent = 'Por favor, informe um email válido.';
            }
        });
    }
}

// ===== VALIDAÇÃO DE CPF =====
function isValidCPF(cpf) {
    // Eliminar CPFs inválidos conhecidos
    if (cpf == "00000000000" || 
        cpf == "11111111111" || 
        cpf == "22222222222" || 
        cpf == "33333333333" || 
        cpf == "44444444444" || 
        cpf == "55555555555" || 
        cpf == "66666666666" || 
        cpf == "77777777777" || 
        cpf == "88888888888" || 
        cpf == "99999999999")
        return false;
        
    // Valida 1º dígito
    let add = 0;
    for (let i = 0; i < 9; i++) {
        add += parseInt(cpf.charAt(i)) * (10 - i);
    }
    let rev = 11 - (add % 11);
    if (rev == 10 || rev == 11) {
        rev = 0;
    }
    if (rev != parseInt(cpf.charAt(9))) {
        return false;
    }
    
    // Valida 2º dígito
    add = 0;
    for (let i = 0; i < 10; i++) {
        add += parseInt(cpf.charAt(i)) * (11 - i);
    }
    rev = 11 - (add % 11);
    if (rev == 10 || rev == 11) {
        rev = 0;
    }
    if (rev != parseInt(cpf.charAt(10))) {
        return false;
    }
    
    return true;
}

// ===== CONFIGURAR VALIDAÇÃO DE FORMULÁRIOS =====
function setupFormValidation() {
    const form = document.getElementById('assistantForm');
    
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            event.stopPropagation();
            
            if (form.checkValidity()) {
                collectFormData();
                showConfirmModal();
            } else {
                // Encontrar primeiro campo inválido e focar nele
                const firstInvalidField = form.querySelector(':invalid');
                if (firstInvalidField) {
                    firstInvalidField.focus();
                    firstInvalidField.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
            
            form.classList.add('was-validated');
        });
    }
}

// ===== COLETAR DADOS DO FORMULÁRIO =====
function collectFormData() {
    const form = document.getElementById('assistantForm');
    const formDataObj = new FormData(form);
    
    formData = {};
    for (let [key, value] of formDataObj.entries()) {
        formData[key] = value;
    }
}

// ===== VISUALIZAR DADOS =====
function previewData() {
    const form = document.getElementById('assistantForm');
    
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        showNotification('Por favor, preencha todos os campos obrigatórios antes de visualizar.', 'warning');
        return;
    }
    
    collectFormData();
    
    const previewContent = document.getElementById('previewContent');
    
    previewContent.innerHTML = `
        <div class="preview-section">
            <h6><i class="bi bi-person-circle me-2"></i>Dados Pessoais</h6>
            <div class="preview-item">
                <span class="label">Nome Completo:</span>
                <span class="value">${formData.nomeCompleto || '-'}</span>
            </div>
            <div class="preview-item">
                <span class="label">CPF:</span>
                <span class="value">${formData.cpf || '-'}</span>
            </div>
            <div class="preview-item">
                <span class="label">Data de Nascimento:</span>
                <span class="value">${formatDate(formData.dataNascimento) || '-'}</span>
            </div>
            <div class="preview-item">
                <span class="label">Sexo:</span>
                <span class="value">${formatSexo(formData.sexo) || '-'}</span>
            </div>
            <div class="preview-item">
                <span class="label">Estado Civil:</span>
                <span class="value">${formatEstadoCivil(formData.estadoCivil) || '-'}</span>
            </div>
        </div>
        
        <div class="preview-section">
            <h6><i class="bi bi-briefcase me-2"></i>Dados Profissionais</h6>
            <div class="preview-item">
                <span class="label">Matrícula SIAPE:</span>
                <span class="value">${formData.matricula || '-'}</span>
            </div>
            <div class="preview-item">
                <span class="label">Área de Atuação:</span>
                <span class="value">${formatAreaAtuacao(formData.areaAtuacao) || '-'}</span>
            </div>
            <div class="preview-item">
                <span class="label">Conselho Profissional:</span>
                <span class="value">${formData.conselhoProfissional || '-'}</span>
            </div>
            <div class="preview-item">
                <span class="label">Número de Registro:</span>
                <span class="value">${formData.numeroRegistro || '-'}</span>
            </div>
            <div class="preview-item">
                <span class="label">Data de Admissão:</span>
                <span class="value">${formatDate(formData.dataAdmissao) || '-'}</span>
            </div>
            <div class="preview-item">
                <span class="label">Regime de Trabalho:</span>
                <span class="value">${formatRegime(formData.regime) || '-'}</span>
            </div>
            <div class="preview-item">
                <span class="label">Status:</span>
                <span class="value">${formatStatus(formData.status) || '-'}</span>
            </div>
        </div>
        
        <div class="preview-section">
            <h6><i class="bi bi-telephone me-2"></i>Dados de Contato</h6>
            <div class="preview-item">
                <span class="label">Email Institucional:</span>
                <span class="value">${formData.email || '-'}</span>
            </div>
            <div class="preview-item">
                <span class="label">Email Pessoal:</span>
                <span class="value">${formData.emailPessoal || '-'}</span>
            </div>
            <div class="preview-item">
                <span class="label">Telefone:</span>
                <span class="value">${formData.telefone || '-'}</span>
            </div>
            <div class="preview-item">
                <span class="label">Ramal:</span>
                <span class="value">${formData.ramal || '-'}</span>
            </div>
        </div>
        
        <div class="preview-section">
            <h6><i class="bi bi-mortarboard me-2"></i>Formação Acadêmica</h6>
            <div class="preview-item">
                <span class="label">Graduação:</span>
                <span class="value">${formData.graduacao || '-'}</span>
            </div>
            <div class="preview-item">
                <span class="label">Instituição de Graduação:</span>
                <span class="value">${formData.instituicaoGraduacao || '-'}</span>
            </div>
            <div class="preview-item">
                <span class="label">Pós-Graduação:</span>
                <span class="value">${formData.posGraduacao || '-'}</span>
            </div>
            <div class="preview-item">
                <span class="label">Instituição da Pós-Graduação:</span>
                <span class="value">${formData.instituicaoPosGraduacao || '-'}</span>
            </div>
        </div>
    `;
    
    const modal = new bootstrap.Modal(document.getElementById('previewModal'));
    modal.show();
}

// ===== FUNÇÕES DE FORMATAÇÃO =====
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString + 'T00:00:00');
    return date.toLocaleDateString('pt-BR');
}

function formatSexo(sexo) {
    const sexos = {
        'masculino': 'Masculino',
        'feminino': 'Feminino',
        'outros': 'Outros',
        'prefiro-nao-informar': 'Prefiro não informar'
    };
    return sexos[sexo] || sexo;
}

function formatEstadoCivil(estado) {
    const estados = {
        'solteiro': 'Solteiro(a)',
        'casado': 'Casado(a)',
        'divorciado': 'Divorciado(a)',
        'viuvo': 'Viúvo(a)',
        'uniao-estavel': 'União Estável'
    };
    return estados[estado] || estado;
}

function formatAreaAtuacao(area) {
    const areas = {
        'servico-social': 'Serviço Social',
        'psicologia': 'Psicologia',
        'pedagogia': 'Pedagogia',
        'nutricao': 'Nutrição',
        'enfermagem': 'Enfermagem',
        'terapia-ocupacional': 'Terapia Ocupacional'
    };
    return areas[area] || area;
}

function formatRegime(regime) {
    const regimes = {
        '20h': '20 horas',
        '40h': '40 horas',
        'dedicacao-exclusiva': 'Dedicação Exclusiva'
    };
    return regimes[regime] || regime;
}

function formatStatus(status) {
    const statusMap = {
        'ativo': 'Ativo',
        'inativo': 'Inativo',
        'ferias': 'Em Férias',
        'licenca': 'Em Licença'
    };
    return statusMap[status] || status;
}

// ===== EDITAR DADOS =====
function editData() {
    // Apenas fecha o modal de preview para voltar ao formulário
    showNotification('Você pode editar os dados no formulário abaixo.', 'info');
}

// ===== MOSTRAR MODAL DE CONFIRMAÇÃO =====
function showConfirmModal() {
    const modal = new bootstrap.Modal(document.getElementById('confirmModal'));
    modal.show();
}

// ===== CONFIRMAR CADASTRO =====
function confirmCadastro() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('confirmModal'));
    modal.hide();
    
    // Enviar dados para o servidor
    submitAssistantForm();
}

// ===== ENVIAR FORMULÁRIO =====
async function submitAssistantForm() {
    showLoadingState();
    
    try {
        const form = document.getElementById('assistantForm');
        const formData = new FormData(form);
        
        const response = await fetch('/admin/usuarios/assistente/novo', {
            method: 'POST',
            body: formData,
            redirect: 'manual' // Não seguir redirecionamentos automaticamente
        });
        
        // Se retornou 303 (redirect), significa sucesso
        if (response.status === 303 || response.type === 'opaqueredirect') {
            hideLoadingState();
            showSuccessMessage();
        } else if (response.ok) {
            // Verificar se o HTML retornado contém erro
            const html = await response.text();
            if (html.includes('alert-danger') || html.includes('erro')) {
                // Recarregar a página com o HTML retornado para mostrar o erro específico
                document.open();
                document.write(html);
                document.close();
            } else {
                hideLoadingState();
                showSuccessMessage();
            }
        } else {
            hideLoadingState();
            showNotification('Erro ao cadastrar assistente. Tente novamente.', 'danger');
        }
        
    } catch (error) {
        hideLoadingState();
        console.error('Erro ao enviar formulário:', error);
        showNotification('Erro de conexão. Tente novamente.', 'danger');
    }
}

// ===== ESTADOS DE CARREGAMENTO =====
function showLoadingState() {
    document.body.classList.add('loading');
    showNotification('Cadastrando assistente...', 'info');
}

function hideLoadingState() {
    document.body.classList.remove('loading');
}

// ===== MENSAGEM DE SUCESSO =====
function showSuccessMessage() {
    showNotification('Assistente cadastrado com sucesso!', 'success');
    
    setTimeout(() => {
        // Redirecionar para a lista de assistentes
        window.location.href = '/admin/usuarios/assistente';
    }, 2000);
}

// ===== MOSTRAR NOTIFICAÇÕES =====
function showNotification(message, type = 'info') {
    // Remover notificações existentes
    const existingNotifications = document.querySelectorAll('.notification-toast');
    existingNotifications.forEach(notification => notification.remove());
    
    // Criar elemento de notificação
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed notification-toast`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px; max-width: 500px;';
    notification.innerHTML = `
        ${getNotificationIcon(type)} ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Adicionar ao body
    document.body.appendChild(notification);
    
    // Remover automaticamente após 5 segundos
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

function getNotificationIcon(type) {
    const icons = {
        'success': '<i class="bi bi-check-circle me-2"></i>',
        'warning': '<i class="bi bi-exclamation-triangle me-2"></i>',
        'info': '<i class="bi bi-info-circle me-2"></i>',
        'danger': '<i class="bi bi-x-circle me-2"></i>'
    };
    return icons[type] || icons['info'];
}

// ===== EVENTOS DE TECLADO =====
document.addEventListener('keydown', function(event) {
    // Ctrl + Enter para enviar formulário
    if (event.ctrlKey && event.key === 'Enter') {
        const form = document.getElementById('assistantForm');
        if (form) {
            form.dispatchEvent(new Event('submit'));
        }
    }
    
    // Escape para cancelar
    if (event.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show');
        if (modals.length > 0) {
            const lastModal = modals[modals.length - 1];
            const modalInstance = bootstrap.Modal.getInstance(lastModal);
            if (modalInstance) {
                modalInstance.hide();
            }
        }
    }
});