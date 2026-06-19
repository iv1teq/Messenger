import flask_sqlalchemy as sqlalchemy
import flask_migrate
from .settings import app

DATABASE = sqlalchemy.SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///DATABASE.db"

DATABASE.init_app(app)

migrate = flask_migrate.Migrate(app = app, db = DATABASE, directory = "app/migrations")