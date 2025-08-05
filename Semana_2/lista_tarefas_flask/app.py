from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tarefas = [
    {'id': 1, 'descricao': 'Estudar os conceitos de rotas no Flask', 'concluida': True},
    {'id': 2, 'descricao': 'Criar o formulário de adição de tarefas', 'concluida': False}
]
proximo_id = 3

@app.route('/')
def index():
    return render_template('index.html', tarefas=tarefas)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    global proximo_id
    descricao = request.form['descricao']
    nova_tarefa = {
        'id': proximo_id,
        'descricao': descricao,
        'concluida': False
    }
    tarefas.append(nova_tarefa)
    proximo_id += 1
    return redirect(url_for('index'))

@app.route('/alternar/<int:id_da_tarefa>', methods=['POST'])
def alternar(id_da_tarefa):
    for tarefa in tarefas:
        if tarefa['id'] == id_da_tarefa:
            tarefa['concluida'] = not tarefa['concluida']
            break
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)