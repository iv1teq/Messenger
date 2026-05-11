import flask
from .settings import app
from registration.app import registration_blueprint, login_blueprint
from registration.view import render_registration, render_login, email_confirmation, email_confirmation_page
from home_page.app import home_page
from home_page.view import render_home_page


registration_blueprint.add_url_rule(rule = "/registration", 
                                    view_func = render_registration,
                                    methods = ["POST", "GET"]
                                    )

registration_blueprint.add_url_rule(rule="/email_confirmation_page",
                view_func = email_confirmation_page)

app.add_url_rule(rule="/email_confirmation",
                view_func = email_confirmation,
                methods = ["POST", "GET"])

login_blueprint.add_url_rule(rule = '/login', 
                            view_func = render_login, 
                            methods = ["POST", "GET"]
                            )
home_page.add_url_rule(rule = '/', 
                    view_func=render_home_page,
                    methods = ["POST", "GET"]
                    )


app.register_blueprint(registration_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(home_page)