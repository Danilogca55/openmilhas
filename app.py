from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Criamos o objeto 'info' para o HTML não dar erro 500
    info = {
        "usuario": "Danilo"
    }
    return render_template('index.html', info=info)

if __name__ == '__main__':
    # Configuração necessária para o Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


