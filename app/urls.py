import flask
from .settings import app
from registration.app import registration_blueprint, login_blueprint
from registration.view import render_registration, redirect_to_reg, render_login


registration_blueprint.add_url_rule(rule = "/registration", 
                                    view_func = render_registration,
                                    methods = ["POST", "GET"]
                                    )
app.add_url_rule(rule="/",
                view_func=redirect_to_reg)

login_blueprint.add_url_rule(rule = '/login', 
                            view_func = render_login, 
                            methods = ["POST", "GET"]
                            )

app.register_blueprint(registration_blueprint)
app.register_blueprint(login_blueprint)