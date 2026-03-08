from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Dados que o seu index.html (linha 53) está pedindo
    info = {
        "usuario": "Danilo",
        "saldo": "R$ 0,00",
        "milhas": "0",
        "status": "Ativo"
    }
    
    # Dados para o gráfico não travar o site
    meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"]
    dados = [0, 0, 0, 0, 0, 0]
    
    return render_template('index.html', info=info, meses=meses, dados=dados)

if __name__ == '__main__':
    # Configuração de porta para o Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)



