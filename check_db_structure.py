import sqlite3

conn = sqlite3.connect('dados.db')
cursor = conn.cursor()

# Check aluno table structure
cursor.execute('PRAGMA table_info(aluno)')
columns = cursor.fetchall()
print('Aluno table columns:')
for col in columns:
    print(f'  {col[1]} ({col[2]})')

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('\nAll tables:')
for table in tables:
    print(f'  {table[0]}')

conn.close()
