import flask_sqlalchemy as sqlalchemy
import flask_migrate
from .settings import app

db = sqlalchemy.SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"

db.init_app(app)

migrate = flask_migrate.Migrate(app = app, db = db, directory = "app/migrations")




