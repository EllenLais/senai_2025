from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/",methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        return render_template("sucesso.html", nome=nome, email=email, senha=senha)
    
    return render_template("cadastro.html")

if __name__ == "__main__":
    app.run(debug=True)