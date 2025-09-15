from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Tabela de associação para relação M:M entre Receita e Ingrediente
receita_ingredientes = db.Table('receita_ingredientes',
    db.Column('receita_id', db.Integer, db.ForeignKey('receita.id'), primary_key=True),
    db.Column('ingrediente_id', db.Integer, db.ForeignKey('ingrediente.id'), primary_key=True),
    db.Column('quantidade', db.String(100))
)

class Chef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    perfil = db.relationship('PerfilChef', backref='chef', uselist=False)
    receitas = db.relationship('Receita', backref='chef', lazy=True)

class PerfilChef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    especialidade = db.Column(db.String(100))
    anos_experiencia = db.Column(db.Integer)
    chef_id = db.Column(db.Integer, db.ForeignKey('chef.id'), unique=True)

class Receita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    instrucoes = db.Column(db.Text, nullable=False)
    chef_id = db.Column(db.Integer, db.ForeignKey('chef.id'), nullable=False)
    ingredientes = db.relationship('Ingrediente', secondary=receita_ingredientes, 
                                  backref=db.backref('receitas', lazy=True))

class Ingrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)