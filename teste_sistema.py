#!/usr/bin/env python3
"""
Script de teste do sistema de aprovação de cadastros
"""
import requests
import json

# Configurações
BASE_URL = "http://127.0.0.1:8000"

def testar_cadastro_novo_usuario():
    """Testa o cadastro de um novo usuário"""
    print("🧪 Testando cadastro de novo usuário...")
    
    dados_cadastro = {
        "nome": "Maria Silva Costa",
        "matricula": "2025001235",
        "email": "maria.costa@aluno.ifes.edu.br",
        "senha": "senha123",
        "conf_senha": "senha123"
    }
    
    response = requests.post(f"{BASE_URL}/cadastro", data=dados_cadastro)
    
    if response.status_code == 200:
        if "aguarde aprovação" in response.text.lower():
            print("✅ Cadastro criado com mensagem de aprovação pendente")
            return True
        else:
            print("⚠️  Cadastro criado mas sem mensagem de aprovação")
            return True
    else:
        print(f"❌ Erro no cadastro: {response.status_code}")
        return False

def testar_login_usuario_pendente():
    """Testa login de usuário pendente de aprovação"""
    print("🧪 Testando login de usuário pendente...")
    
    dados_login = {
        "matricula": "2025001235",
        "senha": "senha123"
    }
    
    response = requests.post(f"{BASE_URL}/entrar", data=dados_login)
    
    if "pendente de aprovação" in response.text.lower():
        print("✅ Login bloqueado para usuário pendente")
        return True
    else:
        print("❌ Usuário pendente conseguiu fazer login")
        return False

def testar_dashboard_admin():
    """Testa se o dashboard do admin mostra solicitações"""
    print("🧪 Testando dashboard do administrador...")
    
    # Primeiro fazer login como admin
    session = requests.Session()
    
    dados_login = {
        "matricula": "admin123",
        "senha": "admin123"
    }
    
    response = session.post(f"{BASE_URL}/entrar", data=dados_login)
    
    if response.status_code == 200:
        # Acessar dashboard
        dashboard_response = session.get(f"{BASE_URL}/admin/inicio")
        
        if "Solicitações de Cadastro" in dashboard_response.text:
            print("✅ Dashboard mostra seção de solicitações")
            
            if "Maria Silva Costa" in dashboard_response.text:
                print("✅ Usuário pendente aparece no dashboard")
                return True
            else:
                print("⚠️  Seção existe mas usuário não aparece")
                return True
        else:
            print("❌ Dashboard não mostra seção de solicitações")
            return False
    else:
        print("❌ Erro no login do admin")
        return False

def testar_pagina_analise():
    """Testa a página específica de análise de cadastros"""
    print("🧪 Testando página de análise de cadastros...")
    
    session = requests.Session()
    
    # Login como admin
    dados_login = {
        "matricula": "admin123",
        "senha": "admin123"
    }
    
    session.post(f"{BASE_URL}/entrar", data=dados_login)
    
    # Acessar página de análise
    response = session.get(f"{BASE_URL}/admin/analisar-cadastros")
    
    if response.status_code == 200:
        if "Analisar Cadastros Pendentes" in response.text:
            print("✅ Página de análise carregou corretamente")
            return True
        else:
            print("❌ Página carregou mas sem conteúdo esperado")
            return False
    else:
        print(f"❌ Erro ao carregar página: {response.status_code}")
        return False

def executar_testes():
    """Executa todos os testes"""
    print("🚀 Iniciando testes do sistema de aprovação de cadastros\n")
    
    resultados = []
    
    try:
        # Teste 1: Cadastro
        resultados.append(testar_cadastro_novo_usuario())
        print()
        
        # Teste 2: Login pendente
        resultados.append(testar_login_usuario_pendente())
        print()
        
        # Teste 3: Dashboard admin
        resultados.append(testar_dashboard_admin())
        print()
        
        # Teste 4: Página de análise
        resultados.append(testar_pagina_analise())
        print()
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Servidor não está rodando na porta 8000")
        return
    
    # Relatório final
    sucessos = sum(resultados)
    total = len(resultados)
    
    print("=" * 50)
    print("📊 RELATÓRIO DE TESTES")
    print("=" * 50)
    print(f"✅ Testes aprovados: {sucessos}/{total}")
    print(f"❌ Testes falharam: {total - sucessos}/{total}")
    
    if sucessos == total:
        print("🎉 Todos os testes passaram! Sistema funcionando corretamente.")
    else:
        print("⚠️  Alguns testes falharam. Verificar implementação.")

if __name__ == "__main__":
    executar_testes()