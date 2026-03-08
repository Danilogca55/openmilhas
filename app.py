from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Dados do usuário para o topo da página
    info = {
        "usuario": "Danilo",
        "saldo": "R$ 0,00",
        "milhas": "0",
        "status": "Ativo"
    }
    
    # LISTA DE VARIÁVEIS PARA O GRÁFICO (Linha 102 do seu HTML)
    meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"]
    dados = [0, 0, 0, 0, 0, 0]
    lucros = [0, 0, 0, 0, 0, 0] # ESTA LINHA RESOLVE O ERRO ATUAL
    
    return render_template('index.html', info=info, meses=meses, dados=dados, lucros=lucros)

if __name__ == '__main__':
    # Garante que o Render use a porta correta
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

