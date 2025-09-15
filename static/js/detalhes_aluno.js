// Detalhes do Aluno - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar funcionalidades da página
    initializePageFunctions();
    loadAlunoData();
    setupEventListeners();
});

// Função para inicializar as funcionalidades da página
function initializePageFunctions() {
    console.log('Página de detalhes do aluno carregada');
    
    // Adicionar animações suaves aos elementos
    animateElements();
    
    // Configurar tooltips se necessário
    setupTooltips();
}

// Função para carregar dados do aluno (simulação)
function loadAlunoData() {
    // Aqui normalmente você faria uma requisição para buscar os dados do aluno
    // Por enquanto, vamos usar dados simulados
    
    const alunoId = getAlunoIdFromUrl();
    
    if (alunoId) {
        // Simular carregamento de dados
        setTimeout(() => {
            updateAlunoInfo(alunoId);
        }, 500);
    }
}

// Função para obter ID do aluno da URL
function getAlunoIdFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id') || '1'; // ID padrão para demonstração
}

// Função para atualizar informações do aluno
function updateAlunoInfo(alunoId) {
    // Buscar aluno nos dados (simular busca no backend)
    const aluno = findAlunoById(alunoId);
    
    if (!aluno) {
        showNotification('Aluno não encontrado!', 'error');
        return;
    }
    
    // Atualizar elementos da página
    document.getElementById('alunoNome').textContent = aluno.nome;
    document.getElementById('alunoInfo').textContent = `Aluno | Matrícula: ${aluno.matricula}`;
    
    // Atualizar badges de auxílios
    updateAuxiliosBadges(aluno.auxilios);
    
    // Atualizar dados pessoais
    updateDadosPessoais(aluno);
}

// Função para buscar aluno por ID
function findAlunoById(id) {
    // Simular dados do aluno baseado no ID
    const nomes = [
        'Ana Silva Santos', 'João Pedro Oliveira', 'Maria Carolina Costa', 'Carlos Eduardo Lima',
        'Fernanda Alves Souza', 'Rafael Santos Pereira', 'Juliana Moreira Lima', 'Bruno Costa Silva',
        'Camila Rodrigues Alves', 'Lucas Gabriel Santos', 'Amanda Ferreira Costa', 'Diego Henrique Lima',
        'Gabriela Santos Oliveira', 'Matheus Almeida Silva', 'Larissa Pereira Costa', 'Felipe Rodrigues Santos'
    ];
    
    const cursos = ['Técnico em Informática', 'Técnico em Eletromecânica'];
    const auxiliosTipos = ['Transporte', 'Moradia', 'Alimentação', 'Material Didático'];
    const periodos = ['1º Período', '2º Período', '3º Período', '4º Período'];
    
    // Usar ID para gerar dados consistentes
    const nome = nomes[id % nomes.length];
    const curso = cursos[id % cursos.length];
    const periodo = periodos[id % periodos.length];
    
    // Gerar auxilios baseado no ID
    const numAuxilios = (id % 4) + 1;
    const auxiliosAluno = [];
    const auxiliosSelecionados = auxiliosTipos.slice(0, numAuxilios);
    
    let valorTotal = 0;
    auxiliosSelecionados.forEach(auxilio => {
        let valor = 0;
        switch(auxilio) {
            case 'Transporte':
                valor = 180;
                break;
            case 'Alimentação':
                valor = 100;
                break;
            case 'Moradia':
                valor = 300;
                break;
            case 'Material Didático':
                valor = 150;
                break;
        }
        auxiliosAluno.push({ nome: auxilio, valor: valor });
        valorTotal += valor;
    });
    
    return {
        id: id,
        nome: nome,
        matricula: `2023${String(id).padStart(6, '0')}`,
        curso: curso,
        periodo: periodo,
        auxilios: auxiliosAluno,
        valorTotal: valorTotal,
        situacao: id % 10 === 0 ? 'Suspenso' : 'Ativo',
        email: `${nome.toLowerCase().replace(/\s+/g, '.')}@aluno.ifes.edu.br`,
        cpf: generateCPF(id),
        dataNascimento: generateDataNascimento(id),
        telefone: generateTelefone(id),
        endereco: generateEndereco(id),
        rendaFamiliar: (Math.floor((id * 1.3) % 50) + 15) * 100, // Entre R$ 1.500 e R$ 6.400
        membrosNaFamilia: (id % 6) + 2, // Entre 2 e 7 membros
        situacaoMoradia: id % 3 === 0 ? 'Alugada' : id % 3 === 1 ? 'Própria' : 'Cedida'
    };
}

// Funções auxiliares para gerar dados
function generateCPF(id) {
    const base = String(id).padStart(9, '0');
    return `${base.slice(0,3)}.${base.slice(3,6)}.${base.slice(6,9)}-${(id % 99).toString().padStart(2, '0')}`;
}

function generateDataNascimento(id) {
    const year = 2005 - (id % 3); // Entre 2002 e 2005
    const month = (id % 12) + 1;
    const day = (id % 28) + 1;
    return `${day.toString().padStart(2, '0')}/${month.toString().padStart(2, '0')}/${year}`;
}

function generateTelefone(id) {
    const num = (27000000000 + (id * 123456)) % 99999999999;
    const str = num.toString().padStart(11, '0');
    return `(${str.slice(0,2)}) ${str.slice(2,7)}-${str.slice(7,11)}`;
}

function generateEndereco(id) {
    const ruas = ['Rua das Flores', 'Av. Central', 'Rua dos Estudantes', 'Rua da Paz', 'Av. das Américas'];
    const bairros = ['Centro', 'Vila Nova', 'Jardim Tropical', 'São José', 'Santa Rita'];
    const cidades = ['Vila Velha', 'Vitória', 'Serra', 'Cariacica', 'Viana'];
    
    return {
        rua: `${ruas[id % ruas.length]}, ${100 + (id % 900)}`,
        bairro: bairros[id % bairros.length],
        cidade: cidades[id % cidades.length],
        cep: `29${(100 + id % 900).toString()}-${(id % 999).toString().padStart(3, '0')}`
    };
}

// Função para atualizar dados pessoais na página
function updateDadosPessoais(aluno) {
    // Atualizar seções de dados pessoais
    const endereco = aluno.endereco;
    const rendaPerCapita = aluno.rendaFamiliar / aluno.membrosNaFamilia;
    
    // Aqui você pode atualizar os elementos HTML com os dados do aluno
    // Por exemplo, se tivesse elementos com IDs específicos:
    /*
    document.getElementById('alunoNomeCompleto').textContent = aluno.nome;
    document.getElementById('alunoCPF').textContent = aluno.cpf;
    document.getElementById('alunoDataNascimento').textContent = aluno.dataNascimento;
    // ... etc
    */
}

// Função para atualizar badges de auxílios
function updateAuxiliosBadges(auxilios) {
    const container = document.getElementById('auxiliosAtivos');
    container.innerHTML = '';
    
    auxilios.forEach(auxilio => {
        const badge = document.createElement('span');
        
        // Definir classe baseada no tipo de auxílio
        let badgeClass = 'badge bg-primary';
        switch(auxilio.nome) {
            case 'Transporte':
                badgeClass = 'badge bg-primary';
                break;
            case 'Alimentação':
                badgeClass = 'badge bg-success';
                break;
            case 'Moradia':
                badgeClass = 'badge bg-warning text-dark';
                break;
            case 'Material Didático':
                badgeClass = 'badge bg-info';
                break;
        }
        
        badge.className = badgeClass;
        badge.textContent = auxilio.nome;
        container.appendChild(badge);
    });
}

// Função para configurar event listeners
function setupEventListeners() {
    // Botão de voltar
    const voltarBtn = document.querySelector('[onclick="voltarParaLista()"]');
    if (voltarBtn) {
        voltarBtn.addEventListener('click', voltarParaLista);
    }
    
    // Botões de ação
    setupActionButtons();
    
    // Histórico completo
    const historicoBtn = document.querySelector('.btn-outline-primary.btn-sm');
    if (historicoBtn) {
        historicoBtn.addEventListener('click', showHistoricoCompleto);
    }
}

// Função para configurar botões de ação
function setupActionButtons() {
    const actionButtons = document.querySelectorAll('.card:last-child .btn');
    
    actionButtons.forEach((btn, index) => {
        btn.addEventListener('click', function() {
            const actions = [
                () => agendarEntrevista(),
                () => gerarRelatorio(),
                () => suspenderAuxilio()
            ];
            
            if (actions[index]) {
                actions[index]();
            }
        });
    });
}

// Função para voltar para a lista de alunos
function voltarParaLista() {
    window.history.back();
    // Alternativa: redirecionar diretamente
    // window.location.href = '/assistente/alunos';
}

// Função para agendar entrevista
function agendarEntrevista() {
    // Mostrar modal de agendamento ou redirecionar
    const alunoNome = document.getElementById('alunoNome').textContent;
    
    if (confirm(`Deseja agendar uma entrevista com ${alunoNome}?`)) {
        // Aqui implementaria a lógica de agendamento
        showNotification('Entrevista agendada com sucesso!', 'success');
    }
}

// Função para gerar relatório
function gerarRelatorio() {
    const alunoNome = document.getElementById('alunoNome').textContent;
    
    showNotification(`Gerando relatório para ${alunoNome}...`, 'info');
    
    // Simular geração de relatório
    setTimeout(() => {
        showNotification('Relatório gerado com sucesso!', 'success');
    }, 2000);
}

// Função para suspender auxílio
function suspenderAuxilio() {
    const alunoNome = document.getElementById('alunoNome').textContent;
    
    if (confirm(`Tem certeza que deseja suspender o auxílio de ${alunoNome}? Esta ação pode ser irreversível.`)) {
        // Aqui implementaria a lógica de suspensão
        showNotification('Auxílio suspenso com sucesso!', 'warning');
    }
}

// Função para mostrar histórico completo
function showHistoricoCompleto() {
    // Criar modal ou redirecionar para página de histórico
    const modal = createHistoricoModal();
    document.body.appendChild(modal);
    
    const bootstrapModal = new bootstrap.Modal(modal);
    bootstrapModal.show();
}

// Função para criar modal de histórico
function createHistoricoModal() {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">
                        <i class="bi bi-clock-history me-2"></i>
                        Histórico Completo de Recebimentos
                    </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Data</th>
                                    <th>Auxílio</th>
                                    <th>Valor</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Setembro 2025</td>
                                    <td>Auxílio Transporte</td>
                                    <td>R$ 180,00</td>
                                    <td><span class="badge bg-success">Pago</span></td>
                                </tr>
                                <tr>
                                    <td>Setembro 2025</td>
                                    <td>Auxílio Alimentação</td>
                                    <td>R$ 100,00</td>
                                    <td><span class="badge bg-success">Pago</span></td>
                                </tr>
                                <tr>
                                    <td>Agosto 2025</td>
                                    <td>Auxílio Transporte</td>
                                    <td>R$ 180,00</td>
                                    <td><span class="badge bg-success">Pago</span></td>
                                </tr>
                                <tr>
                                    <td>Agosto 2025</td>
                                    <td>Auxílio Alimentação</td>
                                    <td>R$ 100,00</td>
                                    <td><span class="badge bg-success">Pago</span></td>
                                </tr>
                                <tr>
                                    <td>Julho 2025</td>
                                    <td>Auxílio Transporte</td>
                                    <td>R$ 180,00</td>
                                    <td><span class="badge bg-warning">Pendente</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-outline-primary">
                        <i class="bi bi-download me-2"></i>
                        Exportar
                    </button>
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Fechar
                    </button>
                </div>
            </div>
        </div>
    `;
    
    return modal;
}

// Função para animar elementos na entrada
function animateElements() {
    const cards = document.querySelectorAll('.data-card');
    
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease-out';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Função para configurar tooltips
function setupTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Função para mostrar notificações
function showNotification(message, type = 'info') {
    // Criar elemento de notificação
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} notification-toast`;
    notification.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="bi bi-check-circle-fill me-2"></i>
            <span>${message}</span>
        </div>
    `;
    
    // Adicionar estilos
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        animation: slideInRight 0.3s ease-out;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    
    document.body.appendChild(notification);
    
    // Remover após 3 segundos
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Adicionar estilos de animação para notificações
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .notification-toast {
        border-radius: 10px;
        border: none;
    }
`;
document.head.appendChild(style);

// Função para lidar com erros
function handleError(error) {
    console.error('Erro na página de detalhes do aluno:', error);
    showNotification('Ocorreu um erro. Tente novamente.', 'danger');
}

// Exportar funções para uso global se necessário
window.voltarParaLista = voltarParaLista;
