from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Criamos um objeto 'info' completo para garantir que nenhum campo no HTML fique vazio e cause erro 500
    info = {
        "usuario": "Danilo",
        "saldo": "0,00",
        "milhas": "0",
        "status": "Ativo"
    }
    # Passamos o dicionário 'info' para o HTML
    return render_template('index.html', info=info)

if __name__ == '__main__':
    # Configuração de porta para o Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)



