from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Isso vai abrir o formulário de cadastro que criamos
    return render_template('index.html')

if __name__ == '__main__':
    # Configuração obrigatória para o Render não dar erro 500
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

