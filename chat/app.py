import flask

chat_blueprint = flask.Blueprint(name = 'chat_page',
                                import_name = __name__,
                                template_folder = 'templates',
                                static_folder = 'static',
                                static_url_path = '/chat/static')

online_users = {}