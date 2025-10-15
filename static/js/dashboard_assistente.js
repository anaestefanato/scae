/* =========================
   DASHBOARD ASSISTENTE SOCIAL - JAVASCRIPT
   ========================= */

// Menu toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    const menuToggle = document.getElementById('menuToggle');
    const closeSidebar = document.getElementById('closeSidebar');
    const sidebarBackdrop = document.createElement('div');
    sidebarBackdrop.className = 'sidebar-backdrop';
    document.body.appendChild(sidebarBackdrop);
    
    function closeSidebarFunction() {
        sidebar.classList.remove('open');
        mainContent.classList.remove('shifted');
        menuToggle.classList.remove('hidden');
        sidebarBackdrop.classList.remove('visible');
        document.body.style.overflow = '';
    }
    
    function openSidebarFunction() {
        sidebar.classList.add('open');
        mainContent.classList.add('shifted');
        menuToggle.classList.add('hidden');
        sidebarBackdrop.classList.add('visible');
        document.body.style.overflow = 'hidden';
    }
    
    // Close sidebar button
    closeSidebar.addEventListener('click', closeSidebarFunction);
    
    // Open sidebar button
    menuToggle.addEventListener('click', openSidebarFunction);

    // Close sidebar when clicking on backdrop
    sidebarBackdrop.addEventListener('click', closeSidebarFunction);

    // Close sidebar when pressing ESC key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && sidebar.classList.contains('open')) {
            closeSidebarFunction();
        }
    });

    // Nova Entrevista Modal functionality
    const agendarBtn = document.getElementById('agendarEntrevista');
    const novaEntrevistaForm = document.getElementById('novaEntrevistaForm');
    
    // Set minimum date to today
    const dataEntrevista = document.getElementById('dataEntrevista');
    if (dataEntrevista) {
        const today = new Date().toISOString().split('T')[0];
        dataEntrevista.setAttribute('min', today);
    }
    
    // Modalidade change handler
    const modalidadeSelect = document.getElementById('modalidade');
    const localInput = document.getElementById('local');
    
    if (modalidadeSelect && localInput) {
        modalidadeSelect.addEventListener('change', function() {
            if (this.value === 'online') {
                localInput.placeholder = 'Ex: https://meet.google.com/abc-defg-hij';
                localInput.value = '';
            } else if (this.value === 'presencial') {
                localInput.placeholder = 'Ex: Sala 201 - Bloco A';
                localInput.value = '';
            } else if (this.value === 'hibrido') {
                localInput.placeholder = 'Ex: Sala 201 + https://meet.google.com/...';
                localInput.value = '';
            }
        });
    }
    
    // Agendar entrevista
    agendarBtn.addEventListener('click', function() {
        const form = novaEntrevistaForm;
        const formData = new FormData(form);
        
        // Validation
        const alunoNome = document.getElementById('alunoNome');
        const tipoEntrevista = document.getElementById('tipoEntrevista');
        const dataEntrevista = document.getElementById('dataEntrevista');
        const horaEntrevista = document.getElementById('horaEntrevista');
        const modalidade = document.getElementById('modalidade');
        const prioridade = document.getElementById('prioridade');
        
        if (!alunoNome.value.trim() || !tipoEntrevista.value || !dataEntrevista.value || 
            !horaEntrevista.value || !modalidade.value || !prioridade.value) {
            alert('Por favor, preencha todos os campos obrigatórios.');
            return;
        }
        
        // Validate student name length
        if (alunoNome.value.trim().length < 3) {
            alert('Por favor, digite o nome completo do aluno (mínimo 3 caracteres).');
            alunoNome.focus();
            return;
        }
        
        // Validate date is not in the past
        const selectedDate = new Date(dataEntrevista.value + 'T' + horaEntrevista.value);
        const now = new Date();
        
        if (selectedDate <= now) {
            alert('A data e horário da entrevista devem ser futuros.');
            return;
        }
        
        // Simulate API call
        agendarBtn.innerHTML = '<i class="bi bi-hourglass-split me-1"></i>Agendando...';
        agendarBtn.disabled = true;
        
        setTimeout(function() {
            // Create new interview element
            const novaEntrevista = criarElementoEntrevista({
                nome: alunoNome.value.trim(),
                tipo: tipoEntrevista.options[tipoEntrevista.selectedIndex].text,
                data: dataEntrevista.value,
                hora: horaEntrevista.value,
                modalidade: modalidade.value,
                local: document.getElementById('local').value || 'A definir',
                prioridade: prioridade.value
            });
            
            // Add to interviews list
            const entrevistasContainer = document.querySelector('#entrevistasContainer');
            const novaEntrevistaBtn = document.querySelector('.d-flex.justify-content-end.mt-3');
            entrevistasContainer.insertBefore(novaEntrevista, novaEntrevistaBtn);
            
            // Success simulation
            alert('Entrevista agendada com sucesso para ' + alunoNome.value.trim() + '!');
            
            // Reset form
            form.reset();
            
            // Reset button
            agendarBtn.innerHTML = '<i class="bi bi-check-circle me-1"></i>Agendar Entrevista';
            agendarBtn.disabled = false;
            
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('novaEntrevistaModal'));
            modal.hide();
            
            // Optionally refresh the entrevistas list here
            // location.reload(); // uncomment to refresh page
            
        }, 1500);
    });
    
    // Reset form when modal is hidden
    document.getElementById('novaEntrevistaModal').addEventListener('hidden.bs.modal', function() {
        novaEntrevistaForm.reset();
        localInput.placeholder = 'Ex: Sala 201 - Bloco A';
    });

    // Document approval functionality
    const botoesAprovar = document.querySelectorAll('.btn-aprovar');
    botoesAprovar.forEach(botao => {
        botao.addEventListener('click', function() {
            const documentoId = this.getAttribute('data-documento');
            aprovarDocumento(this, documentoId);
        });
    });
});

// Function to create new interview element
function criarElementoEntrevista(dados) {
    const div = document.createElement('div');
    div.className = 'd-flex justify-content-between align-items-center mb-3 p-3 bg-light rounded nova-entrevista';
    
    // Format date
    const dataFormatada = formatarDataHora(dados.data, dados.hora);
    
    // Determine button style based on date
    const agora = new Date();
    const dataEntrevista = new Date(dados.data + 'T' + dados.hora);
    const isToday = dataEntrevista.toDateString() === agora.toDateString();
    const isFuture = dataEntrevista > agora;
    
    let buttonClass = 'btn-outline-secondary';
    let buttonText = 'Reagendar';
    
    if (isToday && isFuture) {
        buttonClass = 'btn-outline-primary';
        buttonText = 'Iniciar';
    } else if (isFuture) {
        buttonClass = 'btn-outline-secondary';
        buttonText = 'Reagendar';
    }
    
    // Determine icon based on modality
    let modalidadeIcon = 'bi-geo-alt';
    let modalidadeText = dados.modalidade;
    
    if (dados.modalidade === 'online') {
        modalidadeIcon = 'bi-camera-video';
        modalidadeText = 'Online';
    } else if (dados.modalidade === 'presencial') {
        modalidadeIcon = 'bi-geo-alt';
        modalidadeText = 'Presencial';
    } else if (dados.modalidade === 'hibrido') {
        modalidadeIcon = 'bi-hybrid';
        modalidadeText = 'Híbrido';
    }
    
    div.innerHTML = `
        <div>
            <h5 class="mb-0">${dados.nome}</h5>
            <small class="text-muted">${dados.tipo}</small>
            <br>
            <small class="text-info">
                <i class="${modalidadeIcon}"></i> ${modalidadeText}${dados.local ? ' - ' + dados.local : ''}
            </small>
        </div>
        <div class="text-end">
            <div class="fw-bold">${dataFormatada}</div>
            <span class="badge bg-${getPrioridadeCor(dados.prioridade)} mb-2">${capitalizarPrioridade(dados.prioridade)}</span>
            <br>
            <button class="btn btn-sm ${buttonClass} mt-1">${buttonText}</button>
        </div>
    `;
    
    // Add animation
    div.style.opacity = '0';
    div.style.transform = 'translateY(-10px)';
    
    setTimeout(() => {
        div.style.transition = 'all 0.3s ease';
        div.style.opacity = '1';
        div.style.transform = 'translateY(0)';
    }, 100);
    
    return div;
}

// Function to format date and time
function formatarDataHora(data, hora) {
    const dataObj = new Date(data + 'T' + hora);
    const agora = new Date();
    
    const options = { 
        weekday: 'long', 
        day: '2-digit', 
        month: '2-digit',
        hour: '2-digit', 
        minute: '2-digit' 
    };
    
    if (dataObj.toDateString() === agora.toDateString()) {
        return `Hoje, ${hora}`;
    } else {
        const amanha = new Date(agora);
        amanha.setDate(amanha.getDate() + 1);
        
        if (dataObj.toDateString() === amanha.toDateString()) {
            return `Amanhã, ${hora}`;
        } else {
            return dataObj.toLocaleDateString('pt-BR', { 
                day: '2-digit', 
                month: '2-digit',
                year: dataObj.getFullYear() !== agora.getFullYear() ? 'numeric' : undefined
            }) + `, ${hora}`;
        }
    }
}

// Function to get priority color
function getPrioridadeCor(prioridade) {
    switch(prioridade.toLowerCase()) {
        case 'baixa':
            return 'success';
        case 'media':
        case 'média':
            return 'warning';
        case 'alta':
            return 'danger';
        case 'urgente':
            return 'dark';
        default:
            return 'secondary';
    }
}

// Function to capitalize priority
function capitalizarPrioridade(prioridade) {
    return prioridade.charAt(0).toUpperCase() + prioridade.slice(1);
}

// Function to approve document
function aprovarDocumento(botao, documentoId) {
    // Change button to loading state
    const textoOriginal = botao.innerHTML;
    botao.innerHTML = '<i class="bi bi-hourglass-split"></i> Aprovando...';
    botao.disabled = true;
    
    // Simulate API call
    setTimeout(() => {
        // Change to approved state - only icon
        botao.innerHTML = '<i class="bi bi-check-circle-fill text-success"></i>';
        botao.className = 'btn btn-sm btn-outline-success disabled';
        botao.disabled = true;
        botao.style.border = 'none';
        botao.style.backgroundColor = 'transparent';
        
        // Add visual feedback to the document row
        const documentRow = botao.closest('.d-flex');
        documentRow.style.backgroundColor = '#d4edda';
        documentRow.style.border = '1px solid #c3e6cb';
        documentRow.style.borderRadius = '5px';
        documentRow.style.transition = 'all 0.3s ease';
        
        // Add approved badge to document name - only text
        const documentInfo = documentRow.querySelector('small');
        if (!documentInfo.querySelector('.badge-aprovado')) {
            const badge = document.createElement('span');
            badge.className = 'badge bg-success ms-2 badge-aprovado';
            badge.innerHTML = 'Aprovado';
            documentInfo.appendChild(badge);
        }
        
        // Optional: Show success message
        // alert('Documento aprovado com sucesso!');
        
    }, 1500);
}

// ===== MINI CALENDÁRIO =====
function initMiniCalendar() {
    const miniCalendarDays = document.getElementById('miniCalendarDays');
    if (!miniCalendarDays) return;

    const currentDate = new Date();
    const currentMonth = currentDate.getMonth();
    const currentYear = currentDate.getFullYear();
    const today = currentDate.getDate();
    
    // Update month label
    const monthNames = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
                       'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
    const miniCurrentMonth = document.getElementById('miniCurrentMonth');
    if (miniCurrentMonth) {
        miniCurrentMonth.textContent = `${monthNames[currentMonth]} ${currentYear}`;
    }
    
    // Get first day of month and number of days
    const firstDay = new Date(currentYear, currentMonth, 1).getDay();
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
    const daysInPrevMonth = new Date(currentYear, currentMonth, 0).getDate();
    
    miniCalendarDays.innerHTML = '';
    
    // Days with events (example - você pode substituir por dados reais)
    const eventsOnDays = [8, 10, 12, 15]; // Dias com eventos
    
    // Add previous month's trailing days
    for (let i = firstDay - 1; i >= 0; i--) {
        const day = daysInPrevMonth - i;
        const dayDiv = document.createElement('div');
        dayDiv.className = 'mini-calendar-day other-month';
        dayDiv.textContent = day;
        miniCalendarDays.appendChild(dayDiv);
    }
    
    // Add current month's days
    for (let day = 1; day <= daysInMonth; day++) {
        const dayDiv = document.createElement('div');
        dayDiv.className = 'mini-calendar-day';
        dayDiv.textContent = day;
        
        if (day === today) {
            dayDiv.classList.add('today');
        }
        
        if (eventsOnDays.includes(day)) {
            dayDiv.classList.add('has-event');
        }
        
        miniCalendarDays.appendChild(dayDiv);
    }
    
    // Add next month's leading days to complete the grid
    const totalCells = miniCalendarDays.children.length;
    const remainingCells = 42 - totalCells; // 6 weeks * 7 days = 42
    
    for (let day = 1; day <= remainingCells; day++) {
        const dayDiv = document.createElement('div');
        dayDiv.className = 'mini-calendar-day other-month';
        dayDiv.textContent = day;
        miniCalendarDays.appendChild(dayDiv);
    }
}

// Initialize mini calendar when page loads
document.addEventListener('DOMContentLoaded', initMiniCalendar);

