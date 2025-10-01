// =============================
// CADASTRAR NOVO ADMINISTRADOR - JAVASCRIPT SIMPLIFICADO
// =============================

document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript do Novo Administrador carregado com sucesso');
    
    // ===== ELEMENTOS DO DOM =====
    const form = document.getElementById('adminForm');
    const nome = document.getElementById('nome');
    const matricula = document.getElementById('matricula');
    const email = document.getElementById('email');
    const tipoAdmin = document.getElementById('tipo_admin');
    const senha = document.getElementById('senha');
    const btnSubmit = document.querySelector('button[type="submit"]');
    
    // ===== VALIDAÇÃO DE EMAIL =====
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
    
    // ===== VALIDAÇÃO DE SENHA =====
    function validatePassword(password) {
        return password.length >= 8;
    }
    
    // ===== EVENTOS DE VALIDAÇÃO =====
    if (email) {
        email.addEventListener('blur', function() {
            const isValid = validateEmail(this.value);
            this.classList.remove('is-valid', 'is-invalid');
            
            if (this.value && isValid) {
                this.classList.add('is-valid');
            } else if (this.value) {
                this.classList.add('is-invalid');
            }
        });
    }
    
    if (senha) {
        senha.addEventListener('input', function() {
            const isValid = validatePassword(this.value);
            this.classList.remove('is-valid', 'is-invalid');
            
            if (this.value && isValid) {
                this.classList.add('is-valid');
            } else if (this.value) {
                this.classList.add('is-invalid');
            }
        });
    }
    
    // ===== MÁSCARA PARA MATRÍCULA =====
    // Removido: permitir letras e números na matrícula
    // if (matricula) {
    //     matricula.addEventListener('input', function(e) {
    //         // Apenas números
    //         let value = e.target.value.replace(/\D/g, '');
    //         e.target.value = value;
    //     });
    // }
    
    // ===== VALIDAÇÃO DO FORMULÁRIO =====
    function validateForm() {
        let isValid = true;
        
        // Limpar validações anteriores
        const inputs = form.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.classList.remove('is-invalid');
        });
        
        // Validar campos obrigatórios
        if (!nome.value.trim()) {
            nome.classList.add('is-invalid');
            isValid = false;
        }
        
        if (!matricula.value.trim()) {
            matricula.classList.add('is-invalid');
            isValid = false;
        }
        
        if (!email.value.trim() || !validateEmail(email.value)) {
            email.classList.add('is-invalid');
            isValid = false;
        }
        
        if (!tipoAdmin.value) {
            tipoAdmin.classList.add('is-invalid');
            isValid = false;
        }
        
        if (!senha.value || !validatePassword(senha.value)) {
            senha.classList.add('is-invalid');
            isValid = false;
        }
        
        return isValid;
    }
    
    // ===== SUBMISSÃO DO FORMULÁRIO =====
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            if (validateForm()) {
                // Mostrar modal de confirmação ao invés de submeter diretamente
                showConfirmModal();
            } else {
                showAlert('Por favor, corrija os campos destacados em vermelho.', 'danger');
            }
        });
    }
    
    // ===== MOSTRAR MODAL DE CONFIRMAÇÃO =====
    window.showConfirmModal = function() {
        const modal = new bootstrap.Modal(document.getElementById('confirmModal'));
        modal.show();
    }
    
    // ===== CONFIRMAR CADASTRO =====
    window.confirmCadastro = function() {
        const modal = bootstrap.Modal.getInstance(document.getElementById('confirmModal'));
        modal.hide();
        
        // Enviar dados para o servidor
        submitAdminForm();
    }
    
    // ===== ENVIAR FORMULÁRIO =====
    async function submitAdminForm() {
        showLoadingState();
        
        try {
            const formData = new FormData(form);
            
            const response = await fetch('/admin/usuarios/admin/novo', {
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
                    hideLoadingState();
                    showAlert('Erro ao cadastrar administrador. Verifique os dados informados.', 'danger');
                } else {
                    hideLoadingState();
                    showSuccessMessage();
                }
            } else {
                hideLoadingState();
                showAlert('Erro ao cadastrar administrador. Tente novamente.', 'danger');
            }
            
        } catch (error) {
            hideLoadingState();
            console.error('Erro ao enviar formulário:', error);
            showAlert('Erro de conexão. Tente novamente.', 'danger');
        }
    }
    
    // ===== ESTADOS DE CARREGAMENTO =====
    function showLoadingState() {
        if (btnSubmit) {
            btnSubmit.disabled = true;
            btnSubmit.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Cadastrando...';
        }
        showAlert('Cadastrando administrador...', 'info');
    }
    
    function hideLoadingState() {
        if (btnSubmit) {
            btnSubmit.disabled = false;
            btnSubmit.innerHTML = '<i class="bi bi-check-circle me-2"></i>Cadastrar Administrador';
        }
    }
    
    // ===== MENSAGEM DE SUCESSO =====
    function showSuccessMessage() {
        showAlert('Administrador cadastrado com sucesso!', 'success');
        
        setTimeout(() => {
            // Redirecionar para a lista de administradores
            window.location.href = '/admin/usuarios/admin';
        }, 2000);
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
                <i class="bi bi-${type === 'success' ? 'check-circle' : type === 'danger' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
                <span>${message}</span>
                <button type="button" class="btn-close ms-auto" onclick="this.parentElement.parentElement.remove()"></button>
            </div>
        `;
        
        document.body.appendChild(alert);
        
        // Remover automaticamente após 5 segundos
        setTimeout(() => {
            if (alert && alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }
    
    // ===== CSS PARA ANIMAÇÕES =====
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
    `;
    document.head.appendChild(style);
    
    console.log('JavaScript do Novo Administrador inicializado com sucesso!');
});