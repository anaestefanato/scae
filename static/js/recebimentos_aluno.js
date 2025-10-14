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
function mostrarDetalhes(idRecebimento) {
    var body = document.getElementById('detalhesRecebimentoBody');
    body.innerHTML = `
        <div class="row">
            <div class="col-12">
                <h6 class="mb-3">Informações do Pagamento</h6>
                <p><strong>ID do Recebimento:</strong> ${idRecebimento}</p>
                <p><strong>Status:</strong> <span class='status-badge status-deferido'>Confirmado</span></p>
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

// Modal de confirmação
let idRecebimentoAtual = null;
let tipoAuxilioAtual = null;

function abrirModalConfirmacao(idRecebimento, tipoAuxilio, mes, valor) {
    idRecebimentoAtual = idRecebimento;
    tipoAuxilioAtual = tipoAuxilio;
    
    // Preencher detalhes
    document.getElementById('detalheAuxilio').textContent = formatarTipoAuxilio(tipoAuxilio);
    document.getElementById('detalheMes').textContent = mes;
    document.getElementById('detalheValor').textContent = 'R$ ' + valor.toFixed(2);
    
    // Definir ação do formulário
    document.getElementById('formConfirmacao').action = `/aluno/recebimentos/confirmar/${idRecebimento}`;
    
    // Mostrar/ocultar campos de comprovante baseado no tipo de auxílio
    const divComprovantes = document.getElementById('divComprovantes');
    const divTransporte = document.getElementById('divComprovanteTransporte');
    const divMoradia = document.getElementById('divComprovanteMoradia');
    const inputTransporte = document.getElementById('comprovante_transporte');
    const inputMoradia = document.getElementById('comprovante_moradia');
    
    // Resetar campos
    divTransporte.style.display = 'none';
    divMoradia.style.display = 'none';
    inputTransporte.required = false;
    inputMoradia.required = false;
    inputTransporte.value = '';
    inputMoradia.value = '';
    
    // Mostrar campos necessários
    if (tipoAuxilio.includes('transporte')) {
        divComprovantes.style.display = 'block';
        divTransporte.style.display = 'block';
        inputTransporte.required = true;
    } else if (tipoAuxilio.includes('moradia')) {
        divComprovantes.style.display = 'block';
        divMoradia.style.display = 'block';
        inputMoradia.required = true;
    } else {
        divComprovantes.style.display = 'none';
    }
    
    // Mostrar modal
    document.getElementById('modalConfirmacao').style.display = 'block';
    document.getElementById('modalConfirmacao').classList.add('show');
}

function fecharModalConfirmacao() {
    document.getElementById('modalConfirmacao').style.display = 'none';
    document.getElementById('modalConfirmacao').classList.remove('show');
    idRecebimentoAtual = null;
    tipoAuxilioAtual = null;
}

function formatarTipoAuxilio(tipo) {
    if (tipo.includes('alimentacao')) return 'Auxílio Alimentação';
    if (tipo.includes('transporte')) return 'Auxílio Transporte';
    if (tipo.includes('moradia')) return 'Auxílio Moradia';
    if (tipo.includes('material')) return 'Auxílio Material Didático';
    return tipo.replace('auxilio', 'Auxílio').replace(/_/g, ' ');
}

function baixarComprovante() {
    // Simula o download do comprovante
    alert('Comprovante será baixado em instantes...');
}
