from database import db
from flask_login import UserMixin

# --- Association Table para M:M Receita <-> Ingrediente ---
class ReceitaIngrediente(db.Model):
    __tablename__ = 'receita_ingredientes'
    receita_id = db.Column(db.Integer, db.ForeignKey('receita.id'), primary_key=True)
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingrediente.id'), primary_key=True)
    quantidade = db.Column(db.String(50), nullable=False)

    # Relações de volta
    receita = db.relationship('Receita', back_populates='ingredientes_associados')
    ingrediente = db.relationship('Ingrediente', back_populates='receitas_associadas')


# --- Usuário ---
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    # Relação 1:1 com Chef
    chef = db.relationship('Chef', back_populates='usuario', uselist=False)


# --- Chef ---
class Chef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especialidade = db.Column(db.String(100))

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False, unique=True)
    usuario = db.relationship('Usuario', back_populates='chef')

    # Relação 1:N com Receita
    receitas = db.relationship('Receita', back_populates='chef')


# --- Receita ---
class Receita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    instrucoes = db.Column(db.Text, nullable=False)

    chef_id = db.Column(db.Integer, db.ForeignKey('chef.id'), nullable=False)
    chef = db.relationship('Chef', back_populates='receitas')

    # Relação M:M com Ingredientes
    ingredientes_associados = db.relationship('ReceitaIngrediente', back_populates='receita', cascade='all, delete-orphan')


# --- Ingrediente ---
class Ingrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)

    receitas_associadas = db.relationship('ReceitaIngrediente', back_populates='ingrediente', cascade='all, delete-orphan')
