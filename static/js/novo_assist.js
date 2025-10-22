/* ==========================================
   CADASTRAR NOVO ASSISTENTE - JAVASCRIPT
   ========================================== */

document.addEventListener('DOMContentLoaded', function() {
    // ===== INICIALIZAÇÃO =====
    setupFormValidation();
    setupFieldValidation();
});

// ===== VALIDAÇÃO DE CAMPOS ===== 
function setupFieldValidation() {
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

// ===== CONFIGURAR VALIDAÇÃO DE FORMULÁRIOS =====
function setupFormValidation() {
    const form = document.getElementById('assistantForm');
    
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            event.stopPropagation();
            
            if (form.checkValidity()) {
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
    const form = document.getElementById('assistantForm');
    form.submit();
}