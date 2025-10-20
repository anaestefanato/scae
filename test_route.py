import requests

# Fazer login como aluno
login_data = {
    'matricula': 'aluno123',
    'senha': 'aluno123'
}

session = requests.Session()

# Login
try:
    response = session.post('http://127.0.0.1:8000/login', data=login_data, allow_redirects=False)
    print(f"Login status: {response.status_code}")
    print(f"Cookies: {session.cookies}")
    
    # Acessar página de acompanhar inscrições
    response2 = session.get('http://127.0.0.1:8000/aluno/acompanhar-inscricoes')
    print(f"\n Acompanhar inscrições status: {response2.status_code}")
    if response2.status_code != 200:
        print(f"Error: {response2.text}")
except Exception as e:
    print(f"Erro: {e}")
    import traceback
    traceback.print_exc()
