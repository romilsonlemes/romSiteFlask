from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario

# A classe abaixo é utilizada para controlar os campos que terá no formulário
class FormCriarConta(FlaskForm):
    username                = StringField('Nome de usuário', validators=[DataRequired()])
    email                   = StringField('E-mail', validators=[DataRequired(), Email()])
    senha                   = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha       = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_CriarConta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError(f'O e-mail acima do usuário {usuario.username}  já está cadastrado. Cadastre-se com outro e-mail ou faça login para continuar')


# A classe dos campos do Formulário de Login
class FormLogin(FlaskForm):
    email           = StringField('E-mail', validators=[DataRequired(), Email()])
    senha           = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados   =   BooleanField('Lembrar dados e acesso')
    botao_submit_Login = SubmitField('Fazer Login')
