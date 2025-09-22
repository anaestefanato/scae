/* =======================
   EDITAIS PRIMEIRA INSCRIÇÃO - JAVASCRIPT
   ======================= */

// Sidebar functionality
let sidebarOpen = false;

function openSidebarFunction() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    
    if (sidebar && mainContent) {
        sidebar.classList.add('show');
        mainContent.classList.add('shifted');
        
        // Create backdrop
        const backdrop = document.createElement('div');
        backdrop.className = 'sidebar-backdrop';
        backdrop.id = 'sidebarBackdrop';
        document.body.appendChild(backdrop);
        
        // Show backdrop with animation
        setTimeout(() => backdrop.classList.add('show'), 10);
        
        // Click outside to close
        backdrop.addEventListener('click', closeSidebarFunction);
        
        sidebarOpen = true;
    }
}

function closeSidebarFunction() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    const backdrop = document.getElementById('sidebarBackdrop');
    
    if (sidebar && mainContent) {
        sidebar.classList.remove('show');
        mainContent.classList.remove('shifted');
        
        if (backdrop) {
            backdrop.classList.remove('show');
            setTimeout(() => {
                if (backdrop.parentNode) {
                    backdrop.parentNode.removeChild(backdrop);
                }
            }, 300);
        }
        
        sidebarOpen = false;
    }
}

// Multi-step form functionality
let currentStep = 1;
const totalSteps = 3;

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const submitButton = document.querySelector('.btn-primary');
    
    if (form) {
        // Real-time validation
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', validateField);
            input.addEventListener('input', clearValidation);
        });
        
        // Form submission
        form.addEventListener('submit', handleFormSubmission);
        
        // File upload progress
        const fileInputs = form.querySelectorAll('input[type="file"]');
        fileInputs.forEach(input => {
            input.addEventListener('change', handleFileUpload);
        });
        
        // Initialize progress
        updateFormProgress();
        updateStepProgress();
    }
    
    // CPF formatting
    const cpfInput = document.getElementById('cpf');
    if (cpfInput) {
        cpfInput.addEventListener('input', formatCPF);
    }
    
    // Phone formatting
    const phoneInput = document.getElementById('telefone');
    if (phoneInput) {
        phoneInput.addEventListener('input', formatPhone);
    }
    
    // Income formatting
    const incomeInput = document.getElementById('renda_familiar');
    if (incomeInput) {
        incomeInput.addEventListener('input', formatCurrency);
    }
});

// Step management
function updateStepProgress() {
    const steps = document.querySelectorAll('.step');
    const progressBar = document.querySelector('.progress-steps::after');
    
    steps.forEach((step, index) => {
        const stepNumber = index + 1;
        
        if (stepNumber < currentStep) {
            step.classList.add('completed');
            step.classList.remove('active');
        } else if (stepNumber === currentStep) {
            step.classList.add('active');
            step.classList.remove('completed');
        } else {
            step.classList.remove('active', 'completed');
        }
    });
    
    // Update progress bar
    const progressPercentage = ((currentStep - 1) / (totalSteps - 1)) * 100;
    if (progressBar) {
        progressBar.style.width = progressPercentage + '%';
    }
}

function nextStep() {
    if (currentStep < totalSteps && validateCurrentStep()) {
        currentStep++;
        updateStepProgress();
        scrollToTop();
    }
}

function previousStep() {
    if (currentStep > 1) {
        currentStep--;
        updateStepProgress();
        scrollToTop();
    }
}

function validateCurrentStep() {
    const currentStepFields = getCurrentStepFields();
    let isValid = true;
    
    currentStepFields.forEach(field => {
        const mockEvent = { target: field };
        if (!validateField(mockEvent)) {
            isValid = false;
        }
    });
    
    return isValid;
}

function getCurrentStepFields() {
    // Define which fields belong to each step
    const stepFields = {
        1: ['nome', 'cpf', 'data_nascimento', 'email', 'telefone', 'endereco'],
        2: ['curso', 'matricula', 'renda_familiar'],
        3: ['anexo_documentos', 'comprovante_renda', 'comprovante_residencia', 'historico_escolar']
    };
    
    const fieldNames = stepFields[currentStep] || [];
    return fieldNames.map(name => document.querySelector(`[name="${name}"]`)).filter(field => field);
}

function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Field validation functions
function validateField(event) {
    const field = event.target;
    const value = field.value.trim();
    const fieldType = field.type;
    const fieldName = field.name;
    
    clearValidation(event);
    
    // Required field validation
    if (field.required && !value) {
        showFieldError(field, 'Este campo é obrigatório.');
        return false;
    }
    
    // Specific validation by field type
    switch (fieldType) {
        case 'email':
            if (value && !isValidEmail(value)) {
                showFieldError(field, 'Digite um e-mail válido.');
                return false;
            }
            break;
            
        case 'date':
            if (value && !isValidAge(value)) {
                showFieldError(field, 'Você deve ter pelo menos 16 anos.');
                return false;
            }
            break;
            
        case 'number':
            if (fieldName === 'renda_familiar' && value && parseFloat(value) <= 0) {
                showFieldError(field, 'A renda deve ser maior que zero.');
                return false;
            }
            break;
            
        case 'file':
            if (field.files.length > 0) {
                const file = field.files[0];
                if (!isValidFileType(file, 'pdf')) {
                    showFieldError(field, 'Apenas arquivos PDF são aceitos.');
                    return false;
                }
                if (!isValidFileSize(file, 10)) {
                    showFieldError(field, 'O arquivo deve ter no máximo 10MB.');
                    return false;
                }
            }
            break;
    }
    
    // CPF validation
    if (fieldName === 'cpf' && value && !isValidCPF(value)) {
        showFieldError(field, 'Digite um CPF válido.');
        return false;
    }
    
    // Phone validation
    if (fieldName === 'telefone' && value && !isValidPhone(value)) {
        showFieldError(field, 'Digite um telefone válido.');
        return false;
    }
    
    // If we get here, field is valid
    showFieldSuccess(field);
    updateFormProgress();
    return true;
}

function clearValidation(event) {
    const field = event.target;
    field.classList.remove('is-invalid', 'is-valid');
    
    const feedback = field.parentNode.querySelector('.invalid-feedback');
    if (feedback) {
        feedback.remove();
    }
}

function showFieldError(field, message) {
    field.classList.add('is-invalid');
    field.classList.remove('is-valid');
    
    const feedback = document.createElement('div');
    feedback.className = 'invalid-feedback';
    feedback.textContent = message;
    field.parentNode.appendChild(feedback);
}

function showFieldSuccess(field) {
    field.classList.add('is-valid');
    field.classList.remove('is-invalid');
}

// Validation helper functions
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidAge(birthDate) {
    const today = new Date();
    const birth = new Date(birthDate);
    const age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
        return age - 1 >= 16;
    }
    return age >= 16;
}

function isValidCPF(cpf) {
    cpf = cpf.replace(/[^\d]/g, '');
    
    if (cpf.length !== 11) return false;
    if (/^(\d)\1{10}$/.test(cpf)) return false;
    
    let sum = 0;
    for (let i = 0; i < 9; i++) {
        sum += parseInt(cpf[i]) * (10 - i);
    }
    let digit1 = 11 - (sum % 11);
    if (digit1 > 9) digit1 = 0;
    
    sum = 0;
    for (let i = 0; i < 10; i++) {
        sum += parseInt(cpf[i]) * (11 - i);
    }
    let digit2 = 11 - (sum % 11);
    if (digit2 > 9) digit2 = 0;
    
    return digit1 === parseInt(cpf[9]) && digit2 === parseInt(cpf[10]);
}

function isValidPhone(phone) {
    phone = phone.replace(/[^\d]/g, '');
    return phone.length >= 10 && phone.length <= 11;
}

function isValidFileType(file, allowedType) {
    const fileType = file.type.toLowerCase();
    return fileType.includes(allowedType);
}

function isValidFileSize(file, maxSizeMB) {
    const maxSizeBytes = maxSizeMB * 1024 * 1024;
    return file.size <= maxSizeBytes;
}

// Formatting functions
function formatCPF(event) {
    let value = event.target.value.replace(/[^\d]/g, '');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    event.target.value = value;
}

function formatPhone(event) {
    let value = event.target.value.replace(/[^\d]/g, '');
    if (value.length <= 10) {
        value = value.replace(/(\d{2})(\d)/, '($1) $2');
        value = value.replace(/(\d{4})(\d)/, '$1-$2');
    } else {
        value = value.replace(/(\d{2})(\d)/, '($1) $2');
        value = value.replace(/(\d{5})(\d)/, '$1-$2');
    }
    event.target.value = value;
}

function formatCurrency(event) {
    let value = event.target.value.replace(/[^\d]/g, '');
    value = (value / 100).toFixed(2);
    value = value.replace('.', ',');
    value = value.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    event.target.value = 'R$ ' + value;
}

// File upload handling
function handleFileUpload(event) {
    const file = event.target.files[0];
    const field = event.target;
    
    if (file) {
        // Show upload progress
        const progressContainer = document.createElement('div');
        progressContainer.className = 'upload-progress mt-2';
        progressContainer.innerHTML = `
            <div class="progress">
                <div class="progress-bar" style="width: 0%"></div>
            </div>
            <small class="text-muted">Carregando: ${file.name}</small>
        `;
        
        field.parentNode.appendChild(progressContainer);
        
        // Simulate upload progress
        let progress = 0;
        const progressBar = progressContainer.querySelector('.progress-bar');
        const interval = setInterval(() => {
            progress += Math.random() * 30;
            if (progress >= 100) {
                progress = 100;
                clearInterval(interval);
                setTimeout(() => {
                    progressContainer.remove();
                    showUploadSuccess(field, file.name);
                }, 500);
            }
            progressBar.style.width = progress + '%';
        }, 200);
    }
}

function showUploadSuccess(field, fileName) {
    const successMsg = document.createElement('div');
    successMsg.className = 'upload-success mt-2 text-success';
    successMsg.innerHTML = `<i class="bi bi-check-circle-fill me-2"></i>Arquivo "${fileName}" carregado com sucesso!`;
    field.parentNode.appendChild(successMsg);
}

// Form progress tracking
function updateFormProgress() {
    const form = document.querySelector('form');
    if (!form) return;
    
    const requiredFields = form.querySelectorAll('[required]');
    const validFields = form.querySelectorAll('.is-valid');
    
    const progress = (validFields.length / requiredFields.length) * 100;
    
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        progressBar.style.width = progress + '%';
    }
}

// Form submission handling
function handleFormSubmission(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitButton = form.querySelector('.btn-primary');
    
    // Validate all fields
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    
    inputs.forEach(input => {
        const mockEvent = { target: input };
        if (!validateField(mockEvent)) {
            isValid = false;
        }
    });
    
    if (!isValid) {
        showErrorMessage('Por favor, corrija os erros no formulário antes de continuar.');
        return;
    }
    
    // Show loading state
    submitButton.classList.add('btn-loading');
    submitButton.disabled = true;
    
    // Simulate form submission
    setTimeout(() => {
        // Reset button
        submitButton.classList.remove('btn-loading');
        submitButton.disabled = false;
        
        // Show success message
        showSuccessMessage('Primeira inscrição enviada com sucesso! Você receberá uma confirmação por e-mail.');
        
        // Clear auto-saved data
        clearAutoSavedData();
        
        // Optional: redirect
        // window.location.href = '/aluno/editais';
    }, 3000);
}

// Message functions
function showSuccessMessage(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'success-message';
    alertDiv.innerHTML = `<i class="bi bi-check-circle-fill"></i>${message}`;
    
    const form = document.querySelector('.form-container');
    form.insertBefore(alertDiv, form.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

function showErrorMessage(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger';
    alertDiv.innerHTML = `<i class="bi bi-exclamation-triangle-fill me-2"></i>${message}`;
    
    const form = document.querySelector('.form-container');
    form.insertBefore(alertDiv, form.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Auto-save functionality
function autoSaveForm() {
    const form = document.querySelector('form');
    if (!form) return;
    
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        if (typeof value === 'string' && value.trim()) {
            data[key] = value;
        }
    }
    
    data.currentStep = currentStep;
    localStorage.setItem('primeira_inscricao_autosave', JSON.stringify(data));
}

function loadAutoSavedData() {
    const savedData = localStorage.getItem('primeira_inscricao_autosave');
    if (!savedData) return;
    
    try {
        const data = JSON.parse(savedData);
        const form = document.querySelector('form');
        
        Object.keys(data).forEach(key => {
            if (key === 'currentStep') {
                currentStep = data[key];
                updateStepProgress();
                return;
            }
            
            const field = form.querySelector(`[name="${key}"]`);
            if (field && field.type !== 'file') {
                field.value = data[key];
            }
        });
    } catch (e) {
        console.log('Erro ao carregar dados salvos:', e);
    }
}

function clearAutoSavedData() {
    localStorage.removeItem('primeira_inscricao_autosave');
}

// Auto-save every 30 seconds
setInterval(autoSaveForm, 30000);

// Load saved data when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadAutoSavedData();
});

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl+S to save form
    if (event.ctrlKey && event.key === 's') {
        event.preventDefault();
        autoSaveForm();
        
        const toast = document.createElement('div');
        toast.className = 'toast-message';
        toast.textContent = 'Formulário salvo automaticamente!';
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #4CAF50;
            color: white;
            padding: 1rem;
            border-radius: 8px;
            z-index: 9999;
        `;
        document.body.appendChild(toast);
        
        setTimeout(() => toast.remove(), 2000);
    }
});

// Income calculator helper
function calculateEligibility() {
    const incomeInput = document.getElementById('renda_familiar');
    if (!incomeInput || !incomeInput.value) return;
    
    const income = parseFloat(incomeInput.value.replace(/[^\d,]/g, '').replace(',', '.'));
    const minimumWage = 1320; // 2025 minimum wage in Brazil
    const maxIncome = minimumWage * 1.5;
    
    const resultDiv = document.createElement('div');
    resultDiv.className = 'eligibility-result mt-2';
    
    if (income <= maxIncome) {
        resultDiv.className += ' text-success';
        resultDiv.innerHTML = `<i class="bi bi-check-circle-fill me-2"></i>Renda dentro do limite permitido (até R$ ${maxIncome.toFixed(2)})`;
    } else {
        resultDiv.className += ' text-warning';
        resultDiv.innerHTML = `<i class="bi bi-exclamation-triangle-fill me-2"></i>Renda acima do limite (máximo R$ ${maxIncome.toFixed(2)})`;
    }
    
    // Remove previous result
    const existingResult = incomeInput.parentNode.querySelector('.eligibility-result');
    if (existingResult) {
        existingResult.remove();
    }
    
    incomeInput.parentNode.appendChild(resultDiv);
}

// Add income calculation to income field
document.addEventListener('DOMContentLoaded', function() {
    const incomeInput = document.getElementById('renda_familiar');
    if (incomeInput) {
        incomeInput.addEventListener('blur', calculateEligibility);
    }
});
