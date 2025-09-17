/* =========================
   RECEBIMENTOS ALUNO - JAVASCRIPT
   ========================= */

// Menu toggle functionality - Igual ao dashboard
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    const menuToggle = document.getElementById('menuToggle');
    const closeSidebar = document.getElementById('closeSidebar');
    
    // Criar backdrop igual ao dashboard
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

    // Close sidebar on ESC key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar && sidebar.classList.contains('open')) {
            closeSidebarFunction();
        }
    });

    // Função para garantir que a sidebar esteja sempre fechada ao carregar
    function initializeSidebar() {
        if (sidebar) {
            sidebar.classList.remove('open');
            sidebar.classList.add('collapsed');
        }
        if (mainContent) mainContent.classList.remove('shifted');
        if (menuToggle) menuToggle.classList.remove('hidden');
        if (sidebarBackdrop) sidebarBackdrop.classList.remove('visible');
    }

    // Inicializar sidebar fechada
    initializeSidebar();
});

// Filtro de auxílio
function filtrarAuxilio(tipo) {
    var linhas = document.querySelectorAll('#tabelaRecebimentos tbody tr');
    linhas.forEach(function(linha) {
        if (tipo === 'todos' || linha.getAttribute('data-auxilio') === tipo) {
            linha.style.display = '';
        } else {
            linha.style.display = 'none';
        }
    });
}

// Modal detalhes
function mostrarDetalhes(auxilio, mes, valor, data) {
    var body = document.getElementById('detalhesRecebimentoBody');
    body.innerHTML = `
        <div class="row">
            <div class="col-md-6">
                <h6 class="mb-3">Informações do Pagamento</h6>
                <p><strong>Tipo de Auxílio:</strong> ${auxilio}</p>
                <p><strong>Mês de Referência:</strong> ${mes}</p>
                <p><strong>Valor Recebido:</strong> <span class="text-success fw-bold">${valor}</span></p>
                <p><strong>Data do Recebimento:</strong> ${data}</p>
                <p><strong>Status:</strong> <span class='status-badge status-deferido'>Confirmado</span></p>
            </div>
            <div class="col-md-6">
                <h6 class="mb-3">Dados Bancários</h6>
                <p><strong>Banco:</strong> Banco do Brasil</p>
                <p><strong>Agência:</strong> 1234-5</p>
                <p><strong>Conta:</strong> 12345-6</p>
                <p><strong>Forma de Pagamento:</strong> Transferência Eletrônica</p>
                <p><strong>Comprovante:</strong> Disponível para download</p>
            </div>
        </div>
        <div class="row mt-3">
            <div class="col-12">
                <h6 class="mb-3">Observações</h6>
                <div class="alert alert-success">
                    <i class="bi bi-check-circle me-2"></i>
                    Recebimento processado com sucesso. Para dúvidas sobre valores ou datas, entre em contato com a assistência social.
                </div>
            </div>
        </div>
    `;
    document.getElementById('modalDetalhesRecebimento').style.display = 'block';
    document.getElementById('modalDetalhesRecebimento').classList.add('show');
}

function fecharModalDetalhesRecebimento() {
    document.getElementById('modalDetalhesRecebimento').style.display = 'none';
    document.getElementById('modalDetalhesRecebimento').classList.remove('show');
}

function baixarComprovante() {
    // Simula o download do comprovante
    alert('Comprovante será baixado em instantes...');
}
