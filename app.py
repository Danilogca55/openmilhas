from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Carrega o formulário de cadastro diretamente
    return render_template('index.html')

@app.route('/executar_script', methods=['POST'])
def executar_script():
    # Aqui você pode adicionar a lógica para salvar os dados no futuro
    return "Dados recebidos com sucesso! Seu cadastro está em análise."

if __name__ == '__main__':
    app.run(debug=True)


