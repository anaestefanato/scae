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

// Modal detalhes
function mostrarDetalhes(mes, ano, auxilios) {
    const body = document.getElementById('detalhesRecebimentoBody');
    
    // Calcular valor total
    let valorTotal = 0;
    auxilios.forEach(aux => valorTotal += aux.valor);
    
    // Montar lista de auxílios
    let listaAuxilios = '<ul class="list-unstyled">';
    auxilios.forEach(function(auxilio) {
        let icone = '';
        let nome = '';
        
        if (auxilio.tipo_auxilio.includes('alimentacao')) {
            icone = '<i class="bi bi-cup-hot me-2 text-success"></i>';
            nome = 'Auxílio Alimentação';
        } else if (auxilio.tipo_auxilio.includes('transporte')) {
            icone = '<i class="bi bi-bus-front me-2 text-success"></i>';
            nome = 'Auxílio Transporte';
        } else if (auxilio.tipo_auxilio.includes('moradia')) {
            icone = '<i class="bi bi-house me-2 text-success"></i>';
            nome = 'Auxílio Moradia';
        } else if (auxilio.tipo_auxilio.includes('material')) {
            icone = '<i class="bi bi-book me-2 text-success"></i>';
            nome = 'Auxílio Material Didático';
        } else {
            icone = '<i class="bi bi-gift me-2 text-success"></i>';
            nome = auxilio.tipo_auxilio.replace('auxilio', 'Auxílio').replace(/_/g, ' ');
        }
        
        listaAuxilios += '<li class="mb-2">' + icone + nome + ' - <span class="text-success fw-bold">R$ ' + auxilio.valor.toFixed(2) + '</span></li>';
    });
    listaAuxilios += '</ul>';
    
    body.innerHTML = `
        <div class="row">
            <div class="col-12">
                <h6 class="mb-3">Informações do Pagamento</h6>
                <p><strong>Mês de Referência:</strong> ${mes}/${ano}</p>
                <p><strong>Valor Total:</strong> <span class='text-success fw-bold'>R$ ${valorTotal.toFixed(2)}</span></p>
                <p><strong>Status:</strong> <span class='status-badge status-deferido'>Confirmado</span></p>
            </div>
        </div>
        <div class="row mt-3">
            <div class="col-12">
                <h6 class="mb-3">Auxílios Recebidos</h6>
                ${listaAuxilios}
            </div>
        </div>
        <div class="row mt-3">
            <div class="col-12">
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
let mesAtual = null;
let anoAtual = null;
let auxiliosAtual = [];

function abrirModalConfirmacao(mes, ano, valorTotal, auxilios) {
    mesAtual = mes;
    anoAtual = ano;
    auxiliosAtual = auxilios;
    
    // Preencher detalhes
    document.getElementById('detalheMes').textContent = mes + '/' + ano;
    document.getElementById('detalheValor').textContent = 'R$ ' + valorTotal.toFixed(2);
    
    // Preencher lista de auxílios
    const listaAuxilios = document.getElementById('listaAuxilios');
    listaAuxilios.innerHTML = '';
    
    let temTransporte = false;
    let temMoradia = false;
    
    auxilios.forEach(function(auxilio) {
        const li = document.createElement('li');
        li.className = 'mb-2';
        
        let icone = '';
        let nome = '';
        
        if (auxilio.tipo_auxilio.includes('alimentacao')) {
            icone = '<i class="bi bi-cup-hot me-2 text-success"></i>';
            nome = 'Auxílio Alimentação';
        } else if (auxilio.tipo_auxilio.includes('transporte')) {
            icone = '<i class="bi bi-bus-front me-2 text-success"></i>';
            nome = 'Auxílio Transporte';
            temTransporte = true;
        } else if (auxilio.tipo_auxilio.includes('moradia')) {
            icone = '<i class="bi bi-house me-2 text-success"></i>';
            nome = 'Auxílio Moradia';
            temMoradia = true;
        } else if (auxilio.tipo_auxilio.includes('material')) {
            icone = '<i class="bi bi-book me-2 text-success"></i>';
            nome = 'Auxílio Material Didático';
        } else {
            icone = '<i class="bi bi-gift me-2 text-success"></i>';
            nome = auxilio.tipo_auxilio.replace('auxilio', 'Auxílio').replace(/_/g, ' ');
        }
        
        li.innerHTML = icone + nome + ' - <span class="text-success fw-bold">R$ ' + auxilio.valor.toFixed(2) + '</span>';
        listaAuxilios.appendChild(li);
    });
    
    // Definir ação do formulário
    document.getElementById('formConfirmacao').action = `/aluno/recebimentos/confirmar/${mes}/${ano}`;
    
    // Mostrar/ocultar campos de comprovante baseado nos tipos de auxílio
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
    if (temTransporte || temMoradia) {
        divComprovantes.style.display = 'block';
        
        if (temTransporte) {
            divTransporte.style.display = 'block';
            inputTransporte.required = true;
        }
        
        if (temMoradia) {
            divMoradia.style.display = 'block';
            inputMoradia.required = true;
        }
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
    mesAtual = null;
    anoAtual = null;
    auxiliosAtual = [];
}

function baixarComprovante() {
    // Simula o download do comprovante
    alert('Comprovante será baixado em instantes...');
}
