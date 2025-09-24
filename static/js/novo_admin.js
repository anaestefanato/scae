// =============================
// CADASTRAR NOVO ADMINISTRADOR - JAVASCRIPT
// =============================

document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript do Novo Administrador carregado com sucesso');
    
    // ===== CONFIGURAÇÕES GERAIS =====
    const CONFIG = {
        masks: {
            cpf: '000.000.000-00',
            phone: '(00) 00000-0000',
            cep: '00000-000'
        },
        validation: {
            minPasswordLength: 8,
            maxPasswordLength: 50
        }
    };

    // ===== ELEMENTOS DO DOM =====
    const elements = {
        // Formulário principal
        form: document.getElementById('formNovoAdmin'),
        
        // Campos de dados pessoais
        nome: document.getElementById('nome'),
        cpf: document.getElementById('cpf'),
        dataNascimento: document.getElementById('data_nascimento'),
        email: document.getElementById('email'),
        telefone: document.getElementById('telefone'),
        
        // Endereço
        cep: document.getElementById('cep'),
        logradouro: document.getElementById('logradouro'),
        numero: document.getElementById('numero'),
        complemento: document.getElementById('complemento'),
        bairro: document.getElementById('bairro'),
        cidade: document.getElementById('cidade'),
        estado: document.getElementById('estado'),
        
        // Credenciais de acesso
        usuario: document.getElementById('usuario'),
        senha: document.getElementById('senha'),
        confirmarSenha: document.getElementById('confirmar_senha'),
        
        // Configurações específicas
        nivel: document.getElementById('nivel_acesso'),
        departamento: document.getElementById('departamento'),
        cargo: document.getElementById('cargo'),
        dataInicio: document.getElementById('data_inicio'),
        
        // Botões
        btnBuscarCep: document.getElementById('btnBuscarCep'),
        btnGerarUsuario: document.getElementById('btnGerarUsuario'),
        btnVerificarDisponibilidade: document.getElementById('btnVerificarDisponibilidade'),
        btnSalvar: document.getElementById('btnSalvar'),
        btnVisualizar: document.getElementById('btnVisualizar'),
        btnLimpar: document.getElementById('btnLimpar'),
        
        // Modals
        modalPreview: new bootstrap.Modal(document.getElementById('modalPreview')),
        modalLimpar: new bootstrap.Modal(document.getElementById('modalLimpar')),
        
        // Containers de preview
        previewPessoais: document.getElementById('previewDadosPessoais'),
        previewEndereco: document.getElementById('previewEndereco'),
        previewCredenciais: document.getElementById('previewCredenciais'),
        previewConfiguracoes: document.getElementById('previewConfiguracoes'),
        previewPermissoes: document.getElementById('previewPermissoes'),
        
        // Senha
        passwordStrength: document.getElementById('passwordStrength'),
        passwordStrengthFill: document.querySelector('.password-strength-fill'),
        passwordStrengthText: document.querySelector('.password-strength-text')
    };

    // ===== MÁSCARAS DE ENTRADA =====
    function initMasks() {
        // Máscara para CPF
        if (elements.cpf) {
            elements.cpf.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length <= 11) {
                    value = value.replace(/(\d{3})(\d)/, '$1.$2');
                    value = value.replace(/(\d{3})(\d)/, '$1.$2');
                    value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
                }
                e.target.value = value;
            });
        }
        
        // Máscara para telefone
        if (elements.telefone) {
            elements.telefone.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length <= 11) {
                    value = value.replace(/(\d{2})(\d)/, '($1) $2');
                    value = value.replace(/(\d{4,5})(\d{4})$/, '$1-$2');
                }
                e.target.value = value;
            });
        }
        
        // Máscara para CEP
        if (elements.cep) {
            elements.cep.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length <= 8) {
                    value = value.replace(/(\d{5})(\d)/, '$1-$2');
                }
                e.target.value = value;
            });
        }
    }

    // ===== VALIDAÇÕES =====
    function validateCPF(cpf) {
        cpf = cpf.replace(/[^\d]/g, '');
        if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) return false;
        
        let sum = 0;
        for (let i = 0; i < 9; i++) {
            sum += parseInt(cpf.charAt(i)) * (10 - i);
        }
        let rev = 11 - (sum % 11);
        if (rev === 10 || rev === 11) rev = 0;
        if (rev !== parseInt(cpf.charAt(9))) return false;
        
        sum = 0;
        for (let i = 0; i < 10; i++) {
            sum += parseInt(cpf.charAt(i)) * (11 - i);
        }
        rev = 11 - (sum % 11);
        if (rev === 10 || rev === 11) rev = 0;
        if (rev !== parseInt(cpf.charAt(10))) return false;
        
        return true;
    }

    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    function validatePhone(phone) {
        const cleaned = phone.replace(/\D/g, '');
        return cleaned.length >= 10;
    }

    function validatePassword(password) {
        return {
            length: password.length >= CONFIG.validation.minPasswordLength,
            hasUpper: /[A-Z]/.test(password),
            hasLower: /[a-z]/.test(password),
            hasNumber: /\d/.test(password),
            hasSpecial: /[!@#$%^&*(),.?":{}|<>]/.test(password)
        };
    }

    function getPasswordStrength(password) {
        const checks = validatePassword(password);
        const score = Object.values(checks).filter(Boolean).length;
        
        if (score <= 2) return { level: 'weak', width: 33, text: 'Senha Fraca' };
        if (score <= 4) return { level: 'medium', width: 66, text: 'Senha Média' };
        return { level: 'strong', width: 100, text: 'Senha Forte' };
    }

    // ===== FUNÇÕES DE VALIDAÇÃO DE CAMPOS =====
    function validateField(field, validationFn, errorMsg) {
        const isValid = validationFn(field.value);
        const feedback = field.parentNode.querySelector('.invalid-feedback') || 
                        field.parentNode.querySelector('.valid-feedback');
        
        field.classList.remove('is-valid', 'is-invalid');
        
        if (isValid) {
            field.classList.add('is-valid');
            if (feedback) {
                feedback.className = 'valid-feedback';
                feedback.textContent = 'Campo válido!';
            }
        } else {
            field.classList.add('is-invalid');
            if (feedback) {
                feedback.className = 'invalid-feedback';
                feedback.textContent = errorMsg;
            }
        }
        
        return isValid;
    }

    // ===== EVENTOS DE VALIDAÇÃO EM TEMPO REAL =====
    function initValidation() {
        // CPF
        if (elements.cpf) {
            elements.cpf.addEventListener('blur', function() {
                validateField(this, validateCPF, 'CPF inválido');
            });
        }
        
        // Email
        if (elements.email) {
            elements.email.addEventListener('blur', function() {
                validateField(this, validateEmail, 'Email inválido');
            });
        }
        
        // Telefone
        if (elements.telefone) {
            elements.telefone.addEventListener('blur', function() {
                validateField(this, validatePhone, 'Telefone inválido');
            });
        }
        
        // Senha
        if (elements.senha) {
            elements.senha.addEventListener('input', function() {
                const strength = getPasswordStrength(this.value);
                
                if (elements.passwordStrengthFill) {
                    elements.passwordStrengthFill.style.width = strength.width + '%';
                    elements.passwordStrengthFill.className = `password-strength-fill ${strength.level}`;
                }
                
                if (elements.passwordStrengthText) {
                    elements.passwordStrengthText.textContent = strength.text;
                    elements.passwordStrengthText.className = `password-strength-text text-${strength.level === 'weak' ? 'danger' : strength.level === 'medium' ? 'warning' : 'success'}`;
                }
                
                // Validar confirmação se já foi preenchida
                if (elements.confirmarSenha && elements.confirmarSenha.value) {
                    validatePasswordMatch();
                }
            });
        }
        
        // Confirmar senha
        if (elements.confirmarSenha) {
            elements.confirmarSenha.addEventListener('input', validatePasswordMatch);
        }
    }

    function validatePasswordMatch() {
        if (!elements.senha || !elements.confirmarSenha) return;
        
        const match = elements.senha.value === elements.confirmarSenha.value;
        const feedback = elements.confirmarSenha.parentNode.querySelector('.invalid-feedback') ||
                        elements.confirmarSenha.parentNode.querySelector('.valid-feedback');
        
        elements.confirmarSenha.classList.remove('is-valid', 'is-invalid');
        
        if (match && elements.senha.value.length > 0) {
            elements.confirmarSenha.classList.add('is-valid');
            if (feedback) {
                feedback.className = 'valid-feedback';
                feedback.textContent = 'Senhas coincidem!';
            }
        } else if (elements.confirmarSenha.value.length > 0) {
            elements.confirmarSenha.classList.add('is-invalid');
            if (feedback) {
                feedback.className = 'invalid-feedback';
                feedback.textContent = 'As senhas não coincidem';
            }
        }
    }

    // ===== BUSCA DE CEP =====
    function initCepSearch() {
        if (elements.btnBuscarCep && elements.cep) {
            elements.btnBuscarCep.addEventListener('click', async function() {
                const cep = elements.cep.value.replace(/\D/g, '');
                
                if (cep.length !== 8) {
                    showAlert('Por favor, insira um CEP válido com 8 dígitos.', 'warning');
                    return;
                }
                
                try {
                    this.disabled = true;
                    this.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Buscando...';
                    
                    const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
                    const data = await response.json();
                    
                    if (data.erro) {
                        throw new Error('CEP não encontrado');
                    }
                    
                    // Preencher campos
                    if (elements.logradouro) elements.logradouro.value = data.logradouro || '';
                    if (elements.bairro) elements.bairro.value = data.bairro || '';
                    if (elements.cidade) elements.cidade.value = data.localidade || '';
                    if (elements.estado) elements.estado.value = data.uf || '';
                    
                    // Focar no campo número
                    if (elements.numero) elements.numero.focus();
                    
                    showAlert('Endereço encontrado com sucesso!', 'success');
                    
                } catch (error) {
                    showAlert('Erro ao buscar CEP: ' + error.message, 'danger');
                } finally {
                    this.disabled = false;
                    this.innerHTML = '<i class="bi bi-search me-2"></i>Buscar';
                }
            });
        }
    }

    // ===== GERAÇÃO DE USUÁRIO =====
    function initUserGeneration() {
        if (elements.btnGerarUsuario && elements.nome && elements.usuario) {
            elements.btnGerarUsuario.addEventListener('click', function() {
                const nome = elements.nome.value.trim();
                if (!nome) {
                    showAlert('Por favor, preencha o nome primeiro.', 'warning');
                    return;
                }
                
                // Gerar usuário baseado no nome
                const partesNome = nome.toLowerCase().split(' ').filter(parte => parte.length > 2);
                let usuario = '';
                
                if (partesNome.length >= 2) {
                    usuario = partesNome[0] + '.' + partesNome[partesNome.length - 1];
                } else {
                    usuario = partesNome[0];
                }
                
                // Remover acentos e caracteres especiais
                usuario = usuario.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
                usuario = usuario.replace(/[^a-z0-9.]/g, '');
                
                elements.usuario.value = usuario;
                elements.usuario.focus();
                
                showAlert('Nome de usuário gerado com sucesso!', 'success');
            });
        }
    }

    // ===== VERIFICAÇÃO DE DISPONIBILIDADE DE USUÁRIO =====
    function initUserAvailabilityCheck() {
        if (elements.btnVerificarDisponibilidade && elements.usuario) {
            elements.btnVerificarDisponibilidade.addEventListener('click', async function() {
                const usuario = elements.usuario.value.trim();
                
                if (!usuario) {
                    showAlert('Por favor, insira um nome de usuário.', 'warning');
                    return;
                }
                
                try {
                    this.disabled = true;
                    this.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Verificando...';
                    
                    // Simular verificação (substituir pela chamada real da API)
                    await new Promise(resolve => setTimeout(resolve, 1000));
                    
                    const disponivel = Math.random() > 0.3; // Simulação
                    
                    if (disponivel) {
                        elements.usuario.classList.remove('is-invalid');
                        elements.usuario.classList.add('is-valid');
                        showAlert('Nome de usuário disponível!', 'success');
                    } else {
                        elements.usuario.classList.remove('is-valid');
                        elements.usuario.classList.add('is-invalid');
                        showAlert('Nome de usuário já está em uso. Tente outro.', 'danger');
                    }
                    
                } catch (error) {
                    showAlert('Erro ao verificar disponibilidade: ' + error.message, 'danger');
                } finally {
                    this.disabled = false;
                    this.innerHTML = '<i class="bi bi-check-circle me-2"></i>Verificar';
                }
            });
        }
    }

    // ===== PREVIEW DO FORMULÁRIO =====
    function generatePreview() {
        if (!elements.previewPessoais) return;
        
        // Dados pessoais
        elements.previewPessoais.innerHTML = `
            <div class="preview-item">
                <span class="label">Nome:</span>
                <span class="value">${elements.nome?.value || 'Não informado'}</span>
            </div>
            <div class="preview-item">
                <span class="label">CPF:</span>
                <span class="value">${elements.cpf?.value || 'Não informado'}</span>
            </div>
            <div class="preview-item">
                <span class="label">Data de Nascimento:</span>
                <span class="value">${elements.dataNascimento?.value || 'Não informado'}</span>
            </div>
            <div class="preview-item">
                <span class="label">Email:</span>
                <span class="value">${elements.email?.value || 'Não informado'}</span>
            </div>
            <div class="preview-item">
                <span class="label">Telefone:</span>
                <span class="value">${elements.telefone?.value || 'Não informado'}</span>
            </div>
        `;
        
        // Endereço
        if (elements.previewEndereco) {
            elements.previewEndereco.innerHTML = `
                <div class="preview-item">
                    <span class="label">CEP:</span>
                    <span class="value">${elements.cep?.value || 'Não informado'}</span>
                </div>
                <div class="preview-item">
                    <span class="label">Endereço:</span>
                    <span class="value">${elements.logradouro?.value || 'Não informado'}, ${elements.numero?.value || 'S/N'}</span>
                </div>
                <div class="preview-item">
                    <span class="label">Complemento:</span>
                    <span class="value">${elements.complemento?.value || 'Não informado'}</span>
                </div>
                <div class="preview-item">
                    <span class="label">Bairro:</span>
                    <span class="value">${elements.bairro?.value || 'Não informado'}</span>
                </div>
                <div class="preview-item">
                    <span class="label">Cidade:</span>
                    <span class="value">${elements.cidade?.value || 'Não informado'}</span>
                </div>
                <div class="preview-item">
                    <span class="label">Estado:</span>
                    <span class="value">${elements.estado?.value || 'Não informado'}</span>
                </div>
            `;
        }
        
        // Credenciais
        if (elements.previewCredenciais) {
            elements.previewCredenciais.innerHTML = `
                <div class="preview-item">
                    <span class="label">Nome de usuário:</span>
                    <span class="value">${elements.usuario?.value || 'Não informado'}</span>
                </div>
                <div class="preview-item">
                    <span class="label">Senha:</span>
                    <span class="value">${elements.senha?.value ? '****** (definida)' : 'Não informado'}</span>
                </div>
            `;
        }
        
        // Configurações
        if (elements.previewConfiguracoes) {
            elements.previewConfiguracoes.innerHTML = `
                <div class="preview-item">
                    <span class="label">Nível de Acesso:</span>
                    <span class="value">${elements.nivel?.selectedOptions[0]?.text || 'Não informado'}</span>
                </div>
                <div class="preview-item">
                    <span class="label">Departamento:</span>
                    <span class="value">${elements.departamento?.value || 'Não informado'}</span>
                </div>
                <div class="preview-item">
                    <span class="label">Cargo:</span>
                    <span class="value">${elements.cargo?.value || 'Não informado'}</span>
                </div>
                <div class="preview-item">
                    <span class="label">Data de Início:</span>
                    <span class="value">${elements.dataInicio?.value || 'Não informado'}</span>
                </div>
            `;
        }
        
        // Permissões
        if (elements.previewPermissoes) {
            const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
            const permissoes = Array.from(checkboxes).map(cb => {
                const label = cb.parentNode.querySelector('strong')?.textContent || cb.value;
                return `<span class="permission-badge active">${label}</span>`;
            });
            
            elements.previewPermissoes.innerHTML = permissoes.length > 0 
                ? permissoes.join(' ') 
                : '<em class="text-muted">Nenhuma permissão específica selecionada</em>';
        }
    }

    // ===== EVENTOS DOS BOTÕES =====
    function initButtonEvents() {
        // Visualizar
        if (elements.btnVisualizar) {
            elements.btnVisualizar.addEventListener('click', function() {
                generatePreview();
                elements.modalPreview.show();
            });
        }
        
        // Limpar formulário
        if (elements.btnLimpar) {
            elements.btnLimpar.addEventListener('click', function() {
                elements.modalLimpar.show();
            });
        }
        
        // Confirmar limpeza
        const btnConfirmarLimpar = document.getElementById('btnConfirmarLimpar');
        if (btnConfirmarLimpar) {
            btnConfirmarLimpar.addEventListener('click', function() {
                if (elements.form) {
                    elements.form.reset();
                    
                    // Remover classes de validação
                    const validatedFields = elements.form.querySelectorAll('.is-valid, .is-invalid');
                    validatedFields.forEach(field => {
                        field.classList.remove('is-valid', 'is-invalid');
                    });
                    
                    // Limpar barra de força da senha
                    if (elements.passwordStrengthFill) {
                        elements.passwordStrengthFill.style.width = '0%';
                        elements.passwordStrengthFill.className = 'password-strength-fill';
                    }
                    if (elements.passwordStrengthText) {
                        elements.passwordStrengthText.textContent = '';
                    }
                }
                
                elements.modalLimpar.hide();
                showAlert('Formulário limpo com sucesso!', 'success');
            });
        }
        
        // Salvar
        if (elements.btnSalvar && elements.form) {
            elements.btnSalvar.addEventListener('click', function() {
                if (validateForm()) {
                    submitForm();
                }
            });
        }
    }

    // ===== VALIDAÇÃO COMPLETA DO FORMULÁRIO =====
    function validateForm() {
        let isValid = true;
        const requiredFields = [
            { field: elements.nome, name: 'Nome' },
            { field: elements.cpf, name: 'CPF', validator: validateCPF },
            { field: elements.email, name: 'Email', validator: validateEmail },
            { field: elements.usuario, name: 'Nome de usuário' },
            { field: elements.senha, name: 'Senha' },
            { field: elements.confirmarSenha, name: 'Confirmação de senha' }
        ];
        
        requiredFields.forEach(({ field, name, validator }) => {
            if (!field || !field.value.trim()) {
                if (field) {
                    field.classList.add('is-invalid');
                    field.focus();
                }
                showAlert(`O campo "${name}" é obrigatório.`, 'danger');
                isValid = false;
                return;
            }
            
            if (validator && !validator(field.value)) {
                field.classList.add('is-invalid');
                field.focus();
                showAlert(`O campo "${name}" contém um valor inválido.`, 'danger');
                isValid = false;
                return;
            }
        });
        
        // Validar confirmação de senha
        if (elements.senha && elements.confirmarSenha && 
            elements.senha.value !== elements.confirmarSenha.value) {
            elements.confirmarSenha.classList.add('is-invalid');
            elements.confirmarSenha.focus();
            showAlert('As senhas não coincidem.', 'danger');
            isValid = false;
        }
        
        return isValid;
    }

    // ===== SUBMISSÃO DO FORMULÁRIO =====
    async function submitForm() {
        if (!elements.form) return;
        
        try {
            elements.btnSalvar.disabled = true;
            elements.btnSalvar.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Salvando...';
            
            const formData = new FormData(elements.form);
            
            // Simular envio (substituir pela chamada real da API)
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            showAlert('Administrador cadastrado com sucesso!', 'success');
            
            // Redirecionar após sucesso
            setTimeout(() => {
                window.location.href = '/admin/usuarios_admin';
            }, 2000);
            
        } catch (error) {
            showAlert('Erro ao cadastrar administrador: ' + error.message, 'danger');
        } finally {
            elements.btnSalvar.disabled = false;
            elements.btnSalvar.innerHTML = '<i class="bi bi-check-lg me-2"></i>Cadastrar Administrador';
        }
    }

    // ===== FUNÇÃO PARA EXIBIR ALERTAS =====
    function showAlert(message, type = 'info') {
        // Remover alertas existentes
        const existingAlerts = document.querySelectorAll('.alert-floating');
        existingAlerts.forEach(alert => alert.remove());
        
        // Criar novo alerta
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-floating position-fixed`;
        alert.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            max-width: 500px;
            animation: slideInRight 0.3s ease-out;
        `;
        alert.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="bi bi-${type === 'success' ? 'check-circle' : type === 'danger' ? 'exclamation-triangle' : type === 'warning' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
                <span>${message}</span>
                <button type="button" class="btn-close ms-auto" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        document.body.appendChild(alert);
        
        // Remover automaticamente após 5 segundos
        setTimeout(() => {
            if (alert && alert.parentNode) {
                alert.style.animation = 'slideOutRight 0.3s ease-out';
                setTimeout(() => alert.remove(), 300);
            }
        }, 5000);
    }

    // ===== CSS ADICIONAL PARA ANIMAÇÕES =====
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

    // ===== INICIALIZAÇÃO =====
    function init() {
        console.log('Inicializando JavaScript do Novo Administrador...');
        
        initMasks();
        initValidation();
        initCepSearch();
        initUserGeneration();
        initUserAvailabilityCheck();
        initButtonEvents();
        
        console.log('JavaScript do Novo Administrador inicializado com sucesso!');
    }

    // ===== EXECUTAR INICIALIZAÇÃO =====
    init();
});

// ===== FUNÇÕES GLOBAIS (se necessário) =====
window.NovoAdminJS = {
    showAlert: function(message, type) {
        // Função global para mostrar alertas se necessário
        const event = new CustomEvent('showAlert', { 
            detail: { message, type } 
        });
        document.dispatchEvent(event);
    }
};