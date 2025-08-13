from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tarefas = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        tarefa = request.form["tarefa"]
        data_limite = request.form["data_limite"]
        tarefas.append({"tarefa":tarefa, "data":data_limite})
        return redirect(url_for("sucesso", nome_tarefa=tarefa))
    return render_template("index.html", tarefas=tarefas)

@app.route("/sucesso")
def sucesso():
    nome_tarefa = request.args.get("nome_tarefa")
    return render_template("sucesso.html", nome_tarefa=nome_tarefa)

if __name__ == "__main__":
    app.run(debug=True)