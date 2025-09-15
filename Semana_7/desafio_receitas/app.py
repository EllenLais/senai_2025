from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Chef, PerfilChef, Receita, Ingrediente, receita_ingredientes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///receitas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'sua_chave_secreta_aqui'  # Necessário para flash messages

# Inicializar o banco de dados com o app
db.init_app(app)

@app.route('/')
def index():
    receitas = Receita.query.all()
    return render_template('index.html', receitas=receitas)

# Rota para cadastrar novo chef
@app.route('/chef/novo', methods=['GET', 'POST'])
def novo_chef():
    if request.method == 'POST':
        nome = request.form['nome']
        especialidade = request.form['especialidade']
        anos_experiencia = request.form['anos_experiencia']
        
        # Criar o chef
        novo_chef = Chef(nome=nome)
        db.session.add(novo_chef)
        db.session.commit()
        
        # Criar o perfil do chef
        perfil = PerfilChef(
            especialidade=especialidade,
            anos_experiencia=anos_experiencia,
            chef_id=novo_chef.id
        )
        db.session.add(perfil)
        db.session.commit()
        
        flash('Chef cadastrado com sucesso!', 'success')
        return redirect(url_for('index'))
    
    return render_template('novo_chef.html')

# Rota para listar chefs
@app.route('/chefs')
def listar_chefs():
    chefs = Chef.query.all()
    return render_template('chefs.html', chefs=chefs)

# Rota para cadastrar nova receita
@app.route('/receita/nova', methods=['GET', 'POST'])
def nova_receita():
    if request.method == 'POST':
        titulo = request.form['titulo']
        instrucoes = request.form['instrucoes']
        chef_id = request.form['chef_id']
        ingredientes_texto = request.form['ingredientes']
        
        # Criar a receita
        nova_receita = Receita(titulo=titulo, instrucoes=instrucoes, chef_id=chef_id)
        db.session.add(nova_receita)
        db.session.flush()  # Para obter o ID da receita antes do commit
        
        # Processar ingredientes
        ingredientes_lista = [ing.strip() for ing in ingredientes_texto.split(',')]
        for ing_nome in ingredientes_lista:
            if ing_nome:
                # Verificar se o ingrediente já existe
                ingrediente = Ingrediente.query.filter_by(nome=ing_nome).first()
                if not ingrediente:
                    ingrediente = Ingrediente(nome=ing_nome)
                    db.session.add(ingrediente)
                    db.session.flush()
                
                # Associar ingrediente à receita
                nova_receita.ingredientes.append(ingrediente)
        
        db.session.commit()
        flash('Receita cadastrada com sucesso!', 'success')
        return redirect(url_for('index'))
    
    chefs = Chef.query.all()
    return render_template('nova_receita.html', chefs=chefs)

# Rota para detalhes do chef
@app.route('/chef/<int:chef_id>')
def detalhes_chef(chef_id):
    chef = Chef.query.get_or_404(chef_id)
    return render_template('detalhes_chef.html', chef=chef)

# Rota para buscar por ingrediente
@app.route('/ingrediente/<string:nome_ingrediente>')
def buscar_por_ingrediente(nome_ingrediente):
    ingrediente = Ingrediente.query.filter_by(nome=nome_ingrediente).first_or_404()
    return render_template('buscar_ingrediente.html', ingrediente=ingrediente)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)