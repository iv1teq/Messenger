import flask
import werkzeug.security as security
from .models import User
from app.db import db
import flask_login

def render_registration():
    
    if_error = False

    if flask.request.method == 'POST':
        email = flask.request.form.get('email')
        filtered_user = User.query.filter_by(email = email).scalar() 

        if not filtered_user:
            password = flask.request.form.get('password')
            password_hash = security.generate_password_hash(password)
            
            if password and email and len(password) >= 8:
                user = User(password = password_hash, email = email)
                db.session.add(user)
                db.session.commit()
                flask_login.login_user(user)

        else:
            print('errror')
            if_error = True

    return flask.render_template('registration.html', if_error = if_error) 

def redirect_to_reg():
    return flask.redirect(flask.url_for("registration_blueprint.render_registration"))

def render_login():
    if flask.request.method == 'POST':

        email = flask.request.form.get('email')
        password = flask.request.form.get('password')
        filtered_user = User.query.filter_by(email = email).scalar()

        if filtered_user and security.check_password_hash(filtered_user.password, password):
            flask_login.login_user(filtered_user)


    return flask.render_template('login.html', success = False) 