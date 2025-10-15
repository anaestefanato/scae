from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

from util.validacoes_dto import validar_cpf, validar_telefone, validar_valor_monetario


class PrimeiraInscricaoDTO(BaseModel):
    """DTO para primeira inscrição em edital"""
    
    # Dados pessoais
    nome: str 
    cpf: str
    data_nascimento: str
    telefone: str
    email: str
    logradouro: str
    numero: str 
    complemento: Optional[str]
    bairro: str
    cidade: str
    estado: str
    cep: str
    
    # Dados acadêmicos
    curso: str
    matricula: str
    ano_ingresso: int
    ano_conclusao_previsto: int

    # Dados financeiros
    pessoas_residencia: int
    renda_percapita: float
    bolsa_pesquisa: str
    cad_unico: str
    bolsa_familia: str 
    
    # Auxílios selecionados
    auxilios: List[str] 
    
    # Dados de transporte (opcionais)
    tipo_transporte: Optional[str] 
    tipo_onibus: Optional[List[str]] 
    gasto_passagens_dia: Optional[float] = None
    gasto_van_mensal: Optional[float] = None 

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('Nome deve ter pelo menos 3 caracteres')
        
        # Verificar se contém apenas letras e espaços
        if not all(c.isalpha() or c.isspace() for c in v):
            raise ValueError('Nome deve conter apenas letras e espaços')
        
        return v.strip()
    
    @field_validator('cpf')
    @classmethod    
    def validar_cpf_campo(cls, v):
        cpf_limpo = validar_cpf(v)
        if cpf_limpo is None or len(cpf_limpo) != 11:
            raise ValueError('CPF inválido. Deve conter 11 dígitos')
        return v
    
    @field_validator('email')
    @classmethod
    def validar_email(cls, v):
        if '@' not in v or '.' not in v.split('@')[-1]:
            raise ValueError('E-mail inválido')
        
        # Verificar formato básico
        partes = v.split('@')
        if len(partes) != 2 or len(partes[0]) == 0 or len(partes[1]) < 3:
            raise ValueError('E-mail inválido')
        
        return v.lower().strip()
    
    @field_validator('telefone')
    @classmethod
    def validar_telefone_campo(cls, v):
        telefone_limpo = validar_telefone(v)
        if telefone_limpo is None:
            raise ValueError('Telefone inválido. Deve conter 10 ou 11 dígitos')
        return v
    
    @field_validator('data_nascimento')
    @classmethod
    def validar_data_nascimento(cls, v):
        if not v:
            raise ValueError('Data de nascimento é obrigatória')
        
        try:
            # Tentar fazer parse da data
            data = datetime.strptime(v, '%Y-%m-%d')
            
            # Verificar se a data não é no futuro
            if data > datetime.now():
                raise ValueError('Data de nascimento não pode ser no futuro')
            
            # Verificar idade mínima (14 anos)
            idade = (datetime.now() - data).days // 365
            if idade < 13:
                raise ValueError('É necessário ter pelo menos 13 anos')
            
            # Verificar idade máxima razoável (120 anos)
            if idade > 120:
                raise ValueError('Data de nascimento inválida')
            
            return v
        except ValueError as e:
            if 'does not match format' in str(e) or 'time data' in str(e):
                raise ValueError('Data de nascimento deve estar no formato YYYY-MM-DD')
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
    
    @field_validator('matricula')
    @classmethod
    def validar_matricula(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('Matrícula deve ter pelo menos 3 caracteres')
        return v.strip()
    
    @field_validator('curso')
    @classmethod
    def validar_curso(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('Curso deve ter pelo menos 3 caracteres')
        return v.strip()
    
    @field_validator('pessoas_residencia')
    @classmethod
    def validar_pessoas_residencia(cls, v):
        if v is None or v <= 0:
            raise ValueError('Número de pessoas na residência deve ser maior que zero')
        
        if v > 50:
            raise ValueError('Número de pessoas na residência não pode ser maior que 50')
        
        return v
    
    @field_validator('renda_percapita')
    @classmethod
    def validar_renda_percapita(cls, v):
        # Mapear códigos de renda para valores numéricos (médios da faixa)
        RENDA_MAPPING = {
            'menor_1': 706.0,      # Média até 1 salário mínimo (0 a 1412)
            'ate_1_5': 1765.0,     # Média de 1 a 1,5 salários (1412 a 2118)
            'maior_1_5': 2824.0    # Média acima de 1,5 salários (2118+)
        }
        
        if isinstance(v, str):
            # Verificar se é um código de renda
            if v in RENDA_MAPPING:
                v = RENDA_MAPPING[v]
            else:
                try:
                    v = float(v)
                except (ValueError, TypeError):
                    raise ValueError('Renda per capita deve ser um valor numérico válido ou uma faixa selecionada')
        
        if v < 0:
            raise ValueError('Renda per capita não pode ser negativa')
        
        # Validar limite razoável (3 salários mínimos para auxílio estudantil)
        if v > 4236:  # 3 * 1412 (salário mínimo 2025)
            raise ValueError('Renda per capita muito alta para auxílio estudantil')
        
        return v
    
    @field_validator('auxilios')
    @classmethod
    def validar_auxilios(cls, v):
        if not v or len(v) == 0:
            raise ValueError('Selecione pelo menos um tipo de auxílio')
        
        # Validar se os auxílios são válidos
        auxilios_validos = ['transporte', 'moradia', 'alimentacao', 'material']
        for auxilio in v:
            if auxilio not in auxilios_validos:
                raise ValueError(f'Auxílio inválido: {auxilio}')
        
        return v
    
    @field_validator('gasto_passagens_dia', 'gasto_van_mensal', mode='before')
    @classmethod
    def converter_strings_vazias_em_none(cls, v):
        """Converte strings vazias em None para campos opcionais de float"""
        if v == '' or v is None:
            return None
        return v
    
    @model_validator(mode='after')
    def validar_ano_conclusao(self):
        """Valida se o ano de conclusão é posterior ao ano de ingresso"""
        if self.ano_conclusao_previsto <= self.ano_ingresso:
            raise ValueError('Ano de conclusão previsto deve ser posterior ao ano de ingresso')
        
        # Validar duração razoável do curso (máximo 10 anos)
        duracao = self.ano_conclusao_previsto - self.ano_ingresso
        if duracao > 10:
            raise ValueError('Duração do curso não pode ser maior que 10 anos')
        
        return self
    
    @model_validator(mode='after')
    def validar_dados_transporte(self):
        """Valida se os dados de transporte são obrigatórios quando o auxílio transporte é selecionado"""
        if 'transporte' in self.auxilios:
            if not self.tipo_transporte:
                raise ValueError('Tipo de transporte é obrigatório quando auxílio transporte é selecionado')
            
            # Validar tipos de transporte válidos
            tipos_validos = ['onibus', 'van']
            if self.tipo_transporte not in tipos_validos:
                raise ValueError(f'Tipo de transporte inválido: {self.tipo_transporte}')
            
            # Validar campos específicos de ônibus
            if self.tipo_transporte == 'onibus':
                if not self.tipo_onibus or len(self.tipo_onibus) == 0:
                    raise ValueError('Tipo de ônibus é obrigatório quando transporte por ônibus é selecionado')
                
                if self.gasto_passagens_dia is None or self.gasto_passagens_dia <= 0:
                    raise ValueError('Gasto com passagens por dia é obrigatório e deve ser maior que zero')
                
                # Validar limite razoável (máximo R$ 50 por dia)
                if self.gasto_passagens_dia > 50:
                    raise ValueError('Gasto com passagens por dia não pode ser maior que R$ 50,00')
            
            # Validar campos específicos de van
            if self.tipo_transporte == 'van':
                if self.gasto_van_mensal is None or self.gasto_van_mensal <= 0:
                    raise ValueError('Gasto mensal com van é obrigatório e deve ser maior que zero')
                
                # Validar limite razoável (máximo R$ 800 por mês)
                if self.gasto_van_mensal > 800:
                    raise ValueError('Gasto mensal com van não pode ser maior que R$ 800,00')
        
        return self

