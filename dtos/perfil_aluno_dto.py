from pydantic import BaseModel, Field, field_validator, model_validator

from util.validacoes_dto import validar_cpf, validar_telefone, validar_valor_monetario


class DadosAlunoDTO(BaseModel):
    """DTO para perfil de aluno"""
    nome: str 
    matricula: str 
    email: str
    cpf: str
    telefone: str
    curso: str 
    data_nascimento: str 
    filiacao: str  
    cep: str  
    cidade: str  
    bairro: str 
    rua: str 
    numero: str 
    estado: str 
    complemento: str 
    nome_banco: str 
    agencia_bancaria: str 
    numero_conta_bancaria: str 
    renda_familiar: float 
    quantidade_pessoas: int 
    renda_per_capita: float 
    situacao_moradia: str 
    
    @field_validator('email')
    @classmethod
    def validar_email(cls, v):
        if '@' not in v or '.' not in v.split('@')[-1]:
            raise ValueError('E-mail deve ser um endereço de e-mail válido')
        return v

    @field_validator('cpf')
    @classmethod    
    def validar_cpf(cls, v):
        #cpf_limpo = ''.join(filter(str.isdigit, v))
        cpf_limpo = validar_cpf(v)
        if len(cpf_limpo) != 11:
            raise ValueError('CPF deve conter 11 dígitos')
        return v
    
    @field_validator('telefone')
    @classmethod
    def validar_telefone(cls, v):
        #telefone_limpo = ''.join(filter(str.isdigit, v))
        telefone_limpo = validar_telefone(v)
        if telefone_limpo is None:
            raise ValueError('Telefone deve conter 10 ou 11 dígitos')
        return v

    @field_validator('data_nascimento')
    @classmethod
    def validar_data_nascimento(cls, v):
        if not v:
            raise ValueError('Data de nascimento é obrigatória')
        
        # Validar formato da data (YYYY-MM-DD)
        from datetime import datetime
        try:
            # Tentar fazer parse da data
            data = datetime.strptime(v, '%Y-%m-%d')
            
            # Verificar se a data não é no futuro
            if data > datetime.now():
                raise ValueError('Data de nascimento não pode ser no futuro')
            
            # Verificar se a pessoa tem pelo menos 14 anos (idade mínima comum para trabalhar)
            idade = (datetime.now() - data).days // 365
            if idade < 13:
                raise ValueError('É necessário ter pelo menos 14 anos')
            
            # Verificar se a data é razoável (não mais de 120 anos)
            if idade > 120:
                raise ValueError('Data de nascimento inválida')
            
            return v
        except ValueError as e:
            if 'does not match format' in str(e) or 'time data' in str(e):
                raise ValueError('Data de nascimento deve estar no formato YYYY-MM-DD (ano-mês-dia)')
            raise e
    
    @field_validator('cep')
    @classmethod
    def validar_cep(cls, v):
        if not v:
            raise ValueError('CEP é obrigatório')
        
        # Remover caracteres especiais
        cep_limpo = ''.join(filter(str.isdigit, v))
        
        if len(cep_limpo) != 8:
            raise ValueError('CEP deve conter 8 dígitos')
        
        return v
    
    @field_validator('renda_familiar')
    @classmethod
    def validar_renda_familiar(cls, v):
        from decimal import Decimal
        
        # Converter para Decimal se necessário
        if isinstance(v, (int, float, str)):
            try:
                v = float(v)
            except (ValueError, TypeError):
                raise ValueError('Renda familiar deve ser um valor numérico válido')
        
        # Validar usando a função do validacoes_dto
        valor = validar_valor_monetario(
            Decimal(str(v)),
            campo="Renda familiar",
            obrigatorio=True,
            min_valor=Decimal('1')  # Não pode ser 0 ou negativo
        )
        
        if valor is None or valor == 0:
            raise ValueError('Renda familiar deve ser maior que zero')
        
        return float(valor)
    
    @field_validator('renda_per_capita')
    @classmethod
    def validar_renda_per_capita(cls, v):
        from decimal import Decimal
        
        # Converter para Decimal se necessário
        if isinstance(v, (int, float, str)):
            try:
                v = float(v)
            except (ValueError, TypeError):
                raise ValueError('Renda per capita deve ser um valor numérico válido')
        
        # Validar usando a função do validacoes_dto
        valor = validar_valor_monetario(
            Decimal(str(v)),
            campo="Renda per capita",
            obrigatorio=True,
            min_valor=Decimal('1')  # Não pode ser 0 ou negativo
        )
        
        if valor is None or valor == 0:
            raise ValueError('Renda per capita deve ser maior que zero')
        
        return float(valor)
    
    @field_validator('quantidade_pessoas')
    @classmethod
    def validar_quantidade_pessoas(cls, v):
        if v is None or v <= 0:
            raise ValueError('Quantidade de pessoas deve ser maior que zero')
        
        if v > 50:
            raise ValueError('Quantidade de pessoas não pode ser maior que 50')
        
        return v
    
    @model_validator(mode='after')
    def validar_renda_per_capita_menor_que_familiar(self):
        """Valida se a renda per capita não é maior que a renda familiar"""
        if self.renda_per_capita and self.renda_familiar:
            if self.renda_per_capita > self.renda_familiar:
                raise ValueError('Renda per capita não pode ser maior que a renda familiar')
        return self
