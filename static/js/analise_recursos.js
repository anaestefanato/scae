const recursosData = {
    'Maria Silva Santos': {
        aluno: 'Maria Silva Santos',
        matricula: '2023001234',
        curso: 'Técnico em Informática',
        auxilioOriginal: 'Auxílio Transporte',
        decisaoOriginal: 'Indeferido',
        motivoOriginal: 'Renda familiar acima do limite estabelecido no edital',
        dataRecurso: '15/09/2025',
        prazo: '2 dias',
        prioridade: 'Alta',
        justificativa: 'Solicito a revisão da decisão tendo em vista que houve alteração na situação financeira familiar. Meu pai perdeu o emprego em agosto de 2025, reduzindo significativamente a renda familiar. Anexo comprovantes da rescisão contratual e declaração de desemprego.',
        documentosAnexos: [
            { nome: 'Rescisão Contratual - Pai.pdf', tamanho: '245 KB' },
            { nome: 'Declaração de Desemprego.pdf', tamanho: '156 KB' },
            { nome: 'Nova Declaração de Renda.pdf', tamanho: '189 KB' }
        ],
        timeline: [
            { tipo: 'inscricao', titulo: 'Inscrição Realizada', data: '01/08/2025', descricao: 'Aluna realizou inscrição no Auxílio Transporte' },
            { tipo: 'avaliacao', titulo: 'Primeira Avaliação', data: '20/08/2025', descricao: 'Inscrição avaliada e indeferida por renda familiar acima do limite' },
            { tipo: 'recurso', titulo: 'Recurso Interposto', data: '15/09/2025', descricao: 'Aluna interpôs recurso com nova documentação' }
        ]
    },
    'João Paulo Oliveira': {
        aluno: 'João Paulo Oliveira',
        matricula: '2023005678',
        curso: 'Técnico em Edificações',
        auxilioOriginal: 'Auxílio Alimentação',
        decisaoOriginal: 'Indeferido',
        motivoOriginal: 'Documentação incompleta - faltou comprovante de residência atualizado',
        dataRecurso: '12/09/2025',
        prazo: '5 dias',
        prioridade: 'Média',
        justificativa: 'Venho por meio deste recurso apresentar a documentação que estava em falta na minha inscrição inicial. O comprovante de residência não pôde ser obtido na época devido a problemas com a documentação do imóvel. Agora apresento toda a documentação necessária.',
        documentosAnexos: [
            { nome: 'Comprovante de Residência Atualizado.pdf', tamanho: '198 KB' },
            { nome: 'Contrato de Locação.pdf', tamanho: '234 KB' }
        ],
        timeline: [
            { tipo: 'inscricao', titulo: 'Inscrição Realizada', data: '05/08/2025', descricao: 'Aluno realizou inscrição no Auxílio Alimentação' },
            { tipo: 'avaliacao', titulo: 'Primeira Avaliação', data: '25/08/2025', descricao: 'Inscrição indeferida por documentação incompleta' },
            { tipo: 'recurso', titulo: 'Recurso Interposto', data: '12/09/2025', descricao: 'Aluno interpôs recurso com documentação complementar' }
        ]
    },
    'Ana Carolina Mendes': {
        aluno: 'Ana Carolina Mendes',
        matricula: '2023009876',
        curso: 'Técnico em Enfermagem',
        auxilioOriginal: 'Auxílio Moradia',
        decisaoOriginal: 'Indeferido',
        motivoOriginal: 'Não atendimento ao critério de distância mínima da residência até a instituição',
        dataRecurso: '10/09/2025',
        prazo: '7 dias',
        prioridade: 'Baixa',
        justificativa: 'Solicito reconsideração da decisão pois, embora minha residência não atenda exatamente ao critério de distância, não há transporte público adequado no horário de funcionamento dos cursos noturnos, o que torna necessário o auxílio moradia.',
        documentosAnexos: [
            { nome: 'Mapa de Localização.pdf', tamanho: '167 KB' },
            { nome: 'Horários de Transporte Público.pdf', tamanho: '145 KB' },
            { nome: 'Declaração de Inexistência de Transporte.pdf', tamanho: '123 KB' }
        ],
        timeline: [
            { tipo: 'inscricao', titulo: 'Inscrição Realizada', data: '10/08/2025', descricao: 'Aluna realizou inscrição no Auxílio Moradia' },
            { tipo: 'avaliacao', titulo: 'Primeira Avaliação', data: '30/08/2025', descricao: 'Inscrição indeferida por não atender critério de distância' },
            { tipo: 'recurso', titulo: 'Recurso Interposto', data: '10/09/2025', descricao: 'Aluna interpôs recurso contestando critério de distância' }
        ]
    },
    'Carlos Eduardo Santos': {
        aluno: 'Carlos Eduardo Santos',
        matricula: '2023002468',
        curso: 'Técnico em Mecânica',
        auxilioOriginal: 'Auxílio Material Didático',
        decisaoOriginal: 'Parcialmente Deferido',
        motivoOriginal: 'Auxílio aprovado apenas para material básico, equipamentos específicos não contemplados',
        dataRecurso: '08/09/2025',
        prazo: 'Vencido',
        prioridade: 'Média',
        justificativa: 'Contesto a decisão de deferimento parcial pois os equipamentos específicos solicitados (multímetro, alicate amperímetro) são essenciais para o desenvolvimento das atividades práticas do curso e não são fornecidos pela instituição.',
        documentosAnexos: [
            { nome: 'Lista de Material - Coordenação.pdf', tamanho: '234 KB' },
            { nome: 'Orçamento de Equipamentos.pdf', tamanho: '187 KB' },
            { nome: 'Declaração da Coordenação.pdf', tamanho: '145 KB' }
        ],
        timeline: [
            { tipo: 'inscricao', titulo: 'Inscrição Realizada', data: '15/07/2025', descricao: 'Aluno realizou inscrição no Auxílio Material Didático' },
            { tipo: 'avaliacao', titulo: 'Primeira Avaliação', data: '25/07/2025', descricao: 'Inscrição parcialmente deferida' },
            { tipo: 'recurso', titulo: 'Recurso Interposto', data: '08/09/2025', descricao: 'Aluno interpôs recurso solicitando deferimento integral' }
        ]
    }
};

document.addEventListener('DOMContentLoaded', function() {
    console.log('Analise Recursos JS carregado');
    
    // Funcionalidade de filtro
    const filtroStatus = document.getElementById('filtroStatus');
    const btnFiltrar = document.getElementById('btnFiltrar');
    const searchRecurso = document.getElementById('searchRecurso');
    
    if (btnFiltrar) {
        btnFiltrar.addEventListener('click', filtrarRecursos);
    }
    
    if (searchRecurso) {
        searchRecurso.addEventListener('keyup', function(e) {
            if (e.key === 'Enter') {
                filtrarRecursos();
            }
        });
    }
});

function abrirDetalhesRecurso(button) {
    const row = button.closest('tr');
    const nomeAluno = row.cells[0].textContent.trim();
    const dados = recursosData[nomeAluno];
    
    if (!dados) {
        console.error('Dados não encontrados para:', nomeAluno);
        return;
    }
    
    const modalBody = document.getElementById('detalhesRecursoBody');
    
    modalBody.innerHTML = `
        <div class="row">
            <div class="col-md-6">
                <div class="recurso-section">
                    <h6><i class="bi bi-person-fill"></i>Informações do Aluno</h6>
                    <div class="info-row">
                        <span class="info-label">Nome:</span>
                        <span class="info-value">${dados.aluno}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Matrícula:</span>
                        <span class="info-value">${dados.matricula}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Curso:</span>
                        <span class="info-value">${dados.curso}</span>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="recurso-section">
                    <h6><i class="bi bi-clipboard-data"></i>Informações do Recurso</h6>
                    <div class="info-row">
                        <span class="info-label">Auxílio:</span>
                        <span class="info-value">${dados.auxilioOriginal}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Decisão Original:</span>
                        <span class="info-value"><span class="badge bg-danger">${dados.decisaoOriginal}</span></span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Data do Recurso:</span>
                        <span class="info-value">${dados.dataRecurso}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Prioridade:</span>
                        <span class="info-value"><span class="priority-${dados.prioridade.toLowerCase()}">${dados.prioridade}</span></span>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="recurso-section">
            <h6><i class="bi bi-exclamation-triangle"></i>Motivo da Decisão Original</h6>
            <div class="justificativa-box">
                ${dados.motivoOriginal}
            </div>
        </div>
        
        <div class="recurso-section">
            <h6><i class="bi bi-chat-square-text"></i>Justificativa do Recurso</h6>
            <div class="justificativa-box">
                ${dados.justificativa}
            </div>
        </div>
        
        <div class="recurso-section">
            <h6><i class="bi bi-paperclip"></i>Documentos Anexos</h6>
            ${dados.documentosAnexos.map(doc => `
                <div class="documento-item">
                    <div class="documento-info">
                        <i class="bi bi-file-earmark-pdf"></i>
                        <span class="documento-nome">${doc.nome}</span>
                        <span class="documento-size">(${doc.tamanho})</span>
                    </div>
                    <button class="btn btn-sm btn-outline-primary btn-visualizar" onclick="visualizarDocumento('${doc.nome}')">
                        <i class="bi bi-eye"></i> Visualizar
                    </button>
                </div>
            `).join('')}
        </div>
        
        <div class="recurso-section">
            <h6><i class="bi bi-clock-history"></i>Histórico do Processo</h6>
            ${dados.timeline.map(item => `
                <div class="timeline-item">
                    <div class="timeline-icon ${item.tipo}">
                        <i class="bi bi-${item.tipo === 'inscricao' ? 'file-earmark-plus' : item.tipo === 'avaliacao' ? 'search' : 'exclamation-triangle'}"></i>
                    </div>
                    <div class="timeline-content">
                        <h6>${item.titulo}</h6>
                        <p>${item.descricao}</p>
                        <div class="timeline-date">${item.data}</div>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
    
    // Configurar botões do modal
    const btnDeferirModal = document.getElementById('btnDeferirModal');
    const btnIndeferirModal = document.getElementById('btnIndeferirModal');
    
    btnDeferirModal.onclick = () => deferirRecursoModal(nomeAluno);
    btnIndeferirModal.onclick = () => indeferirRecursoModal(nomeAluno);
}

function deferirRecursoModal(nomeAluno) {
    if (!confirm('Tem certeza que deseja DEFERIR este recurso?')) {
        return;
    }
    
    const modal = bootstrap.Modal.getInstance(document.getElementById('detalhesRecursoModal'));
    modal.hide();
    
    // Encontrar a linha correspondente na tabela
    const rows = document.querySelectorAll('#recursosTableBody tr');
    for (let row of rows) {
        if (row.cells[0].textContent.trim() === nomeAluno) {
            processarDecisaoRecurso(row, 'deferido');
            break;
        }
    }
}

function indeferirRecursoModal(nomeAluno) {
    if (!confirm('Tem certeza que deseja INDEFERIR este recurso?')) {
        return;
    }
    
    const modal = bootstrap.Modal.getInstance(document.getElementById('detalhesRecursoModal'));
    modal.hide();
    
    // Encontrar a linha correspondente na tabela
    const rows = document.querySelectorAll('#recursosTableBody tr');
    for (let row of rows) {
        if (row.cells[0].textContent.trim() === nomeAluno) {
            processarDecisaoRecurso(row, 'indeferido');
            break;
        }
    }
}

function processarDecisaoRecurso(row, decisao) {
    const statusCell = row.cells[4].querySelector('span');
    const actionButtons = row.querySelector('.action-buttons');
    
    // Simular processamento
    setTimeout(() => {
        // Atualizar status
        statusCell.className = decisao === 'deferido' ? 'badge bg-success' : 'badge bg-danger';
        statusCell.textContent = decisao === 'deferido' ? 'Deferido' : 'Indeferido';
        
        // Adicionar classe de animação
        row.classList.add('status-changed');
        if (decisao === 'deferido') {
            row.classList.add('recurso-deferido');
        } else {
            row.classList.add('recurso-indeferido');
        }
        
        // Atualizar botão para mostrar apenas o resultado
        const eyeButton = actionButtons.querySelector('.btn-outline-primary');
        if (decisao === 'deferido') {
            eyeButton.innerHTML = '<i class="bi bi-check-circle-fill text-success"></i>';
            eyeButton.title = 'Recurso Deferido';
        } else {
            eyeButton.innerHTML = '<i class="bi bi-x-circle-fill text-danger"></i>';
            eyeButton.title = 'Recurso Indeferido';
        }
        eyeButton.classList.remove('btn-outline-primary');
        eyeButton.classList.add('btn-outline-secondary', 'disabled');
        eyeButton.disabled = true;
        
        // Remover animação após um tempo
        setTimeout(() => {
            row.classList.remove('status-changed');
        }, 500);
        
        // Mostrar notificação
        showNotification(`Recurso ${decisao} com sucesso!`, decisao === 'deferido' ? 'success' : 'danger');
        
    }, 1500);
}

function filtrarRecursos() {
    const filtroValue = document.getElementById('filtroStatus').value.toLowerCase();
    const searchValue = document.getElementById('searchRecurso').value.toLowerCase();
    const rows = document.querySelectorAll('#recursosTableBody tr');
    
    rows.forEach(row => {
        const aluno = row.cells[0].textContent.toLowerCase();
        const auxilio = row.cells[1].textContent.toLowerCase();
        const status = row.cells[4].textContent.toLowerCase();
        
        const matchSearch = !searchValue || aluno.includes(searchValue) || auxilio.includes(searchValue);
        const matchFilter = !filtroValue || status.includes(filtroValue.replace('-', ' '));
        
        if (matchSearch && matchFilter) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

function visualizarDocumento(nomeDocumento) {
    // Simular abertura de documento
    alert(`Abrindo documento: ${nomeDocumento}`);
    // Aqui você implementaria a lógica real de visualização do documento
}

function showNotification(message, type = 'info') {
    // Criar notificação simples
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px; 
        right: 20px; 
        z-index: 9999; 
        min-width: 300px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remover após 3 segundos
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 3000);
}
