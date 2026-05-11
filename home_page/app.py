import flask





home_page = flask.Blueprint(name = "homepage_blueprint",
                                        import_name=__name__,
                                        static_folder="static",
                                        template_folder="templates",
                                        static_url_path="/home_page/static")