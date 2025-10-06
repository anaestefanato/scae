from pydantic import BaseModel, field_validator


class LoginDTO(BaseModel):
    matricula: str
    senha: str
    
    @field_validator('matricula')
    def validate_matricula(cls, v):
        if len(v) < 5:
            raise ValueError('Matrícula deve ter pelo menos 5 caracteres.')
        return v

    @field_validator('senha')
    def validate_senha(cls, v):
        if len(v) < 6:
            raise ValueError('Senha deve ter pelo menos 6 caracteres.')
        return v