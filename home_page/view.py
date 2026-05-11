import flask
import flask_login
from registration.models import User


def render_home_page():
    if flask_login.current_user.is_authenticated:
        
        user = flask_login.current_user

        return flask.render_template('home_page.html')
    else:
        return flask.redirect('/registration')