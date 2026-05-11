import flask
import werkzeug.security as security
from .models import User
from app.db import db
import flask_login
from .mailer import send_email

from flask import session

import random



def render_registration():
    
    if_error = False

    if flask.request.method == 'POST':
        email = flask.request.form.get('email')
        session['email'] = email
        filtered_user = User.query.filter_by(email = email).scalar() 

        if not filtered_user:
            password = flask.request.form.get('password')
            password_hash = security.generate_password_hash(password)
            
            if password and email and len(password) >= 8:
                user = User(password = password_hash, email = email)
                db.session.add(user)
                db.session.commit()
                send_email(user_email=email)
                
                
                return flask.redirect('/email_confirmation_page')

        else:
            print('errror')
            if_error = True

    return flask.render_template('registration.html', if_error = if_error) 

def render_login():
    if_error_login = False
    if flask.request.method == 'POST':

        email = flask.request.form.get('email')
        password = flask.request.form.get('password')
        filtered_user = User.query.filter_by(email = email).scalar()

        if filtered_user and filtered_user.is_verified and security.check_password_hash(filtered_user.password, password):
            flask_login.login_user(filtered_user)
            return flask.redirect('/')
        else:
            if_error_login = True

    return flask.render_template('login.html', if_error = if_error_login) 

def email_confirmation_page():
    return flask.render_template('email_confirmation.html')

def email_confirmation():
    email = flask.request.args.get('email')

    filtered_user = User.query.filter_by(email = email).scalar()

    if filtered_user:
        filtered_user.is_verified = True
        db.session.commit()
        flask_login.login_user(filtered_user)

    
    print(filtered_user)

    return flask.redirect('/')

