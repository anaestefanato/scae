from pydantic import BaseModel, EmailStr, Field, field_validator


class CadastroAdminDTO(BaseModel):
    """DTO para cadastro de administrador"""
    nome: str 
    matricula: str 
    email: str 
    senha: str 
    tipo_admin: str 
    
    @field_validator('matricula')
    @classmethod
    def validar_matricula(cls, v):
        if len(v) < 4:
            raise ValueError('Matrícula deve ter no mínimo 4 caracteres')
        return v
    
    @field_validator('email')
    @classmethod
    def validar_email(cls, v):
        if '@' not in v or '.' not in v.split('@')[-1]:
            raise ValueError('E-mail deve ser um endereço de e-mail válido')
        return v
    
    @field_validator('senha')
    @classmethod
    def validar_senha(cls, v):
        if len(v) < 6:
            raise ValueError('Senha deve ter no mínimo 8 caracteres')
        return v
    
    