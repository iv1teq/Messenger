from .app import registration_blueprint, login_blueprint
from .view import render_registration, render_login, email_confirmation, email_confirmation_page
from .models import User
from .mailer import send_email