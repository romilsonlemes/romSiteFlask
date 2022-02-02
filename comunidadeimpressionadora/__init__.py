from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# import pyperclip


app = Flask(__name__)

# ***** Configurações Gerais da Aplicação *****
# ---------------------------------------------
# TOKEN de acesso
app.config['SECRET_KEY'] = '59940c20166524157d996d8ba6749e6b'

# Configurações de acesso ao Banco de Dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/comunidade.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager = LoginManager(app)


# Criar o Banco de dados Físic
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from comunidadeimpressionadora import routes

