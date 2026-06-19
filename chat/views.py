from datetime import datetime
import random
import flask
import flask_login
from app.database import DATABASE
from auth.models import Groups, User
import random

color_r_list = [80, 255,  75, 255,  64, 230, 226,   0, 170, 220]
color_g_list = [200, 127,   0, 215, 224, 230, 114,   0, 240,  20]
color_b_list = [120,  80, 130,   0, 208, 250,  91, 128, 209,  60]
def handle_chat_page(chat_id=None):
    
    if not flask_login.current_user.is_authenticated:
        return flask.redirect('/registration')

    # Инициализируем базовое значение (по умолчанию запрашивать вход не нужно)
    need_to_join = False
    
    
    # Сразу получаем объект активного чата, если передан chat_id
    active_chat = None
    if chat_id:
        active_chat = Groups.query.get(chat_id)
        if not active_chat:
            return flask.redirect('/chat/')
        
        # ЛОГИКА ПРОВЕРКИ ДОСТУПА:
        # Если чат открыт, проверяем, есть ли текущий юзер в списке участников этой группы
        if flask_login.current_user not in active_chat.users:
            need_to_join = True

    # ОБРАБОТКА POST ЗАПРОСОВ
    if flask.request.method == 'POST':
        action = flask.request.form.get("action")

        # 1. Действие: Вступление в группу
        if action == "join_group" and active_chat:
            if flask_login.current_user not in active_chat.users:
                active_chat.users.append(flask_login.current_user)
                DATABASE.session.commit()
            # Перезагружаем страницу этого же чата, теперь need_to_join станет False
            return flask.redirect(f'/chat/{chat_id}')

        # 2. Действие: Создание чата
        elif action == "create_chat":
            current_user_id = int(flask_login.current_user.id)
            existing_group = Groups.query.filter_by(owner_id=current_user_id).first()
            if existing_group:
                return flask.redirect('/chat/')

            chosen_name = flask.request.form.get('custom_group_name')
            if not chosen_name or chosen_name.strip() == "":
                user_name = flask_login.current_user.username or f"User{current_user_id}"
                chosen_name = f"Group {user_name} #{random.randint(1000, 9999)}"

            group = Groups(group_name=chosen_name, owner_id=current_user_id, color_r=random.choice(color_r_list), color_g=random.choice(color_g_list), color_b=random.choice(color_b_list))
            group.users.append(flask_login.current_user)
            DATABASE.session.add(group)
            DATABASE.session.commit()
            return flask.redirect('/chat/')

        # 3. Действие: Обновление профиля
        elif action == "update_profile":
            first_name = flask.request.form.get('first_name') or None
            last_name = flask.request.form.get('last_name') or None
            username = flask.request.form.get('username') or None
            gender = flask.request.form.get('gender')
            birth_date_str = flask.request.form.get('birth_date')
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str else None
            
                    

            flask_login.current_user.first_name = first_name
            flask_login.current_user.last_name = last_name
            flask_login.current_user.gender = gender
            flask_login.current_user.birth_date = birth_date
            if flask_login.current_user.color_r is None or flask_login.current_user.color_r == 0:
                random_index = random.randint(0, len(color_r_list) - 1)
                flask_login.current_user.color_r = color_r_list[random_index]
                flask_login.current_user.color_g = color_g_list[random_index]
                flask_login.current_user.color_b = color_b_list[random_index]
            

            user = User.query.filter_by(username=username).first()
            if user and user.id != flask_login.current_user.id:
                print('Username already exists')
            else:
                flask_login.current_user.username = username

            DATABASE.session.commit()
            return flask.redirect('/chat/')

        # 4. Действие: Удаление чата
        elif action == "delete_chat":
            current_user_id = int(flask_login.current_user.id)
            chat_to_delete = Groups.query.filter_by(owner_id=current_user_id).first()
            
            if chat_to_delete:
                chat_to_delete.users.clear()
                DATABASE.session.delete(chat_to_delete)
                DATABASE.session.commit()
            
            return flask.redirect('/chat/')

    # ФОРМИРОВАНИЕ ДАННЫХ ДЛЯ ШАБЛОНА (GET-запрос)
    current_user_id = int(flask_login.current_user.id)
    my_group = Groups.query.filter_by(owner_id=current_user_id).first()
    other_groups = Groups.query.filter(Groups.owner_id != current_user_id).all()

    if my_group is None:
        class EmptyGroup:
            id = None
            group_name = ""
        template_my_group = EmptyGroup()
        has_chat = False
    else:
        template_my_group = my_group
        has_chat = True

    return flask.render_template(
        'chat_page.html', 
        user=flask_login.current_user, 
        my_group=template_my_group,  
        has_chat=has_chat,            
        other_groups=other_groups,
        active_chat=active_chat,
        need_to_join=need_to_join  # Отправляем флаг в HTML-шаблон
    )