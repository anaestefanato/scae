import traceback
import sys
sys.path.insert(0, '.')

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

try:
    # Fazer login
    response = client.post("/login", data={
        "matricula": "admin123",
        "senha": "admin123"
    }, follow_redirects=False)
    
    print(f"Login Status: {response.status_code}")
    print(f"Redirect: {response.headers.get('location', 'N/A')}")
    
    # Tentar acessar página admin
    cookies = response.cookies
    response2 = client.get("/admin/inicio", cookies=cookies)
    
    print(f"\nAdmin page Status: {response2.status_code}")
    if response2.status_code != 200:
        print(f"Error content: {response2.text[:500]}")
    
except Exception as e:
    print(f"Erro: {e}")
    traceback.print_exc()
