import flask
import werkzeug.security as security
from .models import User
from app.database import DATABASE
import flask_login
import smtplib
from config import EMAIL, PASSWORD
import email.message as msg
from flask import session

def registration_view():

    if flask_login.current_user.is_authenticated and flask_login.current_user.is_verified:
        return flask.redirect('/')

    if flask.request.method == 'POST':
        email = flask.request.form.get('email')
        password = flask.request.form.get('password')

        filtred_user = User.query.filter_by(email=email).scalar()

        if not filtred_user:
            hashed_password = security.generate_password_hash(password)

            if password and email and len(password) >= 8:
                existing_user = User.query.filter_by(email=email).first()
                if existing_user:
                    flask.flash("Пользователь с такой почтой уже зарегистрирован!", "error")
                    print(123)
                    return flask.render_template("registration.html") 
                user = User(password_hash=hashed_password, email=email)
        
                DATABASE.session.add(user)
                DATABASE.session.commit()
                confirm_link = flask.url_for('auth.confirm_email_view', email=email, _external=True)

                html = f'''
                    <html>
                        <body style="margin:0; padding:0; font-family:Arial, sans-serif; background:#f6f8fb;">
                            <div style="max-width:700px; margin:0 auto; padding:24px;">
                                <div style="background:#ffffff; border-radius:28px; overflow:hidden; box-shadow:0 20px 60px rgba(15,23,42,0.08);">
                                    
                                    <div style="padding:36px 32px 24px; text-align:center;">
                                        <h1 style="font-size:32px; margin:0 0 16px; color:#111827;">Вас вітає команда World IT!</h1>
                                        <p style="font-size:16px; line-height:1.8; color:#4b5563; margin:0 0 30px;">
                                            Щоб завершити реєстрацію та переконатися, що саме ви є власником цієї електронної адреси, будь ласка, підтвердіть свою пошту.
                                        </p>
                                        
                                        <a href="{confirm_link}" style="display:inline-block; width:100%; max-width:420px; margin:0 auto; padding:18px 0; background:#111827; color:#ffffff; text-decoration:none; border-radius:14px; font-size:16px; font-weight:700;">
                                            Підтвердити пошту
                                        </a>
                                    </div>
                                    
                                    <div style="background:#ffffff; padding:0 32px 24px; text-align:center;">
                                        <img src="{{ url_for('registration.static', filename='images/world_it.svg')}}" alt="World IT illustration" style="width:100%; max-width:500px; border-none; border-radius:16px; display:block; margin:0 auto;" />
                                    </div>
                                    
                                    <div style="padding:0 32px 36px; text-align:center; color:#6b7280; font-size:14px; line-height:1.7;">
                                        <p style="margin:0;">Якщо у вас виникнуть питання — ми завжди раді допомогти!</p>
                                        <p style="margin:10px 0 0;">З найкращими побажаннями, команда WIT Academy</p>
                                    </div>
                                    
                                </div>
                            </div>
                        </body>
                    </html>
                '''
                
                with smtplib.SMTP(host = "smtp.gmail.com", port = 587) as smtp:
                    smtp.starttls()
                    smtp.login(user = EMAIL, password = PASSWORD)
                    email_msg = msg.EmailMessage()
                    email_msg["Subject"] = "Перевірка пошти"
                    email_msg["From"] = EMAIL
                    email_msg["To"] = email
                    email_msg.add_alternative(html, subtype = "html")
                    smtp.send_message(email_msg)
                session['email'] = email
                return flask.redirect('/confirm_page')
        else:
            flask.flash("Пользователь с такой почтой уже зарегистрирован!", "error")
            print(123)
            return flask.render_template("registration.html") 

    return flask.render_template('registration.html')

def confirm_email_view():
    if flask_login.current_user.is_authenticated and flask_login.current_user.is_verified:
        return flask.redirect('/')
    email = flask.request.args.get('email')
    if not email:
        return 'Невірне посилання для підтвердження пошти'

    user = User.query.filter_by(email=email).first()
    if not user:
        return 'Користувача не знайдено'

    if not user.is_verified:
        user.is_verified = True
        flask_login.login_user(user)
        DATABASE.session.commit()

    return flask.redirect('/')
    
def auth_view():
    if flask_login.current_user.is_authenticated and flask_login.current_user.is_verified:
        return flask.redirect('/')
    if flask.request.method == 'POST':

        email = flask.request.form.get('email')
        password = flask.request.form.get('password')

        filtred_user = User.query.filter_by(email=email).scalar()

        if filtred_user and security.check_password_hash(filtred_user.password_hash, password):
            flask_login.login_user(filtred_user)
            filtred_user.is_verified = True
            return flask.redirect('/')

    return flask.render_template('auth.html')

def confirm_email_page():
    if flask_login.current_user.is_authenticated and flask_login.current_user.is_verified:
        return flask.redirect('/')
    email = session.get('email')
    if email:
        return flask.render_template('email_confirm.html')
    return flask.redirect('/registration')  