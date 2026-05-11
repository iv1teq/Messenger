import flask


registration_blueprint = flask.Blueprint(name = "registration_blueprint",
                                        import_name=__name__,
                                        static_folder="static",
                                        template_folder="templates",
                                        static_url_path="/registration/static")



login_blueprint = flask.Blueprint(name = "login_blueprint",
                                        import_name=__name__,
                                        static_folder="static",
                                        template_folder="templates",
                                        static_url_path="/registration/static")

