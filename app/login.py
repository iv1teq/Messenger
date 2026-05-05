import flask_login
from .settings import app
from registration.models import User
from config import SECRET_KEY

manager = flask_login.LoginManager(app = app)
app.secret_key = SECRET_KEY

manager.init_app(app)


@manager.user_loader
def get_user(user_id):
    print(f"Загружаю пользователя с ID: {user_id}")
    return User.query.get(int(user_id))



