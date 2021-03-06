from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user

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


# A classe dos campos de edição do Formulário do Perfil do Usuário
class FormEditarPerfil(FlaskForm):
    username        = StringField('Nome de Usuário', validators=[DataRequired()])
    email           = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

    # ---------------------------------------------------
    # ------         Cursos da Hash TAG            ------
    # ---------------------------------------------------
    curso_Excel     = BooleanField('Excel Impressionador')
    curso_Vba       = BooleanField('VBA Impressionador')
    curso_Python    = BooleanField('Python Impressionador')
    curso_PowerBi   = BooleanField('Power BI Impressionador')
    curso_ppt       = BooleanField('Apresentações Impressionadoras')
    curso_Sql       = BooleanField('SQL Impressionador')
    # ---------------------------------------------------
    botao_submit_EditarPerfil = SubmitField('Confirmar Edição')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError(f'Já existe o usuário com esse e-mail. Cadastre outro e-mail')

# A classe dos campos para criação / Edição de Posts de Usuários
class FormCriarPost(FlaskForm):
    titulo          = StringField('Titulo do Post', validators=[DataRequired(), Length(2, 140)])
    corpo           = TextAreaField('Escreva o seu Post Aqui', validators=[DataRequired()])
    botao_submit    = SubmitField('Criar Post')
