/* =========================
   ANÁLISE DE INSCRIÇÕES - JAVASCRIPT
   ========================= */

document.addEventListener('DOMContentLoaded', function() {
    // Inicialização
    initializeAnaliseInscricoes();
});

function initializeAnaliseInscricoes() {
    // Event listeners para filtros
    setupFilters();
    
    // Event listeners para ações em lote
    setupBatchActions();
    
    // Event listeners para checkboxes
    setupCheckboxes();
    
    // Event listeners para modais
    setupModals();
    
    // Inicializar tooltips
    initializeTooltips();
}

// ===== FILTROS =====
function setupFilters() {
    const filtroEdital = document.getElementById('filtroEdital');
    const filtroStatus = document.getElementById('filtroStatus');
    const filtroPrioridade = document.getElementById('filtroPrioridade');
    const buscarAluno = document.getElementById('buscarAluno');
    const limparFiltros = document.getElementById('limparFiltros');

    if (filtroEdital) {
        filtroEdital.addEventListener('change', aplicarFiltros);
    }
    
    if (filtroStatus) {
        filtroStatus.addEventListener('change', aplicarFiltros);
    }
    
    if (filtroPrioridade) {
        filtroPrioridade.addEventListener('change', aplicarFiltros);
    }
    
    if (buscarAluno) {
        let searchTimeout;
        buscarAluno.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(aplicarFiltros, 300);
        });
    }
    
    if (limparFiltros) {
        limparFiltros.addEventListener('click', function() {
            document.getElementById('filtroEdital').value = '';
            document.getElementById('filtroStatus').value = '';
            document.getElementById('filtroPrioridade').value = '';
            document.getElementById('buscarAluno').value = '';
            aplicarFiltros();
        });
    }
}

function aplicarFiltros() {
    const edital = document.getElementById('filtroEdital').value;
    const status = document.getElementById('filtroStatus').value;
    const prioridade = document.getElementById('filtroPrioridade').value;
    const busca = document.getElementById('buscarAluno').value.toLowerCase();
    
    const linhas = document.querySelectorAll('#tabelaInscricoes tr');
    let inscricoesVisiveis = 0;
    
    linhas.forEach(linha => {
        let mostrar = true;
        
        // Filtro por edital
        if (edital && !linha.querySelector('.edital-badge').textContent.includes(edital)) {
            mostrar = false;
        }
        
        // Filtro por status
        if (status) {
            const statusElemento = linha.querySelector('.status-badge');
            if (!statusElemento.classList.contains(`status-${status}`)) {
                mostrar = false;
            }
        }
        
        // Filtro por prioridade
        if (prioridade) {
            const prioridadeElemento = linha.querySelector('.priority-high, .priority-medium, .priority-low');
            if (!prioridadeElemento.classList.contains(`priority-${prioridade}`)) {
                mostrar = false;
            }
        }
        
        // Filtro por busca de nome
        if (busca) {
            const nomeAluno = linha.querySelector('.aluno-nome').textContent.toLowerCase();
            if (!nomeAluno.includes(busca)) {
                mostrar = false;
            }
        }
        
        linha.style.display = mostrar ? '' : 'none';
        if (mostrar) inscricoesVisiveis++;
    });
    
    // Atualizar contador
    atualizarContador(inscricoesVisiveis);
}

function atualizarContador(visiveis) {
    const contador = document.querySelector('.card-footer .text-muted');
    if (contador) {
        const total = document.querySelectorAll('#tabelaInscricoes tr').length;
        contador.textContent = `Mostrando ${visiveis} de ${total} inscrições`;
    }
}

// ===== AÇÕES EM LOTE =====
function setupBatchActions() {
    const executarAcaoLote = document.getElementById('executarAcaoLote');
    
    if (executarAcaoLote) {
        executarAcaoLote.addEventListener('click', function() {
            const acao = document.getElementById('acaoLote').value;
            const selecionados = getInscricoesSelecionadas();
            
            if (!acao) {
                showAlert('Selecione uma ação para executar.', 'warning');
                return;
            }
            
            if (selecionados.length === 0) {
                showAlert('Selecione pelo menos uma inscrição.', 'warning');
                return;
            }
            
            executarAcaoEmLote(acao, selecionados);
        });
    }
}

function getInscricoesSelecionadas() {
    const checkboxes = document.querySelectorAll('.inscricao-checkbox:checked');
    return Array.from(checkboxes).map(cb => cb.value);
}

function executarAcaoEmLote(acao, inscricoes) {
    const confirmacao = confirm(`Tem certeza que deseja ${acao} ${inscricoes.length} inscrição(ões)?`);
    
    if (!confirmacao) return;
    
    // Mostrar loading
    const btn = document.getElementById('executarAcaoLote');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<span class="loading-spinner"></span> Processando...';
    btn.disabled = true;
    
    // Simular processamento (substituir por chamada real à API)
    setTimeout(() => {
        switch(acao) {
            case 'deferir':
                inscricoes.forEach(id => atualizarStatusInscricao(id, 'deferido'));
                showAlert(`${inscricoes.length} inscrição(ões) deferida(s) com sucesso!`, 'success');
                break;
            case 'indeferir':
                inscricoes.forEach(id => atualizarStatusInscricao(id, 'indeferido'));
                showAlert(`${inscricoes.length} inscrição(ões) indeferida(s) com sucesso!`, 'success');
                break;
            case 'agendar':
                showAlert(`Entrevistas agendadas para ${inscricoes.length} inscrição(ões)!`, 'info');
                break;
        }
        
        // Limpar seleções
        document.querySelectorAll('.inscricao-checkbox:checked').forEach(cb => cb.checked = false);
        document.getElementById('selecionarTodos').checked = false;
        document.getElementById('acaoLote').value = '';
        
        // Restaurar botão
        btn.innerHTML = originalText;
        btn.disabled = false;
    }, 2000);
}

// ===== CHECKBOXES =====
function setupCheckboxes() {
    const selecionarTodos = document.getElementById('selecionarTodos');
    
    if (selecionarTodos) {
        selecionarTodos.addEventListener('change', function() {
            const checkboxes = document.querySelectorAll('.inscricao-checkbox');
            checkboxes.forEach(cb => {
                if (cb.closest('tr').style.display !== 'none') {
                    cb.checked = this.checked;
                }
            });
        });
    }
    
    // Event listener para checkboxes individuais
    document.addEventListener('change', function(e) {
        if (e.target.classList.contains('inscricao-checkbox')) {
            atualizarSelecionarTodos();
        }
    });
}

function atualizarSelecionarTodos() {
    const checkboxes = document.querySelectorAll('.inscricao-checkbox');
    const checkboxesVisiveis = Array.from(checkboxes).filter(cb => cb.closest('tr').style.display !== 'none');
    const selecionados = checkboxesVisiveis.filter(cb => cb.checked);
    
    const selecionarTodos = document.getElementById('selecionarTodos');
    if (selecionarTodos) {
        selecionarTodos.checked = checkboxesVisiveis.length > 0 && selecionados.length === checkboxesVisiveis.length;
        selecionarTodos.indeterminate = selecionados.length > 0 && selecionados.length < checkboxesVisiveis.length;
    }
}

// ===== MODAIS =====
function setupModals() {
    // Modal de filtros avançados
    const aplicarFiltrosAvancados = document.getElementById('aplicarFiltrosAvancados');
    const limparFiltrosAvancados = document.getElementById('limparFiltrosAvancados');
    
    if (aplicarFiltrosAvancados) {
        aplicarFiltrosAvancados.addEventListener('click', function() {
            aplicarFiltrosAvancados();
            bootstrap.Modal.getInstance(document.getElementById('filtrosModal')).hide();
        });
    }
    
    if (limparFiltrosAvancados) {
        limparFiltrosAvancados.addEventListener('click', function() {
            document.getElementById('filtrosAvancadosForm').reset();
        });
    }
}

// ===== AÇÕES ESPECÍFICAS =====
function visualizarDetalhes(inscricaoId) {
    // Carregar dados da inscrição
    carregarDetalhesInscricao(inscricaoId);
    
    // Mostrar modal
    const modal = new bootstrap.Modal(document.getElementById('detalhesModal'));
    modal.show();
}

function carregarDetalhesInscricao(inscricaoId) {
    const detalhesConteudo = document.getElementById('detalhesConteudo');
    
    // Simular carregamento de dados (substituir por chamada real à API)
    const dadosSimulados = {
        1: {
            nome: 'João Silva dos Santos',
            matricula: '20251234567',
            curso: 'Técnico em Informática',
            periodo: '3º período',
            email: 'joao.silva@ifes.edu.br',
            telefone: '(27) 99999-9999',
            edital: '001/2025 - Auxílio Transporte',
            dataInscricao: '15/03/2025',
            status: 'Pendente',
            prioridade: 'Alta',
            rendaPerCapita: 'R$ 256,80',
            composicaoFamiliar: '4 pessoas',
            documentos: [
                'Comprovante de renda familiar ✓',
                'Comprovante de residência ✓', 
                'Declaração de matrícula ✓',
                'RG e CPF ✓'
            ],
            observacoes: 'Aluno em situação de vulnerabilidade social. Reside em área rural e necessita do auxílio transporte para frequentar as aulas.'
        }
        // Adicionar mais dados conforme necessário
    };
    
    const dados = dadosSimulados[inscricaoId] || dadosSimulados[1];
    
    detalhesConteudo.innerHTML = `
        <div class="row">
            <div class="col-md-6">
                <div class="detalhe-secao">
                    <h6><i class="bi bi-person me-2"></i>Dados Pessoais</h6>
                    <div class="detalhe-item">
                        <span class="detalhe-label">Nome:</span>
                        <span class="detalhe-valor">${dados.nome}</span>
                    </div>
                    <div class="detalhe-item">
                        <span class="detalhe-label">Matrícula:</span>
                        <span class="detalhe-valor">${dados.matricula}</span>
                    </div>
                    <div class="detalhe-item">
                        <span class="detalhe-label">Curso:</span>
                        <span class="detalhe-valor">${dados.curso}</span>
                    </div>
                    <div class="detalhe-item">
                        <span class="detalhe-label">Período:</span>
                        <span class="detalhe-valor">${dados.periodo}</span>
                    </div>
                    <div class="detalhe-item">
                        <span class="detalhe-label">Email:</span>
                        <span class="detalhe-valor">${dados.email}</span>
                    </div>
                    <div class="detalhe-item">
                        <span class="detalhe-label">Telefone:</span>
                        <span class="detalhe-valor">${dados.telefone}</span>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="detalhe-secao">
                    <h6><i class="bi bi-clipboard-check me-2"></i>Dados da Inscrição</h6>
                    <div class="detalhe-item">
                        <span class="detalhe-label">Edital:</span>
                        <span class="detalhe-valor">${dados.edital}</span>
                    </div>
                    <div class="detalhe-item">
                        <span class="detalhe-label">Data da Inscrição:</span>
                        <span class="detalhe-valor">${dados.dataInscricao}</span>
                    </div>
                    <div class="detalhe-item">
                        <span class="detalhe-label">Status:</span>
                        <span class="detalhe-valor">${dados.status}</span>
                    </div>
                    <div class="detalhe-item">
                        <span class="detalhe-label">Prioridade:</span>
                        <span class="detalhe-valor">${dados.prioridade}</span>
                    </div>
                    <div class="detalhe-item">
                        <span class="detalhe-label">Renda Per Capita:</span>
                        <span class="detalhe-valor">${dados.rendaPerCapita}</span>
                    </div>
                    <div class="detalhe-item">
                        <span class="detalhe-label">Composição Familiar:</span>
                        <span class="detalhe-valor">${dados.composicaoFamiliar}</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-6">
                <div class="detalhe-secao">
                    <h6><i class="bi bi-file-earmark-text me-2"></i>Documentos Anexados</h6>
                    ${dados.documentos.map(doc => `<div class="detalhe-item"><span class="detalhe-valor">${doc}</span></div>`).join('')}
                </div>
            </div>
            <div class="col-md-6">
                <div class="detalhe-secao">
                    <h6><i class="bi bi-chat-text me-2"></i>Observações</h6>
                    <p>${dados.observacoes}</p>
                </div>
            </div>
        </div>
    `;
}

function deferirInscricao(inscricaoId) {
    if (confirm('Tem certeza que deseja deferir esta inscrição?')) {
        atualizarStatusInscricao(inscricaoId, 'deferido');
        showAlert('Inscrição deferida com sucesso!', 'success');
    }
}

function indeferirInscricao(inscricaoId) {
    const motivo = prompt('Digite o motivo do indeferimento:');
    if (motivo) {
        atualizarStatusInscricao(inscricaoId, 'indeferido');
        showAlert('Inscrição indeferida com sucesso!', 'success');
    }
}

function agendarEntrevista(inscricaoId) {
    // Implementar lógica para agendar entrevista
    showAlert('Funcionalidade de agendamento será implementada em breve.', 'info');
}

function reagendarEntrevista(inscricaoId) {
    // Implementar lógica para reagendar entrevista
    showAlert('Funcionalidade de reagendamento será implementada em breve.', 'info');
}

function verJustificativa(inscricaoId) {
    // Implementar lógica para ver justificativa
    showAlert('Funcionalidade de visualização de justificativa será implementada em breve.', 'info');
}

function atualizarStatusInscricao(inscricaoId, novoStatus) {
    const linha = document.querySelector(`tr[data-inscricao-id="${inscricaoId}"]`);
    if (linha) {
        const statusElement = linha.querySelector('.status-badge');
        
        // Remover classes antigas
        statusElement.classList.remove('status-pendente', 'status-deferido', 'status-indeferido', 'status-entrevista');
        
        // Adicionar nova classe e conteúdo
        statusElement.classList.add(`status-${novoStatus}`);
        
        let novoConteudo = '';
        switch(novoStatus) {
            case 'deferido':
                novoConteudo = '<i class="bi bi-check-circle me-1"></i>Deferida';
                break;
            case 'indeferido':
                novoConteudo = '<i class="bi bi-x-circle me-1"></i>Indeferida';
                break;
            case 'entrevista':
                novoConteudo = '<i class="bi bi-person-video2 me-1"></i>Aguardando Entrevista';
                break;
            default:
                novoConteudo = '<i class="bi bi-clock me-1"></i>Pendente';
        }
        
        statusElement.innerHTML = novoConteudo;
        
        // Atualizar botões de ação
        atualizarBotoesAcao(linha, novoStatus);
        
        // Adicionar animação
        linha.classList.add('fade-in');
        setTimeout(() => linha.classList.remove('fade-in'), 500);
    }
}

function atualizarBotoesAcao(linha, status) {
    const actionButtons = linha.querySelector('.action-buttons');
    
    if (status === 'deferido' || status === 'indeferido') {
        // Desabilitar botões de ação exceto visualizar
        const botoes = actionButtons.querySelectorAll('.btn:not(.btn-outline-primary)');
        botoes.forEach(btn => {
            btn.disabled = true;
            btn.classList.add('disabled');
        });
    }
}

// ===== UTILITIES =====
function showAlert(message, type = 'info') {
    // Criar elemento de alerta
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Remover após 5 segundos
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[title]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}