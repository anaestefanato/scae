document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('fc-calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
    themeSystem: 'bootstrap5',
    initialView: 'dayGridMonth',
    locale: 'pt-br',
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: ''
    },
    buttonText: {
      today: 'Hoje'
    },
    events: [
      {
        title: 'Início das inscrições para Auxílio Material Didático',
        start: '2025-04-20'
      },
      {
        title: 'Resultado da análise do Auxílio Transporte',
        start: '2025-04-30'
      },
      {
        title: 'Fim das inscrições para Auxílio Material Didático',
        start: '2025-05-05'
      },
      {
        title: 'Prazo para confirmação de recebimento do Auxílio Alimentação',
        start: '2025-05-10'
      }
    ]
  });

  calendar.render();
});

