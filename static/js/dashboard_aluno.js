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
            headerToolbar: {
                left: "prev,next today",
                center: "title",
                right: "",
            },
            buttonText: {
                today: "Hoje",
            },
            events: [
                {
                    title: "Início das inscrições para Auxílio Material Didático",
                    start: "2025-04-20",
                },
                {
                    title: "Resultado da análise do Auxílio Transporte",
                    start: "2025-04-30",
                },
                {
                    title: "Fim das inscrições para Auxílio Material Didático",
                    start: "2025-05-05",
                },
                {
                    title: "Prazo para confirmação de recebimento do Auxílio Alimentação",
                    start: "2025-05-10",
                },
            ],
        });
        calendar.render();
    }
});
