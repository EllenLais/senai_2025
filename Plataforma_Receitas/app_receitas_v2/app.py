import os
from flask import Flask, render_template, request, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from database import db
from models import Usuario, Chef, Receita, Ingrediente, ReceitaIngrediente

# --- Configuração inicial ---
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-dificil-de-adivinhar'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'receitas.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Cria a pasta 'instance' se não existir
instance_path = os.path.join(basedir, 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

# --- Extensões ---
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Por favor, faça login para acessar esta página."
login_manager.login_message_category = "info"

# --- Configuração do Flask-Login ---
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# --- Rotas ---
@app.route('/')
def index():
    receitas = Receita.query.all()
    return render_template('index.html', receitas=receitas)


@app.route("/login", methods=['GET', 'POST'])
def login():
    from forms import LoginForm
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    from forms import RegistrationForm
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        novo_usuario = Usuario(email=form.email.data, password_hash=hashed_password)
        novo_chef = Chef(nome=form.nome.data, especialidade=form.especialidade.data, usuario=novo_usuario)
        db.session.add_all([novo_usuario, novo_chef])
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('cadastro.html', form=form)


@app.route('/receita/nova', methods=['GET', 'POST'])
@login_required
def criar_receita():
    if not current_user.chef:
        return "Apenas chefs podem criar receitas.", 403

    if request.method == 'POST':
        titulo = request.form['titulo']
        instrucoes = request.form['instrucoes']

        receita = Receita(titulo=titulo, instrucoes=instrucoes, chef=current_user.chef)
        db.session.add(receita)

        ingredientes_str = request.form['ingredientes']
        for par in [p.strip() for p in ingredientes_str.split(',') if p.strip()]:
            if ':' in par:
                nome, qtd = par.split(':', 1)
                nome = nome.strip().lower()
                qtd = qtd.strip()
                ingrediente = Ingrediente.query.filter_by(nome=nome).first()
                if not ingrediente:
                    ingrediente = Ingrediente(nome=nome)
                    db.session.add(ingrediente)
                db.session.add(ReceitaIngrediente(receita=receita, ingrediente=ingrediente, quantidade=qtd))

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('criar_receita.html')


@app.route('/chef/<int:chef_id>')
def detalhes_chef(chef_id):
    chef = Chef.query.get_or_404(chef_id)
    return render_template('detalhes_chef.html', chef=chef)


# --- Comando CLI init-db ---
@app.cli.command('init-db')
def init_db_command():
    """Cria tabelas e popula com dados de exemplo"""
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Usuários e chefs
        user1 = Usuario(email='ana@example.com', password_hash=bcrypt.generate_password_hash('senha123').decode('utf-8'))
        user2 = Usuario(email='erick@exemplo.com', password_hash=bcrypt.generate_password_hash('123').decode('utf-8'))

        chef1 = Chef(nome='Ana Maria', especialidade='Culinária Brasileira', usuario=user1)
        chef2 = Chef(nome='Érick Jacquin', especialidade='Culinária Francesa', usuario=user2)

        db.session.add_all([user1, user2, chef1, chef2])
        db.session.commit()

        # Ingredientes
        ingredientes = {
            'tomate': Ingrediente(nome='tomate'),
            'cebola': Ingrediente(nome='cebola'),
            'farinha': Ingrediente(nome='farinha'),
            'ovo': Ingrediente(nome='ovo'),
            'manteiga': Ingrediente(nome='manteiga')
        }
        db.session.add_all(ingredientes.values())
        db.session.commit()

        # Receitas
        receita1 = Receita(titulo='Molho de Tomate Clássico', instrucoes='Refogue tudo.', chef=chef1)
        receita2 = Receita(titulo='Bolo Simples', instrucoes='...', chef=chef2)
        receita3 = Receita(titulo='Petit Gâteau', instrucoes='...', chef=chef2)
        db.session.add_all([receita1, receita2, receita3])
        db.session.commit()

        # Associações Receita <-> Ingrediente
        db.session.add_all([
            ReceitaIngrediente(receita=receita1, ingrediente=ingredientes['tomate'], quantidade='5 unidades'),
            ReceitaIngrediente(receita=receita1, ingrediente=ingredientes['cebola'], quantidade='1 unidade'),
            ReceitaIngrediente(receita=receita2, ingrediente=ingredientes['farinha'], quantidade='2 xícaras'),
            ReceitaIngrediente(receita=receita2, ingrediente=ingredientes['ovo'], quantidade='3 unidades'),
            ReceitaIngrediente(receita=receita3, ingrediente=ingredientes['manteiga'], quantidade='150g')
        ])
        db.session.commit()

        print('Banco de dados inicializado com sucesso!')


if __name__ == '__main__':
    app.run(debug=True)
