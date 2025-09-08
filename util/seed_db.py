# criar_admin.py
from model.administrador_model import Administrador
from model.aluno_model import Aluno
from util.security import criar_hash_senha
from repo import usuario_repo
from model.usuario_model import Usuario

def criar_admin_padrao():
    # Verificar se já existe admin
    admins = usuario_repo.obter_todos_por_perfil("admin")
    if not admins:
        senha_hash = criar_hash_senha("admin123")
        admin = Administrador(
            id_usuario=0,
            nome="Administrador",
            email="admin@admin.com",
            senha=senha_hash,
            perfil="admin",
            matricula="admin123",
            tipo_usuario="admin"
        )
        id_usuario = usuario_repo.inserir(admin)        
        print("Admin criado: admin@admin.com / admin123")
        
        
def criar_aluno_padrao():
    # Verificar se já existe aluno
    alunos = usuario_repo.obter_todos_por_perfil("aluno")
    if not alunos:
        senha_hash = criar_hash_senha("aluno123")
        aluno = Aluno(
            id_usuario=0,
            nome="Aluno Padrão",
            email="aluno@aluno.com",
            senha=senha_hash,
            perfil="aluno",
            matricula="aluno123",
            tipo_usuario="aluno",
            cpf="000.000.000-00",
            rg="00.000.000-0",
            telefone="(00) 00000-0000",
            curso="Curso Exemplo",
            data_nascimento="2000-01-01",
            filiacao="Nome do Pai e Nome da Mãe",
            endereco="Rua Exemplo, 123, Cidade, Estado",
            nome_banco="Banco Exemplo",
            agencia_bancaria="0001",
            numero_conta_bancaria="12345-6",
            renda_familiar=6000.00,
            quantidade_pessoas=4
        )
        id_usuario = usuario_repo.inserir(aluno)
        print("Aluno criado: aluno@aluno.com / aluno123")


if __name__ == "__main__":
    criar_admin_padrao()            
    criar_aluno_padrao()