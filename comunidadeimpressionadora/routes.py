import flask_bcrypt
from flask import render_template, redirect, url_for, flash, request
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil
from comunidadeimpressionadora.models import Usuario
from flask_login import login_user, logout_user, current_user, login_required

listaUsuarios = ['Romilson', 'Thiago', 'Juan', 'Juliano', 'Valquiria', 'Marcelo', 'Ivens']

# Configuração Inicial
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/usuarios')
@login_required
def usuarios():
    listaUsuarios.sort()
    return render_template('usuarios.html', listaUsuarios=listaUsuarios)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit()  and 'botao_submit_Login' in request.form:
        #Verificar se o usuário existe
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            # Exibir msg de Login Bem Sucedido
            print(f"Login Realizado com sucesso pelo email: {form_login.email.data}")
            flash(f"Login feito com sucesso no email: {form_login.email.data}", "alert-success")
            param_next = request.args.get('next')
            if param_next:
                return redirect(param_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f"Falha no Login: {form_login.email.data} ou Senha errada !!", "alert-danger")


    if form_criarconta.validate_on_submit() and 'botao_submit_CriarConta' in request.form:
        # Criar o Usuario
        # Critografar a senha do Usuário antes de Gravar na base de dados
        senha_criptog = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data,
                          email=form_criarconta.email.data,
                          senha=senha_criptog)

        # Adicionar a Sessão e commitar o Registro
        database.session.add(usuario)
        database.session.commit()

        print(f"Criada a conta do email: {form_login.email.data} com sucesso")
        flash(f"Conta criada para o email: {form_login.email.data}", "alert-success")
        return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com Sucesso', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)


@app.route('/perfil/editar', methods=['GET', 'post'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        database.session.commit()
        flash('Perfil atualizado com Sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form.email.data     = current_user.email
        form.username.data  = current_user.username

    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/post/criar')
@login_required
def criar_post():
    return render_template('criarpost.html')



