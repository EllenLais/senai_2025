# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Inicializa a aplicação Flask
app = Flask(__name__)

# Chave secreta para segurança das sessões e formulários
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'

# Configuração do Banco de Dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estante.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa a extensão do banco de dados com a aplicação
db = SQLAlchemy(app)

# --- Modelos ---
class Autor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), unique=True, nullable=False)
    livros = db.relationship('Livro', backref='autor', lazy=True)

    def __repr__(self):
        return f'<Autor {self.nome}>'

class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    ano_publicacao = db.Column(db.Integer, nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey('autor.id'), nullable=False)

    def __repr__(self):
        return f'<Livro {self.titulo}>'

# --- Rotas ---
@app.route('/autores', methods=['GET', 'POST'])
def autores():
    if request.method == 'POST':
        nome = request.form['nome']
        if nome:
            novo_autor = Autor(nome=nome)
            db.session.add(novo_autor)
            db.session.commit()
            flash("Autor cadastrado com sucesso!", "success")
        return redirect(url_for('autores'))

    todos_autores = Autor.query.all()
    return render_template('autores.html', autores=todos_autores)

@app.route('/', methods=['GET', 'POST'])
@app.route('/livros', methods=['GET', 'POST'])
def livros():
    if request.method == 'POST':
        titulo = request.form['titulo']
        ano_publicacao = request.form['ano_publicacao']
        autor_id = request.form['autor_id']

        if titulo and ano_publicacao and autor_id:
            novo_livro = Livro(
                titulo=titulo,
                ano_publicacao=int(ano_publicacao),
                autor_id=int(autor_id)
            )
            db.session.add(novo_livro)
            db.session.commit()
            flash("Livro cadastrado com sucesso!", "success")
        return redirect(url_for('livros'))

    todos_livros = Livro.query.all()
    todos_autores = Autor.query.all()
    return render_template('livros.html', livros=todos_livros, autores=todos_autores)

# --- Criação do banco ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001, debug=True)
