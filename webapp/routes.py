from flask import render_template, flash, redirect, url_for
from webapp import app, wappdb
from webapp.forms import LoginForm
from flask_login import current_user, login_user
from webapp.models import User
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from webapp import wappdb
from webapp.forms import RegistrationForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm
from email.message import EmailMessage
from webapp.CFDImodels import CFDI, Emisor, Articulo69, Receptor
import threading
import smtplib
import locale
from datetime import datetime
from webapp.dbtools import cfdiscompl


def send_async_email(app_, srv, msge):
    with app_.app_context():
        if not srv['SSL']:
            smtp = smtplib.SMTP(srv['server'], srv['port'])
            smtp.starttls()
        else:
            smtp = smtplib.SMTP_SSL(srv['server'], srv['port'])  # Use this for Nemaris Server
        smtp.login(srv['user'], srv['password'])
        smtp.sendmail(msge['From'], msge['To'], msge.as_string())
        smtp.quit()


def send_email(server, msg):
    threading.Thread(target=send_async_email, args=(app, server, msg)).start()


def send_password_reset_email(usr):
    smtpserver = app.config['SMTP']

    msg = EmailMessage()
    msg['Subject'] = "Restablecer Password - Robot Email"
    msg['From'] = smtpserver['user']
    msg['To'] = usr.email
    msg.set_type('text/html')

    token = usr.get_reset_password_token()
    msg.set_content(render_template('email/reset_password.txt', user=usr, token=token))
    html_msg = render_template('email/reset_password.html', user=usr, token=token)
    msg.add_alternative(html_msg, subtype="html")

    send_email(smtpserver, msg)


def snart69b(rfcfdi):
    a69 = 'No'
    art69 = Articulo69.query.filter_by(rfc=rfcfdi, situacion='Definitivo').all()
    if len(art69) != 0:
        a69 = 'Sí'
    return a69


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    cols = ['Emisor', 'Serie', 'Folio', 'Fecha', 'SubTotal', 'Total', 'Art.69b']
    # c = CFDI.query.filter_by().first()
    # .add_columns().filter(friendships.user_id == userID).paginate(page, 1, False)
    c = CFDI.query.join(Emisor, CFDI.uuid == Emisor.uuid).add_columns(CFDI.serie, CFDI.subtotal,
                                                                      CFDI.folio, CFDI.fecha, CFDI.total,
                                                                      Emisor.RFC, Emisor.nombre).all()
    # c = CFDI.query.all()
    facts = list()
    for line in c:

        facts.append([line.RFC, line.serie, line.folio, datetime.strftime(line.fecha, "%d/%m/%Y"),
                      locale.currency(line.subtotal, grouping=True), locale.currency(line.total, grouping=True),
                      snart69b(line.RFC)])
    #  '$' + '{:20,.2f}'.format(line.total)
    return render_template('index.html', title='Inicio', columnas=cols, facturas=facts)


@app.route('/aerolineas', methods=['GET', 'POST'])
@login_required
def aerolineas():
    cfdiscompl('Aerolineas')
    # cols = ['Emisor', 'Serie', 'Folio', 'Fecha', 'SubTotal', 'Total']
    c, cols = cfdiscompl('Aerolineas')
    cols.append('Art.69b')
    facts = list()
    for line in c:
        facts.append([line[0], line[1], line[2], datetime.strftime(line[3], "%d/%m/%Y"),
                      locale.currency(line[4], grouping=True), locale.currency(line[5], grouping=True),
                      locale.currency(line[6], grouping=True), locale.currency(line[7], grouping=True)
                      ])
        for i in range(8, len(line)):
            facts[len(facts) - 1].append(locale.currency(line[i], grouping=True))
        facts[len(facts) - 1].append(snart69b(line[0]))
    rightalg = ''
    for i in range(4, len(facts[0]) - 1):
        rightalg = rightalg + str(i) + ', '
    rightalg = rightalg[:-2]
    #  '$' + '{:20,.2f}'.format(line.total)
    return render_template('tua.html', title='Inicio', columnas=cols, facturas=facts, alg=rightalg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    frm_lgin = LoginForm()
    if frm_lgin.validate_on_submit():
        user = User.query.filter_by(username=frm_lgin.username.data).first()
        if user is None or not user.check_password(frm_lgin.password.data):
            flash('Nombre de usuario o password invalido')
            return redirect(url_for('login'))
        login_user(user, remember=frm_lgin.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Ingreso', form=frm_lgin)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        wappdb.session.add(user)
        wappdb.session.commit()
        flash('Se ha registrado el usuario nuevo.')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


@app.route('/usuarios')
@login_required
def usuarios():
    u = User.query.all()
    return render_template('usuarios.html', title='Usuarios', users=u)


@app.route('/perfil/<username>', methods=['GET', 'POST'])
@login_required
def perfil(username):
    usr = User.query.filter_by(username=username).first_or_404()
    frm = EditProfileForm(usr.username, usr.email)
    frm.username.id = usr.username
    frm.email.id = usr.email
    if frm.validate_on_submit():
        user = User.query.filter_by(username=frm.original_username).first()
        user.username = frm.username.data
        user.email = frm.email.data
        if frm.oldpassword != "":
            user.set_password(frm.newpassword.data)
        wappdb.session.commit()
        flash('Actualización completada con éxito.')
        return redirect(url_for('usuarios'))
    return render_template('perfil.html', user=usr, form=frm)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Restablecer Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        wappdb.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)