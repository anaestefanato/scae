// =========================
// NOVA ENTREVISTA - JAVASCRIPT
// =========================

document.addEventListener('DOMContentLoaded', function() {
    initializeSidebar();
    initializeForm();
    initializeValidation();
    initializeModalityChange();
    initializeFormSubmission();
    setDefaultDateTime();
});

// ===== SIDEBAR FUNCTIONALITY =====
function initializeSidebar() {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    const closeSidebar = document.getElementById('closeSidebar');
    const mainContent = document.getElementById('mainContent');

    // Create backdrop
    const backdrop = document.createElement('div');
    backdrop.className = 'sidebar-backdrop';
    document.body.appendChild(backdrop);

    // Toggle sidebar
    menuToggle.addEventListener('click', function() {
        sidebar.classList.add('open');
        backdrop.classList.add('visible');
        menuToggle.classList.add('hidden');
        mainContent.classList.add('shifted');
    });

    // Close sidebar
    function closeSidebarFunction() {
        sidebar.classList.remove('open');
        backdrop.classList.remove('visible');
        menuToggle.classList.remove('hidden');
        mainContent.classList.remove('shifted');
    }

    closeSidebar.addEventListener('click', closeSidebarFunction);
    backdrop.addEventListener('click', closeSidebarFunction);

    // Close sidebar on ESC key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar.classList.contains('open')) {
            closeSidebarFunction();
        }
    });
}

// ===== FORM INITIALIZATION =====
function initializeForm() {
    // Format phone input
    const phoneInput = document.getElementById('alunoTelefone');
    phoneInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length <= 11) {
            value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
            if (value.length < 14) {
                value = value.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
            }
            e.target.value = value;
        }
    });

    // Format matricula input
    const matriculaInput = document.getElementById('alunoMatricula');
    matriculaInput.addEventListener('input', function(e) {
        e.target.value = e.target.value.toUpperCase();
    });

    // Auto-capitalize student name
    const nomeInput = document.getElementById('alunoNome');
    nomeInput.addEventListener('input', function(e) {
        e.target.value = e.target.value.replace(/\b\w/g, l => l.toUpperCase());
    });

    // Cancel button
    const btnCancelar = document.getElementById('btnCancelar');
    btnCancelar.addEventListener('click', function() {
        if (confirm('Tem certeza que deseja cancelar? Todos os dados preenchidos serão perdidos.')) {
            window.location.href = '/assistente/entrevistas';
        }
    });
}

// ===== VALIDATION =====
function initializeValidation() {
    const form = document.getElementById('novaEntrevistaForm');
    const inputs = form.querySelectorAll('input[required], select[required]');

    // Real-time validation
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });

        input.addEventListener('input', function() {
            if (this.classList.contains('is-invalid')) {
                validateField(this);
            }
        });
    });

    // Date validation
    const dataInput = document.getElementById('dataEntrevista');
    dataInput.addEventListener('change', function() {
        validateDate(this);
    });

    // Time validation
    const horaInput = document.getElementById('horaEntrevista');
    horaInput.addEventListener('change', function() {
        validateTime(this);
    });
}

function validateField(field) {
    const value = field.value.trim();
    let isValid = true;
    let message = '';

    // Required validation
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        message = 'Este campo é obrigatório.';
    }

    // Email validation
    if (field.type === 'email' && value && !isValidEmail(value)) {
        isValid = false;
        message = 'Por favor, insira um email válido.';
    }

    // URL validation
    if (field.type === 'url' && value && !isValidUrl(value)) {
        isValid = false;
        message = 'Por favor, insira uma URL válida.';
    }

    // Update field state
    if (isValid) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
        
        const feedback = field.nextElementSibling;
        if (feedback && feedback.classList.contains('invalid-feedback')) {
            feedback.textContent = message;
        }
    }

    return isValid;
}

function validateDate(dateInput) {
    const selectedDate = new Date(dateInput.value);
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    if (selectedDate < today) {
        dateInput.classList.add('is-invalid');
        dateInput.classList.remove('is-valid');
        
        const feedback = dateInput.nextElementSibling;
        if (feedback && feedback.classList.contains('invalid-feedback')) {
            feedback.textContent = 'A data não pode ser anterior a hoje.';
        }
        return false;
    }

    dateInput.classList.remove('is-invalid');
    dateInput.classList.add('is-valid');
    return true;
}

function validateTime(timeInput) {
    const selectedDate = document.getElementById('dataEntrevista').value;
    const selectedTime = timeInput.value;
    
    if (selectedDate && selectedTime) {
        const selectedDateTime = new Date(`${selectedDate}T${selectedTime}`);
        const now = new Date();

        if (selectedDateTime <= now) {
            timeInput.classList.add('is-invalid');
            timeInput.classList.remove('is-valid');
            
            const feedback = timeInput.nextElementSibling;
            if (feedback && feedback.classList.contains('invalid-feedback')) {
                feedback.textContent = 'O horário deve ser futuro.';
            }
            return false;
        }
    }

    timeInput.classList.remove('is-invalid');
    timeInput.classList.add('is-valid');
    return true;
}

// ===== MODALITY CHANGE HANDLER =====
function initializeModalityChange() {
    const modalidadeSelect = document.getElementById('modalidade');
    const localInput = document.getElementById('local');
    const localLabel = document.getElementById('localLabel');
    const localHelp = document.getElementById('localHelp');
    const linkOnlineRow = document.getElementById('linkOnlineRow');

    modalidadeSelect.addEventListener('change', function() {
        const modalidade = this.value;
        
        switch(modalidade) {
            case 'presencial':
                localLabel.innerHTML = '<i class="bi bi-building me-1"></i>Local/Sala';
                localInput.placeholder = 'Ex: Sala 201 - Bloco A';
                localHelp.textContent = 'Informe a sala onde será realizada a entrevista.';
                linkOnlineRow.style.display = 'none';
                break;
                
            case 'online':
                localLabel.innerHTML = '<i class="bi bi-camera-video me-1"></i>Plataforma';
                localInput.placeholder = 'Ex: Google Meet, Zoom, Teams';
                localHelp.textContent = 'Informe a plataforma que será utilizada.';
                linkOnlineRow.style.display = 'block';
                linkOnlineRow.classList.add('show');
                break;
                
            case 'hibrido':
                localLabel.innerHTML = '<i class="bi bi-geo-alt me-1"></i>Local Principal';
                localInput.placeholder = 'Ex: Sala 201 - Bloco A (com transmissão online)';
                localHelp.textContent = 'Local físico principal com opção de participação online.';
                linkOnlineRow.style.display = 'block';
                linkOnlineRow.classList.add('show');
                break;
                
            default:
                localLabel.innerHTML = '<i class="bi bi-building me-1"></i>Local/Sala';
                localInput.placeholder = 'Informe o local da entrevista';
                localHelp.textContent = 'Selecione primeiro a modalidade da entrevista.';
                linkOnlineRow.style.display = 'none';
        }
    });
}

// ===== FORM SUBMISSION =====
function initializeFormSubmission() {
    const form = document.getElementById('novaEntrevistaForm');
    const btnSubmit = document.getElementById('btnAgendar');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (validateForm()) {
            submitForm();
        }
    });
}

function validateForm() {
    const form = document.getElementById('novaEntrevistaForm');
    const requiredFields = form.querySelectorAll('input[required], select[required]');
    let isValid = true;

    // Validate all required fields
    requiredFields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });

    // Special validations
    if (!validateDate(document.getElementById('dataEntrevista'))) {
        isValid = false;
    }

    if (!validateTime(document.getElementById('horaEntrevista'))) {
        isValid = false;
    }

    // Check online link if needed
    const modalidade = document.getElementById('modalidade').value;
    const linkOnline = document.getElementById('linkOnline');
    
    if ((modalidade === 'online' || modalidade === 'hibrido') && !linkOnline.value) {
        linkOnline.classList.add('is-invalid');
        isValid = false;
    }

    form.classList.add('was-validated');
    
    if (!isValid) {
        // Scroll to first invalid field
        const firstInvalid = form.querySelector('.is-invalid');
        if (firstInvalid) {
            firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
            firstInvalid.focus();
        }
        
        showNotification('Por favor, corrija os erros no formulário.', 'error');
    }

    return isValid;
}

function submitForm() {
    const btnSubmit = document.getElementById('btnAgendar');
    const originalText = btnSubmit.innerHTML;
    
    // Show loading state
    btnSubmit.classList.add('loading');
    btnSubmit.disabled = true;
    
    // Collect form data
    const formData = collectFormData();
    
    // Simulate API call
    setTimeout(() => {
        console.log('Dados da entrevista:', formData);
        
        // Reset button
        btnSubmit.classList.remove('loading');
        btnSubmit.disabled = false;
        
        // Show success modal
        showSuccessModal(formData);
        
    }, 2000);
}

function collectFormData() {
    return {
        aluno: {
            nome: document.getElementById('alunoNome').value,
            matricula: document.getElementById('alunoMatricula').value,
            email: document.getElementById('alunoEmail').value,
            telefone: document.getElementById('alunoTelefone').value
        },
        entrevista: {
            tipo: document.getElementById('tipoEntrevista').value,
            auxilioTipo: document.getElementById('auxilioTipo').value,
            data: document.getElementById('dataEntrevista').value,
            hora: document.getElementById('horaEntrevista').value,
            duracao: document.getElementById('duracao').value,
            modalidade: document.getElementById('modalidade').value,
            local: document.getElementById('local').value,
            linkOnline: document.getElementById('linkOnline').value,
            prioridade: document.getElementById('prioridade').value,
            status: document.getElementById('status').value,
            observacoes: document.getElementById('observacoes').value
        },
        configuracoes: {
            notificarAluno: document.getElementById('notificarAluno').checked,
            lembrete: document.getElementById('lembrete').checked,
            confirmarPresenca: document.getElementById('confirmarPresenca').checked,
            anexarDocumentos: document.getElementById('anexarDocumentos').checked
        }
    };
}

function showSuccessModal(formData) {
    const modal = new bootstrap.Modal(document.getElementById('successModal'));
    const successMessage = document.getElementById('successMessage');
    const successDetails = document.getElementById('successDetails');
    
    const dataFormatada = formatDate(formData.entrevista.data);
    const horaFormatada = formData.entrevista.hora;
    
    successMessage.textContent = `Entrevista com ${formData.aluno.nome} agendada com sucesso!`;
    successDetails.textContent = `Data: ${dataFormatada} às ${horaFormatada}. ${formData.configuracoes.notificarAluno ? 'O aluno será notificado por email.' : ''}`;
    
    modal.show();
    
    // Reset form after showing modal
    setTimeout(() => {
        resetForm();
    }, 500);
}

// ===== UTILITY FUNCTIONS =====
function setDefaultDateTime() {
    // Set tomorrow as default date
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    document.getElementById('dataEntrevista').value = tomorrow.toISOString().split('T')[0];
    
    // Set 9:00 AM as default time
    document.getElementById('horaEntrevista').value = '09:00';
}

function resetForm() {
    const form = document.getElementById('novaEntrevistaForm');
    form.reset();
    form.classList.remove('was-validated');
    
    // Remove validation classes
    const fields = form.querySelectorAll('.form-control, .form-select');
    fields.forEach(field => {
        field.classList.remove('is-valid', 'is-invalid');
    });
    
    // Reset defaults
    setDefaultDateTime();
    document.getElementById('duracao').value = '60';
    document.getElementById('modalidade').value = 'presencial';
    document.getElementById('prioridade').value = 'media';
    document.getElementById('status').value = 'agendada';
    document.getElementById('notificarAluno').checked = true;
    document.getElementById('lembrete').checked = true;
    
    // Hide online link row
    document.getElementById('linkOnlineRow').style.display = 'none';
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidUrl(url) {
    try {
        new URL(url);
        return true;
    } catch {
        return false;
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show notification-toast`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        max-width: 400px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        border-radius: 10px;
        border: none;
    `;
    
    notification.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="bi bi-${type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
            ${message}
        </div>
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 4 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 4000);
}

// ===== EXPORT FOR GLOBAL ACCESS =====
window.NovaEntrevistaManager = {
    validateForm,
    submitForm,
    resetForm,
    showNotification
};