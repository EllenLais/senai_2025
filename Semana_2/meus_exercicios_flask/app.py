
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/bemvindo')
def exercicio1():
    nome_usuario = "Maria"
    return render_template('exercicio1.html', nome_usuario=nome_usuario)

@app.route('/cursos')
def exercicio2():
    lista_de_cursos = [
        "Desenvolvimento Web com Flask",
        "Python para Análise de Dados",
        "Introdução a Machine Learning",
        "Banco de Dados SQL"
    ]
    return render_template('exercicio2.html', cursos=lista_de_cursos)

@app.route('/perfil/<nome>')
@app.route('/perfil')
def exercicio3(nome=None):
    logado = nome is not None
    return render_template('exercicio3.html', usuario_logado=logado,
    nome_usuario=nome)

@app.route('/sobre')
def exercicio4():
    return render_template('sobre.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)