import os
import datetime
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Email, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

class EventoForm(FlaskForm):
    """Define os campos e validadores para o formulário de evento."""
    nome_evento = StringField(
        'Nome do Evento',
        validators=[DataRequired(message="O campo nome do evento é obrigatório.")]
    )
    data_evento = DateField(
        'Data do Evento',
        format='%Y-%m-%d',
        validators=[DataRequired(message="O campo data é obrigatório.")]
    )
    organizador = StringField(
        'Organizador',
        validators=[DataRequired(message="O campo organizador é obrigatório.")]
    )
    email = StringField(
        'E-mail',
        validators=[
            DataRequired(message="O campo e-mail é obrigatório."),
            Email(message="Por favor, insira um e-mail válido.")
        ]
    )
    tipo_evento = SelectField(
        'Tipo de Evento',
        choices=[('Palestra', 'Palestra'), 
                 ('Workshop', 'Workshop'),
                 ('Meetup', 'Meetup'), 
                 ('Outro', 'Outro')],
        validators=[DataRequired(message="O campo tipo de evento é obrigatório.")]
    )
    descricao = TextAreaField('Descrição (obrigatória se tipo for Outro)')
    enviar = SubmitField('Cadastrar')

    def validate_data_evento(self, field):
        if field.data < datetime.date.today():
            raise ValidationError("A data do evento não pode estar no passado.")

    def validate_descricao(self, field):
        if self.tipo_evento.data == 'Outro' and not field.data.strip():
            raise ValidationError("Descrição é obrigatória para o tipo 'Outro'.")

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/vazio", methods=['GET', 'POST'])
def formulario_vazio():
    form = EventoForm()
    if form.validate_on_submit():
        return render_template('sucesso.html', form=form)

    return render_template(
        'formulario.html',
        form=form,
        title="Cadastro de Evento (Vazio)"
    )


@app.route("/via-argumentos", methods=['GET', 'POST'])
def formulario_via_argumentos():
    form = EventoForm()
    if form.validate_on_submit():
        return render_template('sucesso.html', form=form)

    elif not form.is_submitted():
        dados_iniciais = {
            'nome_evento': 'Encontro de Tecnologia',
            'data_evento': datetime.date.today(),
            'organizador': 'João da Silva',
            'email': 'joao.silva@email.com',
            'tipo_evento': 'Workshop',
            'descricao': 'Evento preenchido por argumentos.'
        }
        form = EventoForm(**dados_iniciais)

    return render_template(
        'formulario.html',
        form=form,
        title="Cadastro de Evento (via Argumentos)"
    )


@app.route("/via-objeto", methods=['GET', 'POST'])
def formulario_via_objeto():
    class EventoMock:
        def __init__(self, nome_evento, data_evento, organizador, email, tipo_evento, descricao):
            self.nome_evento = nome_evento
            self.data_evento = data_evento
            self.organizador = organizador
            self.email = email
            self.tipo_evento = tipo_evento
            self.descricao = descricao

    form = EventoForm()
    if form.validate_on_submit():
        return render_template('sucesso.html', form=form)

    elif not form.is_submitted():
        evento_mock = EventoMock(
            nome_evento="Hackathon 2025",
            data_evento=datetime.date.today(),
            organizador="Maria Oliveira",
            email="maria.o@email.net",
            tipo_evento="Palestra",
            descricao="Evento vindo de um objeto mock."
        )
        form = EventoForm(obj=evento_mock)

    return render_template(
        'formulario.html',
        form=form,
        title="Cadastro de Evento (via Objeto)"
    )

if __name__ == '__main__':
    app.run(debug=True)
