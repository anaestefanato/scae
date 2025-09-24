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
function confirmarRecebimento(idAuxilio) {
    // Aqui você pode implementar a lógica para confirmar o recebimento
    // Por enquanto, apenas simula a confirmação
    console.log('Confirmando recebimento do auxílio ID:', idAuxilio);
    
    // Exibir modal de confirmação (exemplo)
    if(confirm('Tem certeza que deseja confirmar o recebimento deste auxílio?')) {
        // Aqui você faria uma requisição AJAX para o backend
        alert('Recebimento confirmado com sucesso!');
        
        // Desabilitar o botão após confirmação
        const btn = event.target.closest('button');
        if(btn) {
            btn.textContent = 'Recebimento Confirmado';
            btn.classList.remove('btn-outline-success');
            btn.classList.add('btn-success');
            btn.disabled = true;
        }
    }
}

// Modal Detalhes Auxílio
function verDetalhes(idAuxilio) {
    console.log('Visualizando detalhes do auxílio ID:', idAuxilio);
    
    // Buscar dados do auxílio e popular o modal
    // Por enquanto, vamos buscar do DOM os dados do auxílio
    const auxilioCards = document.querySelectorAll('.card');
    let auxilioData = null;
    
    auxilioCards.forEach(card => {
        const button = card.querySelector(`button[onclick*="${idAuxilio}"]`);
        if (button) {
            const cardBody = card.querySelector('.card-body');
            if (cardBody) {
                const edital = cardBody.querySelector('p:nth-child(1) strong').nextSibling.textContent.trim();
                const valor = cardBody.querySelector('p:nth-child(2)').textContent.match(/R\$ ([\d,\.]+)/)?.[1] || '0,00';
                const dataInicio = cardBody.querySelector('p:nth-child(4)').textContent.split(':')[1]?.trim() || '-';
                const tipoAuxilio = card.querySelector('.card-header span').textContent.trim();
                const status = card.querySelector('.status-badge').textContent.trim();
                
                auxilioData = { edital, valor, dataInicio, tipoAuxilio, status };
            }
        }
    });
    
    if (auxilioData) {
        // Popular o modal com os dados encontrados
        document.getElementById('detalheEdital').textContent = auxilioData.edital;
        document.getElementById('detalheValor').textContent = auxilioData.valor;
        document.getElementById('detalheDataAprovacao').textContent = auxilioData.dataInicio;
        document.getElementById('detalheVigencia').textContent = auxilioData.dataInicio + ' a ' + (auxilioData.dataFim || 'indefinido');
        document.getElementById('detalheTipo').textContent = auxilioData.tipoAuxilio;
        document.getElementById('modalTituloDetalhes').textContent = 'Detalhes do ' + auxilioData.tipoAuxilio;
        
        const statusElement = document.getElementById('detalheStatus');
        statusElement.textContent = auxilioData.status;
        statusElement.className = 'status-badge status-' + auxilioData.status.toLowerCase();
        
        // Abrir o modal
        const modal = document.getElementById('modalDetalhesAuxilio');
        if (modal) {
            modal.style.display = 'block';
            modal.classList.add('show');
        }
    } else {
        alert('Não foi possível carregar os detalhes do auxílio.');
    }
}

// Modal de acompanhamento de inscrição - Removido, agora redireciona para página dedicada

// Remover as funções antigas que não são mais necessárias
function fecharModalAcompanhar() {
    // Função removida - modal não existe mais
}

// Manter as funções antigas para compatibilidade com elementos estáticos
if(document.getElementById('btnConfirmarRecebimento')){
    document.getElementById('btnConfirmarRecebimento').addEventListener('click', function() {
        document.getElementById('modalConfirmarRecebimento').style.display = 'block';
        document.getElementById('modalConfirmarRecebimento').classList.add('show');
    });
}
function fecharModalConfirmarRecebimento() {
    const modal = document.getElementById('modalConfirmarRecebimento');
    if(modal) {
        modal.style.display = 'none';
        modal.classList.remove('show');
    }
}
function confirmarRecebimentoModal() {
    fecharModalConfirmarRecebimento();
    var btn = document.getElementById('btnConfirmarRecebimento');
    if(btn) {
        btn.textContent = 'Recebimento Confirmado';
        btn.classList.remove('btn-outline-success');
        btn.classList.add('btn-success');
        btn.disabled = true;
    }
}

// Modal Detalhes Auxílio  
function fecharModalDetalhesAuxilio() {
    const modal = document.getElementById('modalDetalhesAuxilio');
    if(modal) {
        modal.style.display = 'none';
        modal.classList.remove('show');
    }
}

// Remover eventos antigos que não são mais necessários
// Modal de acompanhamento removido - agora usa página dedicada

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
