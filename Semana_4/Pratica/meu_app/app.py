from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-dificil-de-adivinhar'


# ------------------- FORMULÁRIO SIMPLES -------------------
class MeuFormulario(FlaskForm):
    nome = StringField(
        'Nome Completo',
        validators=[DataRequired(message="Este campo é obrigatório.")]
    )
    email = StringField(
        'Seu Melhor E-mail',
        validators=[
            DataRequired(message="Este campo é obrigatório."),
            Email(message="Por favor, insira um e-mail válido.")
        ]
    )
    submit = SubmitField('Enviar Cadastro')


# ------------------- FORMULÁRIO AVANÇADO DE REGISTRO -------------------
class FormularioRegistro(FlaskForm):
    nome = StringField(
        'Nome Completo',
        validators=[DataRequired(message="Informe seu nome completo.")]
    )
    email = StringField(
        'E-mail',
        validators=[DataRequired(), Email(message="E-mail inválido.")]
    )
    senha = PasswordField(
        'Senha',
        validators=[
            DataRequired(message="Informe uma senha."),
            Length(min=8, message="A senha deve ter pelo menos 8 caracteres.")
        ]
    )
    confirmar_senha = PasswordField(
        'Confirmar Senha',
        validators=[
            DataRequired(message="Confirme sua senha."),
            EqualTo('senha', message="As senhas devem coincidir.")
        ]
    )
    biografia = TextAreaField('Biografia (opcional)')
    aceitar_termos = BooleanField(
        'Aceito os termos de serviço',
        validators=[DataRequired(message="Você deve aceitar os termos para prosseguir.")]
    )
    submit = SubmitField('Registrar')


# ------------------- ROTAS -------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    form = MeuFormulario()
    if form.validate_on_submit():
        nome_usuario = form.nome.data
        email_usuario = form.email.data
        flash(f'Cadastro recebido com sucesso para {nome_usuario} ({email_usuario})!', 'success')
        return redirect(url_for('formulario'))
    return render_template('formulario.html', form=form)


@app.route('/formulario/preenchido-args', methods=['GET', 'POST'])
def formulario_com_argumentos():
    form = MeuFormulario(nome="Fulano de Tal", email="fulano@exemplo.com")
    if form.validate_on_submit():
        flash(f'Dados de "{form.nome.data}" atualizados com sucesso!', 'success')
        return redirect(url_for('formulario_com_argumentos'))
    return render_template('formulario.html', form=form)


@app.route('/formulario/preenchido-obj', methods=['GET', 'POST'])
def formulario_com_objeto():
    class UsuarioMock:
        def __init__(self, nome, email):
            self.nome = nome
            self.email = email

    usuario_do_banco = UsuarioMock(nome="Ciclano da Silva", email="ciclano@banco.com")
    form = MeuFormulario(obj=usuario_do_banco)
    if form.validate_on_submit():
        flash(f'Dados de "{form.nome.data}" atualizados com sucesso!', 'success')
        return redirect(url_for('formulario_com_objeto'))
    return render_template('formulario.html', form=form)


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = FormularioRegistro()
    if form.validate_on_submit():
        nome = form.nome.data
        bio = form.biografia.data
        msg = f"Bem-vindo(a), {nome}!"
        if bio:
            msg += f" Sua biografia: {bio[:50]}..."
        flash(msg, 'success')
        return redirect(url_for('registro'))
    return render_template('registro.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
