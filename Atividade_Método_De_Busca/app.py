from flask import Flask, request, render_template_string
from flask_sqlalchemy import SQLAlchemy
import os

# --- Configuração do app ---
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# --- Modelo ---
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_nome = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"<Usuario {self.usuario_nome}>"

@app.cli.command("init-db")
def init_db_command():
    """Cria tabelas e popula com dados de exemplo"""
    db.drop_all()
    db.create_all()
    db.session.add_all([
        Usuario(usuario_nome="Ellen"),
        Usuario(usuario_nome="Amanda"),
        Usuario(usuario_nome="Carlos"),
        Usuario(usuario_nome="Marina"),
        Usuario(usuario_nome="João"),
    ])
    db.session.commit()
    print("Banco de dados inicializado com sucesso!")

# --- Rota inicial ---
@app.route("/")
def index():
    return """
    <h2>Busque usuários</h2>
    <form action="/buscar_usuario">
        <input type="text" name="q" placeholder="Digite uma letra ou nome">
        <button type="submit">Buscar</button>
    </form>
    """

# --- Rota de busca ---
@app.route("/buscar_usuario")
def buscar_usuario():
    termo = request.args.get("q", "").strip()
    if not termo:
        return "<p>Digite algo para buscar.</p>"

    resultados = Usuario.query.filter(Usuario.usuario_nome.ilike(f"%{termo}%")).all()

    # Render simples usando render_template_string
    html = "<h2>Resultados da busca por '{}'</h2>".format(termo)
    if resultados:
        html += "<ul>"
        for u in resultados:
            html += f"<li>{u.usuario_nome}</li>"
        html += "</ul>"
    else:
        html += "<p>Nenhum usuário encontrado.</p>"

    html += '<a href="/">Voltar</a>'
    return render_template_string(html)

# --- Executar app ---
if __name__ == "__main__":
    app.run(debug=True)