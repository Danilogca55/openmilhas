from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Criamos um "info" básico para o site não travar ao carregar o HTML
    info = {
        "usuario": "Danilo"
    }
    return render_template('index.html', info=info)

if __name__ == '__main__':
    # Configuração obrigatória para o Render não dar erro 500
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


