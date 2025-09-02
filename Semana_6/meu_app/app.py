# -*- coding: utf-8 -*-

# Passo 1: Importações e Configuração
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# Inicializa a aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Sua-Segurança-Mora-Aqui'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meuapp.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Usuario: {self.nome}>'
    
class Postagens(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    data_publicacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.template_filter("brasilia_datetime")
def brasilia_datetime(value):
    if value is None:
        return ""
    # Se não tiver timezone, assume UTC
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M")

# --- Rotas da Aplicação ---

# Rota principal que exibe o formulário e a lista de usuários
@app.route('/')
def index():
    usuarios = Usuario.query.all()
    return render_template('index.html', usuarios=usuarios)

@app.route('/adicionar', methods=['POST'])
def adicionar_usuario():
    nome = request.form['nome']
    email = request.form['email']

    novo_usuario = Usuario(nome=nome, email=email)

    db.session.add(novo_usuario)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/postagens')
def listar_postagens():
    postagens = Postagens.query.order_by(Postagens.data_publicacao.desc()).all()
    return render_template('postagens.html', postagens=postagens)

@app.route('/adicionar_postagem', methods=['POST'])
def adicionar_postagem():
    titulo = request.form['titulo']
    conteudo = request.form['conteudo']

    nova_postagem = Postagens(titulo=titulo, conteudo=conteudo)
    db.session.add(nova_postagem)
    db.session.commit()

    return redirect(url_for('listar_postagens'))

# Passo 3: Criando o Banco de Dados Físico
if __name__ == '__main__':
    with app.app_context():
        #db.drop_all()
        db.create_all()

    # Inicia o servidor de desenvolvimento do Flask
    app.run(host='0.0.0.0', port=5000, debug=True)


