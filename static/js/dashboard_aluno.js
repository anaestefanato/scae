/* =========================
   DASHBOARD ALUNO - JAVASCRIPT
   ========================= */

// Menu toggle functionality - Igual ao dashboard assistente
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    const menuToggle = document.getElementById('menuToggle');
    const closeSidebar = document.getElementById('closeSidebar');
    
    // Criar backdrop igual ao assistente
    const sidebarBackdrop = document.createElement('div');
    sidebarBackdrop.className = 'sidebar-backdrop';
    document.body.appendChild(sidebarBackdrop);
    
    function closeSidebarFunction() {
        if (sidebar) {
            sidebar.classList.remove('open');
            sidebar.classList.add('collapsed');
        }
        if (mainContent) mainContent.classList.remove('shifted');
        if (menuToggle) menuToggle.classList.remove('hidden');
        if (sidebarBackdrop) sidebarBackdrop.classList.remove('visible');
        document.body.style.overflow = ''; // Permite scroll novamente
    }
    
    function openSidebarFunction() {
        if (sidebar) {
            sidebar.classList.add('open');
            sidebar.classList.remove('collapsed');
        }
        if (mainContent) mainContent.classList.add('shifted');
        if (menuToggle) menuToggle.classList.add('hidden');
        if (sidebarBackdrop) sidebarBackdrop.classList.add('visible');
        document.body.style.overflow = 'hidden'; // Impede scroll da página
    }
    
    // Close sidebar button
    if (closeSidebar) {
        closeSidebar.addEventListener('click', closeSidebarFunction);
    }
    
    // Open sidebar button
    if (menuToggle) {
        menuToggle.addEventListener('click', openSidebarFunction);
    }

    // Close sidebar when clicking on backdrop
    if (sidebarBackdrop) {
        sidebarBackdrop.addEventListener('click', closeSidebarFunction);
    }

    // Close sidebar when pressing ESC key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && sidebar && sidebar.classList.contains('open')) {
            closeSidebarFunction();
        }
    });
});

// Modal Confirmar Recebimento
if(document.getElementById('btnConfirmarRecebimento')){
    document.getElementById('btnConfirmarRecebimento').addEventListener('click', function() {
        document.getElementById('modalConfirmarRecebimento').style.display = 'block';
        document.getElementById('modalConfirmarRecebimento').classList.add('show');
    });
}
function fecharModalConfirmarRecebimento() {
    document.getElementById('modalConfirmarRecebimento').style.display = 'none';
    document.getElementById('modalConfirmarRecebimento').classList.remove('show');
}
function confirmarRecebimento() {
    fecharModalConfirmarRecebimento();
    var btn = document.getElementById('btnConfirmarRecebimento');
    btn.textContent = 'Recebimento Confirmado';
    btn.classList.remove('btn-outline-success');
    btn.classList.add('btn-success');
    btn.disabled = true;
}

// Modal Detalhes Auxílio
if(document.getElementById('btnDetalhesAuxilio')){
    document.getElementById('btnDetalhesAuxilio').addEventListener('click', function() {
        document.getElementById('modalDetalhesAuxilio').style.display = 'block';
        document.getElementById('modalDetalhesAuxilio').classList.add('show');
    });
}
function fecharModalDetalhesAuxilio() {
    document.getElementById('modalDetalhesAuxilio').style.display = 'none';
    document.getElementById('modalDetalhesAuxilio').classList.remove('show');
}

// Modal de acompanhamento de inscrição
if(document.getElementById('btnAcompanhar')){
    document.getElementById('btnAcompanhar').addEventListener('click', function() {
        document.getElementById('modalAcompanhar').style.display = 'block';
        document.getElementById('modalAcompanhar').classList.add('show');
    });
}
function fecharModalAcompanhar() {
    document.getElementById('modalAcompanhar').style.display = 'none';
    document.getElementById('modalAcompanhar').classList.remove('show');
}

// FullCalendar
window.addEventListener("DOMContentLoaded", function () {
    var calendarEl = document.getElementById("fc-calendar");
    if (calendarEl) {
        var calendar = new FullCalendar.Calendar(calendarEl, {
            themeSystem: "bootstrap5",
            initialView: "dayGridMonth",
            locale: "pt-br",
            events: [
                {
                    title: "Período de Inscrições - Auxílio Transporte",
                    start: "2025-04-10",
                    end: "2025-04-30",
                    backgroundColor: "#4CAF50",
                    borderColor: "#2E7D32"
                },
                {
                    title: "Resultado - Auxílio Moradia",
                    start: "2025-04-15",
                    backgroundColor: "#FF9800",
                    borderColor: "#F57C00"
                },
                {
                    title: "Entrevista Presencial",
                    start: "2025-04-18T14:00:00",
                    backgroundColor: "#2196F3",
                    borderColor: "#1976D2"
                }
            ],
            headerToolbar: {
                left: "prev,next today",
                center: "title",
                right: "dayGridMonth,timeGridWeek"
            },
            height: "auto",
            contentHeight: 300
        });
        calendar.render();
    }
});
