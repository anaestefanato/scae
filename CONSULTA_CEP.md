# Funcionalidade de Consulta de CEP

## Descrição
Esta funcionalidade implementa a consulta automática de CEP utilizando a API gratuita do ViaCEP (https://viacep.com.br/). 

## Como funciona

### 1. Formatação Automática
- O campo CEP formata automaticamente o valor inserido no padrão `00000-000`
- Remove caracteres não numéricos automaticamente

### 2. Validação
- Valida se o CEP possui exatamente 8 dígitos
- Habilita/desabilita o botão de busca baseado na validade do CEP

### 3. Consulta Automática
- **Busca automática**: Ao sair do campo (evento `blur`), se o CEP for válido, a consulta é feita automaticamente
- **Busca manual**: Clique no botão de busca ou pressione Enter
- **API utilizada**: `https://viacep.com.br/ws/{cep}/json/`

### 4. Preenchimento Automático
- **Rua/Logradouro**: Preenchido automaticamente com `data.logradouro`
- **Bairro**: Preenchido automaticamente com `data.bairro`
- **Cidade**: Preenchido automaticamente com `data.localidade`

### 5. Feedback Visual
- **Loading**: Exibe indicador de carregamento durante a consulta
- **Sucesso**: Campos preenchidos automaticamente recebem destaque visual com animação
- **Erro**: Exibe mensagem de erro se o CEP não for encontrado
- **Estados do botão**: Muda cor baseado na validade do CEP

## Funcionalidades Implementadas

### JavaScript
- Formatação automática de CEP
- Validação de formato
- Consulta à API ViaCEP
- Preenchimento automático de campos
- Feedback visual com animações
- Tratamento de erros

### CSS
- Animação para campos preenchidos automaticamente
- Estilos para estados de sucesso/erro
- Responsividade
- Hover effects

### HTML
- Input group com botão de busca
- Mensagens de feedback (loading/error)
- IDs nos campos para preenchimento automático

## Arquivos Modificados

1. **templates/aluno/perfil.html**
   - Adicionado input group para CEP
   - IDs nos campos de endereço
   - JavaScript para funcionalidade completa

2. **static/css/perfil_aluno.css**
   - Estilos para a funcionalidade de CEP
   - Animações e feedback visual
   - Estilos gerais do perfil

## API Utilizada
- **ViaCEP**: https://viacep.com.br/
- **Endpoint**: `https://viacep.com.br/ws/{cep}/json/`
- **Gratuito**: Sim
- **Limitações**: Não especificadas para uso normal

## Exemplo de Uso
1. Usuario digita CEP: `01001000`
2. Campo formata automaticamente: `01001-000`
3. Ao sair do campo, consulta é feita automaticamente
4. Campos são preenchidos:
   - Rua: "Praça da Sé"
   - Bairro: "Sé"  
   - Cidade: "São Paulo"
5. Campos recebem destaque visual temporário
