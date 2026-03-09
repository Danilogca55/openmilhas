import os
from flask import Flask, render_template, request, redirect

# Configuração explícita do caminho das pastas
base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def index():
    # Tenta carregar o arquivo principal
    return render_template('cadastro.html')

@app.route('/login', methods=['POST'])
def login():
    # Captura simplificada para teste
    print(request.form)
    return redirect("https://www.google.com")

@app.route('/admin_painel_secreto_99')
def admin():
    return render_template('admin.html', usuarios=[])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)




