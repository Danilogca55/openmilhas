from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Dados básicos para o site não quebrar
    info = {
        "usuario": "Danilo",
        "saldo": "R$ 0,00",
        "milhas": "0",
        "status": "Ativo"
    }
    # ESTAS DUAS LINHAS ABAIXO RESOLVEM O ERRO DO LOG:
    meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"]
    dados = [0, 0, 0, 0, 0, 0]
    
    return render_template('index.html', info=info, meses=meses, dados=dados)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)



