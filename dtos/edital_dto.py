from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from typing import Optional


class EditalDTO(BaseModel):
    """DTO para criação/publicação de edital"""
    
    model_config = ConfigDict(
        str_min_length=1,
        str_strip_whitespace=True
    )
    
    # Dados principais
    titulo: str
    descricao: str
    data_publicacao: str
    
    # Período de inscrição
    data_inicio_inscricao: str
    data_fim_inscricao: str
    
    # Período de vigência dos auxílios
    data_inicio_vigencia: str
    data_fim_vigencia: str
    
    # Status
    status: Optional[str] = "ativo"
    
    @field_validator('titulo')
    @classmethod
    def validar_titulo(cls, v):
        if not v or len(v.strip()) < 5:
            raise ValueError('Título deve ter pelo menos 5 caracteres')
        
        if len(v.strip()) > 200:
            raise ValueError('Título não pode exceder 200 caracteres')
        
        return v.strip()
    
    @field_validator('descricao')
    @classmethod
    def validar_descricao(cls, v):
        if not v or len(v.strip()) < 10:
            raise ValueError('Descrição deve ter pelo menos 10 caracteres')
        
        if len(v.strip()) > 1000:
            raise ValueError('Descrição não pode exceder 1000 caracteres')
        
        return v.strip()
    
    @field_validator('data_publicacao')
    @classmethod
    def validar_data_publicacao(cls, v):
        if not v:
            raise ValueError('Data de publicação é obrigatória')
        
        try:
            # Validar formato da data
            data = datetime.strptime(v, '%Y-%m-%d')
            
            # Data de publicação pode ser no futuro ou passado
            # mas não pode ser muito antiga (mais de 2 anos)
            anos_atras = (datetime.now() - data).days // 365
            if anos_atras > 2:
                raise ValueError('Data de publicação não pode ser superior a 2 anos no passado')
            
            return v
        except ValueError as e:
            if 'does not match format' in str(e) or 'time data' in str(e):
                raise ValueError('Data de publicação deve estar no formato AAAA-MM-DD')
            raise e
    
    @field_validator('data_inicio_inscricao')
    @classmethod
    def validar_data_inicio_inscricao(cls, v):
        if not v:
            raise ValueError('Data de início da inscrição é obrigatória')
        
        try:
            # Validar formato da data
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Data de início da inscrição deve estar no formato AAAA-MM-DD')
    
    @field_validator('data_fim_inscricao')
    @classmethod
    def validar_data_fim_inscricao(cls, v, info):
        if not v:
            raise ValueError('Data de fim da inscrição é obrigatória')
        
        try:
            # Validar formato da data
            data_fim = datetime.strptime(v, '%Y-%m-%d')
            
            # Validar se é posterior à data de início
            if 'data_inicio_inscricao' in info.data:
                data_inicio = datetime.strptime(info.data['data_inicio_inscricao'], '%Y-%m-%d')
                if data_fim <= data_inicio:
                    raise ValueError('Data de fim da inscrição deve ser posterior à data de início')
            
            return v
        except ValueError as e:
            if 'does not match format' in str(e) or 'time data' in str(e):
                raise ValueError('Data de fim da inscrição deve estar no formato AAAA-MM-DD')
            raise e
    
    @field_validator('data_inicio_vigencia')
    @classmethod
    def validar_data_inicio_vigencia(cls, v):
        if not v:
            raise ValueError('Data de início da vigência é obrigatória')
        
        try:
            # Validar formato da data
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Data de início da vigência deve estar no formato AAAA-MM-DD')
    
    @field_validator('data_fim_vigencia')
    @classmethod
    def validar_data_fim_vigencia(cls, v, info):
        if not v:
            raise ValueError('Data de fim da vigência é obrigatória')
        
        try:
            # Validar formato da data
            data_fim = datetime.strptime(v, '%Y-%m-%d')
            
            # Validar se é posterior à data de início
            if 'data_inicio_vigencia' in info.data:
                data_inicio = datetime.strptime(info.data['data_inicio_vigencia'], '%Y-%m-%d')
                if data_fim <= data_inicio:
                    raise ValueError('Data de fim da vigência deve ser posterior à data de início')
            
            return v
        except ValueError as e:
            if 'does not match format' in str(e) or 'time data' in str(e):
                raise ValueError('Data de fim da vigência deve estar no formato AAAA-MM-DD')
            raise e
    
    @field_validator('status')
    @classmethod
    def validar_status(cls, v):
        if v and v not in ['ativo', 'inativo']:
            raise ValueError('Status deve ser "ativo" ou "inativo"')
        return v or 'ativo'
    