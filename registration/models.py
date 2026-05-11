from app.db import db
import flask_login


class User(db.Model, flask_login.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    avatar_path = db.Column(db.String)
    gender = db.Column(db.String)
    birth_date = db.Column(db.String)
    is_verified = db.Column(db.Boolean)