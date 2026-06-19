import flask


registration = flask.Blueprint(name = 'registration', 
                        import_name = __name__,
                        static_folder='static',
                        static_url_path='/auth/static',
                        template_folder='templates'
                        )
auth = flask.Blueprint(name = 'auth', 
                        import_name = __name__,
                        static_folder='static',
                        static_url_path='/auth/static',
                        template_folder='templates'
                        )
email_confirm = flask.Blueprint(name = 'email_confirm', 
                        import_name = __name__,
                        static_folder='static',
                        static_url_path='/auth/static',
                        template_folder='templates'
                        )