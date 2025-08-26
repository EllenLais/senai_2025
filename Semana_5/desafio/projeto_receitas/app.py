from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma-chave-secreta-facil-para-revisao'

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Formulário de nova receita
@app.route('/nova-receita', methods=['GET', 'POST'])
def nova_receita():
    errors = {}
    if request.method == 'POST':
        nome = request.form['nome']
        ingredientes = request.form['ingredientes']
        modo_preparo = request.form['modo_preparo']

        if not nome:
            errors['nome'] = 'O nome da receita é obrigatório.'
        if not ingredientes:
            errors['ingredientes'] = 'Os ingredientes são obrigatórios.'
        if not modo_preparo:
            errors['modo_preparo'] = 'O modo de preparo é obrigatório.'

        if errors:
            return render_template('nova_receita.html', errors=errors,
                                   nome=nome, ingredientes=ingredientes,
                                   modo_preparo=modo_preparo)

        session['receita'] = {
            'nome': nome,
            'ingredientes': ingredientes,
            'modo_preparo': modo_preparo
        }
        flash('Receita criada com sucesso!', 'success')
        return redirect(url_for('receita_criada'))

    return render_template('nova_receita.html', errors={})

# Página de receita criada
@app.route('/receita-criada')
def receita_criada():
    receita = session.get('receita')
    if not receita:
        flash('Nenhuma receita encontrada. Crie uma receita primeiro!', 'danger')
        return redirect(url_for('nova_receita'))
    return render_template('receita_criada.html', receita=receita)

# Executa a aplicação
if __name__ == '__main__':
    app.run(debug=True)
