"""
Script de migração para atualizar a tabela auxilio_transporte
Adiciona novos campos e remove campos antigos
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from util.db_util import get_connection

def migrar_auxilio_transporte():
    """Migra a tabela auxilio_transporte para a nova estrutura"""
    
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Verificar se a tabela existe
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auxilio_transporte'")
            if not cursor.fetchone():
                print("⚠️  Tabela auxilio_transporte não existe. Criando nova tabela...")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS auxilio_transporte (
                        id_auxilio_transporte INTEGER PRIMARY KEY,
                        tipo_transporte TEXT NOT NULL,
                        tipo_onibus TEXT,
                        gasto_passagens_dia REAL,
                        gasto_van_mensal REAL,
                        urlCompResidencia TEXT,
                        urlPasseEscolarFrente TEXT,
                        urlPasseEscolarVerso TEXT,
                        urlComprovanteRecarga TEXT,
                        urlComprovantePassagens TEXT,
                        urlContratoTransporte TEXT,
                        FOREIGN KEY (id_auxilio_transporte) REFERENCES auxilio(id_auxilio) ON DELETE CASCADE
                    )
                """)
                conn.commit()
                print("✅ Tabela auxilio_transporte criada com sucesso!")
                return True
            
            # Verificar colunas existentes
            cursor.execute("PRAGMA table_info(auxilio_transporte)")
            colunas_existentes = {row[1] for row in cursor.fetchall()}
            
            print(f"Colunas existentes: {colunas_existentes}")
            
            # Se já tem as novas colunas, não precisa migrar
            novas_colunas = {'tipo_transporte', 'tipo_onibus', 'gasto_passagens_dia', 'gasto_van_mensal'}
            if novas_colunas.issubset(colunas_existentes):
                print("✅ Tabela já está atualizada!")
                return True
            
            # Fazer backup dos dados existentes
            print("\n📦 Fazendo backup dos dados existentes...")
            cursor.execute("SELECT * FROM auxilio_transporte")
            dados_antigos = cursor.fetchall()
            print(f"   {len(dados_antigos)} registros encontrados")
            
            # Renomear tabela antiga
            print("\n🔄 Renomeando tabela antiga...")
            cursor.execute("ALTER TABLE auxilio_transporte RENAME TO auxilio_transporte_old")
            
            # Criar nova tabela com estrutura atualizada
            print("🆕 Criando nova tabela...")
            cursor.execute("""
                CREATE TABLE auxilio_transporte (
                    id_auxilio_transporte INTEGER PRIMARY KEY,
                    tipo_transporte TEXT NOT NULL,
                    tipo_onibus TEXT,
                    gasto_passagens_dia REAL,
                    gasto_van_mensal REAL,
                    urlCompResidencia TEXT,
                    urlPasseEscolarFrente TEXT,
                    urlPasseEscolarVerso TEXT,
                    urlComprovanteRecarga TEXT,
                    urlComprovantePassagens TEXT,
                    urlContratoTransporte TEXT,
                    FOREIGN KEY (id_auxilio_transporte) REFERENCES auxilio(id_auxilio) ON DELETE CASCADE
                )
            """)
            
            # Migrar dados antigos se existirem
            if dados_antigos:
                print(f"\n💾 Migrando {len(dados_antigos)} registros...")
                for row in dados_antigos:
                    # row[0] = id_auxilio_transporte
                    # row[1] = urlCompResidencia (antigo)
                    # row[2] = urlCompTransporte (antigo)
                    cursor.execute("""
                        INSERT INTO auxilio_transporte (
                            id_auxilio_transporte,
                            tipo_transporte,
                            tipo_onibus,
                            gasto_passagens_dia,
                            gasto_van_mensal,
                            urlCompResidencia,
                            urlPasseEscolarFrente,
                            urlPasseEscolarVerso,
                            urlComprovanteRecarga,
                            urlComprovantePassagens,
                            urlContratoTransporte
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        row[0],  # id_auxilio_transporte
                        'onibus',  # tipo_transporte (valor padrão)
                        None,  # tipo_onibus
                        None,  # gasto_passagens_dia
                        None,  # gasto_van_mensal
                        row[1] if len(row) > 1 else None,  # urlCompResidencia (do backup)
                        None,  # urlPasseEscolarFrente
                        None,  # urlPasseEscolarVerso
                        None,  # urlComprovanteRecarga
                        row[2] if len(row) > 2 else None,  # urlComprovantePassagens (do backup)
                        None   # urlContratoTransporte
                    ))
                print(f"   ✓ {len(dados_antigos)} registros migrados")
            
            # Remover tabela antiga
            print("\n🗑️  Removendo tabela antiga...")
            cursor.execute("DROP TABLE auxilio_transporte_old")
            
            conn.commit()
            print("\n✅ Migração concluída com sucesso!")
            print("\n📊 Nova estrutura da tabela:")
            cursor.execute("PRAGMA table_info(auxilio_transporte)")
            for col in cursor.fetchall():
                print(f"   - {col[1]} ({col[2]})")
            
            return True
            
    except Exception as e:
        print(f"\n❌ Erro na migração: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("MIGRAÇÃO DA TABELA AUXILIO_TRANSPORTE")
    print("=" * 70)
    print("\nAtualizando estrutura para incluir novos campos do formulário...\n")
    
    migrar_auxilio_transporte()
