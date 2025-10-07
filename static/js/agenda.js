// Agenda - JavaScript

// Estado do calendário
let currentDate = new Date();
let selectedDate = new Date();

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    renderCalendar();
    updateSelectedDateDisplay();
    setupEventListeners();
});

// Renderizar calendário
function renderCalendar() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    
    // Atualizar título do mês
    const monthNames = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ];
    document.getElementById('currentMonth').textContent = `${monthNames[month]} ${year}`;
    
    // Primeiro dia do mês
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    
    // Dias do mês anterior para preencher
    const prevLastDay = new Date(year, month, 0);
    const firstDayWeek = firstDay.getDay();
    
    // Limpar calendário
    const calendarDays = document.getElementById('calendarDays');
    calendarDays.innerHTML = '';
    
    // Dias do mês anterior
    for (let i = firstDayWeek - 1; i >= 0; i--) {
        const day = prevLastDay.getDate() - i;
        const dayElement = createDayElement(day, 'other-month');
        calendarDays.appendChild(dayElement);
    }
    
    // Dias do mês atual
    for (let day = 1; day <= lastDay.getDate(); day++) {
        const dayElement = createDayElement(day, 'current-month');
        
        // Verificar se é hoje
        const today = new Date();
        if (day === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
            dayElement.classList.add('today');
        }
        
        // Verificar se é o dia selecionado
        if (day === selectedDate.getDate() && month === selectedDate.getMonth() && year === selectedDate.getFullYear()) {
            dayElement.classList.add('selected');
        }
        
        // Adicionar indicador de eventos (exemplo)
        if (hasEvents(day, month, year)) {
            dayElement.classList.add('has-event');
        }
        
        calendarDays.appendChild(dayElement);
    }
    
    // Dias do próximo mês para completar
    const totalCells = calendarDays.children.length;
    const remainingCells = 42 - totalCells; // 6 semanas x 7 dias
    
    for (let day = 1; day <= remainingCells; day++) {
        const dayElement = createDayElement(day, 'other-month');
        calendarDays.appendChild(dayElement);
    }
}

// Criar elemento de dia
function createDayElement(day, type) {
    const dayElement = document.createElement('div');
    dayElement.className = `calendar-day ${type}`;
    dayElement.textContent = day;
    
    if (type === 'current-month') {
        dayElement.addEventListener('click', function() {
            selectedDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), day);
            renderCalendar();
            updateSelectedDateDisplay();
            // Aqui você pode carregar eventos do dia selecionado
        });
    }
    
    return dayElement;
}

// Verificar se o dia tem eventos (exemplo com dados mock)
function hasEvents(day, month, year) {
    // Dados de exemplo - substitua com dados reais da API
    const eventsData = [
        { date: new Date(2025, 9, 7) },  // 7 de outubro
        { date: new Date(2025, 9, 8) },  // 8 de outubro
        { date: new Date(2025, 9, 10) }, // 10 de outubro
        { date: new Date(2025, 9, 12) }, // 12 de outubro
        { date: new Date(2025, 9, 15) }, // 15 de outubro
        { date: new Date(2025, 9, 18) }, // 18 de outubro
    ];
    
    return eventsData.some(event => 
        event.date.getDate() === day && 
        event.date.getMonth() === month && 
        event.date.getFullYear() === year
    );
}

// Atualizar exibição da data selecionada
function updateSelectedDateDisplay() {
    const monthNames = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ];
    
    const day = selectedDate.getDate();
    const month = monthNames[selectedDate.getMonth()];
    const year = selectedDate.getFullYear();
    
    document.getElementById('selectedDate').textContent = `${day} de ${month}, ${year}`;
}

// Configurar event listeners
function setupEventListeners() {
    // Navegação do calendário
    document.getElementById('prevMonth').addEventListener('click', function() {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar();
    });
    
    document.getElementById('nextMonth').addEventListener('click', function() {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar();
    });
    
    document.getElementById('hoje').addEventListener('click', function() {
        currentDate = new Date();
        selectedDate = new Date();
        renderCalendar();
        updateSelectedDateDisplay();
    });
    
    // Filtros
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            const filter = this.getAttribute('data-filter');
            filterEvents(filter);
        });
    });
}

// Filtrar eventos
function filterEvents(filter) {
    const eventos = document.querySelectorAll('.evento-item, .evento-resumo');
    
    eventos.forEach(evento => {
        if (filter === 'todos') {
            evento.style.display = 'flex';
        } else {
            if (evento.classList.contains(filter.replace('s', ''))) {
                evento.style.display = 'flex';
            } else {
                evento.style.display = 'none';
            }
        }
    });
}

// Função para formatar data
function formatDate(date) {
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${day}/${month}/${year}`;
}

// Função para formatar hora
function formatTime(date) {
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${hours}:${minutes}`;
}

// Adicionar evento ao clicar no botão do modal
document.addEventListener('DOMContentLoaded', function() {
    const modalElement = document.getElementById('novoEventoModal');
    if (modalElement) {
        modalElement.addEventListener('shown.bs.modal', function() {
            // Preencher data atual no formulário
            const dateInput = modalElement.querySelector('input[type="date"]');
            if (dateInput) {
                const today = new Date();
                const formattedDate = today.toISOString().split('T')[0];
                dateInput.value = formattedDate;
            }
        });
    }
});

// Exportar funções para uso global
window.AgendaCalendar = {
    renderCalendar,
    updateSelectedDateDisplay,
    filterEvents
};
