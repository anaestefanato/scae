from pydantic import BaseModel, EmailStr, Field, field_validator


class CadastroUsuarioDTO(BaseModel):
    """DTO para cadastro de usuário"""
    nome: str = Field(..., min_length=3, max_length=100)
    matricula: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    senha: str = Field(..., min_length=6)
    conf_senha : str = Field(..., min_length=6)
    

    @field_validator('senha')
    @classmethod
    def validar_senha_forte(cls, v):
        if len(v) < 6:
            raise ValueError('Senha deve ter no mínimo 6 caracteres')
        if not any(c.isdigit() for c in v):
            raise ValueError('Senha deve conter pelo menos um número')
        return v

    @field_validator('conf_senha')
    @classmethod
    def senhas_devem_coincidir(cls, v, info):
        if 'senha' in info.data and v != info.data['senha']:
            raise ValueError('As senhas não coincidem')
        return v