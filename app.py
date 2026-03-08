from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Tenta carregar o index.html da pasta templates
    return render_template('index.html')

if __name__ == '__main__':
    # O Render usa a variável de ambiente PORT, isso evita o erro 502
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

