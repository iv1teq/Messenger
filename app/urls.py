import flask
from .settings import app
from auth.app import registration, auth, email_confirm
from auth.views import registration_view, auth_view, confirm_email_view, confirm_email_page
from chat.app import chat_blueprint
from chat.views import handle_chat_page

# ==========================================
# 1. МАРШРУТЫ АВТОРИЗАЦИИ И РЕГИСТРАЦИИ
# ==========================================
registration.add_url_rule('/registration', 
                        view_func=registration_view, 
                        methods=['POST', 'GET'])

auth.add_url_rule('/auth', 
                view_func=auth_view, 
                methods=['POST', 'GET'])

auth.add_url_rule('/confirm', 
                view_func=confirm_email_view,
                methods=['GET'])

email_confirm.add_url_rule('/confirm_page', 
                        view_func=confirm_email_page,
                        methods=['GET'])

# ==========================================
# 2. МАРШРУТЫ ДЛЯ МЕССЕНДЖЕРА (ЧАТОВ)
# ==========================================

# Главная страница чатов (когда ни один конкретный чат еще не выбран)
# defaults={'chat_id': None} говорит Flask, что аргумент chat_id в функцию передавать не нужно (он будет None)
chat_blueprint.add_url_rule('/chat/', 
                            endpoint='chat_index',
                            view_func=handle_chat_page, 
                            defaults={'chat_id': None}, 
                            methods=['GET', 'POST'])

# Дополнительное правило, если пользователь просто введет '/' в браузере, чтобы его тоже кидало на вьюху чата
chat_blueprint.add_url_rule('/', 
                            endpoint='chat_root',
                            view_func=handle_chat_page, 
                            defaults={'chat_id': None}, 
                            methods=['GET', 'POST'])

# Страница конкретной комнаты чата. Сюда будут уходить и GET (для загрузки), 
# и POST-запросы (для создания, удаления, обновления и ВСТУПЛЕНИЯ "join_group")
chat_blueprint.add_url_rule('/chat/<int:chat_id>', 
                            endpoint='chat_room',
                            view_func=handle_chat_page, 
                            methods=['GET', 'POST'])


# ==========================================
# 3. РЕГИСТРАЦИЯ БЛЮПРИНТОВ В ПРИЛОЖЕНИИ
# ==========================================
app.register_blueprint(registration)
app.register_blueprint(auth)
app.register_blueprint(email_confirm)
app.register_blueprint(chat_blueprint)