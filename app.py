from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Esta é a tela de cadastro inicial que fizemos no começo
    return render_template('cadastro.html')

@app.route('/login', methods=['POST'])
def login():
    # Após o cadastro, redireciona para a tela de vendas
    return redirect(url_for('vendas'))

@app.route('/vendas')
def vendas():
    # Tela de vendas de milhas com os dados corrigidos
    info = {
        "usuario": "Danilo",
        "saldo": "R$ 0,00",
        "milhas": "0",
        "status": "Aguardando Sincronização"
    }
    meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"]
    dados = [0, 0, 0, 0, 0, 0]
    lucros = [0, 0, 0, 0, 0, 0]
    return render_template('index.html', info=info, meses=meses, dados=dados, lucros=lucros)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)


