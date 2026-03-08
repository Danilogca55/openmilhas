from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = 'chave_open_milhas_2026'

# Configuração de Acesso (Usuário: admin | Senha: 1234)
USER_DB = {"admin": "1234"}

def carregar_dados_reais():
    """Lê as informações do arquivo de dados na pasta do projeto"""
    # Usamos o caminho relativo para funcionar no servidor do Render
    caminho_arquivo = os.path.join(os.path.dirname(__file__), 'dados_bancarios')
    dados = {
        "usuario": "Danilo",
        "saldo_milhas": "0",
        "lucro_estimado": "0,00",
        "status": "Bronze"
    }
    try:
        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
                if len(linhas) >= 2:
                    dados["saldo_milhas"] = linhas[0].strip()
                    dados["lucro_estimado"] = linhas[1].strip()
                    dados["status"] = "Executive Gold"
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
    return dados

@app.route('/')
def home():
    info = carregar_dados_reais()
    return render_template('index.html', info=info)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username in USER_DB and USER_DB[username] == password:
        return redirect(url_for('dashboard'))
    return "Erro: Usuário ou senha inválidos. Volte e tente novamente."

@app.route('/dashboard')
def dashboard():
    info = carregar_dados_reais()
    # Dados para o gráfico de barras
    lucros_mensais = [5000, 8500, 12000, 18000, 22500] 
    meses = ["Nov", "Dez", "Jan", "Fev", "Mar"]
    return render_template('index.html', info=info, lucros=lucros_mensais, meses=meses)

@app.route('/vendas')
def vendas():
    # Corrigido: Fechando as aspas e o parêntese para evitar o erro de Status 1
    return render_template('vendas.html')

@app.route('/executar_script', methods=['POST'])
def executar_script():
    # Rota para o botão de automação
    print("Iniciando script de coleta...")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    # O Render gerencia a porta automaticamente
    app.run(debug=True)

