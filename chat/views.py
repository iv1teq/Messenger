from datetime import datetime
import random
import os
import flask
import flask_login
from werkzeug.utils import secure_filename
from app.database import DATABASE
from auth.models import Groups, User
from app.settings import socket  # імпортуємо об'єкт SocketIO

# Список кольорів для нових чатів/користувачів
color_r_list = [80, 255,  75, 255,  64, 230, 226,   0, 170, 220]
color_g_list = [200, 127,   0, 215, 224, 230, 114,   0, 240,  20]
color_b_list = [120,  80, 130,   0, 208, 250,  91, 128, 209,  60]

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(CURRENT_DIR, 'static', 'avatars')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def handle_chat_page(chat_id=None):
    if not flask_login.current_user.is_authenticated:
        return flask.redirect('/registration')

    need_to_join = False
    active_chat = None
    
    if chat_id:
        active_chat = Groups.query.get(chat_id)
        if not active_chat:
            return flask.redirect('/chat/')
        if flask_login.current_user not in active_chat.users:
            need_to_join = True

    if flask.request.method == 'POST':
        action = flask.request.form.get("action")

        # Завантаження аватара
        if action == "update_avatar":
            if 'avatar' not in flask.request.files:
                return flask.jsonify({'error': 'Файл не знайдено у запиті'}), 400
            file = flask.request.files['avatar']
            if file.filename == '':
                return flask.jsonify({'error': 'Файл не вибрано'}), 400
            if file and allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = secure_filename(f"user_{flask_login.current_user.id}.{ext}")
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                avatar_url = f"/chat/static/avatars/{filename}"
                flask_login.current_user.avatar = avatar_url
                DATABASE.session.commit()
                return flask.jsonify({'success': True, 'avatar_url': avatar_url})

        # Видалення аватара
        elif action == "delete_avatar":
            flask_login.current_user.avatar = None
            DATABASE.session.commit()
            return flask.jsonify({'success': True, 'avatar_url': None})

        # Вступ до групи
        elif action == "join_group" and active_chat:
            if flask_login.current_user not in active_chat.users:
                active_chat.users.append(flask_login.current_user)
                DATABASE.session.commit()
            return flask.redirect(f'/chat/{chat_id}')

        # Створення чату
        # Створення чату
        elif action == "create_chat":
            try:
                current_user_id = int(flask_login.current_user.id)
                
                # Перевіряємо, чи є вже створена група у цього користувача
                existing_group = Groups.query.filter_by(owner_id=current_user_id).first()
                if existing_group:
                    # Повертаємо 200, щоб JS прочитав текст помилки, а не впав у .catch()
                    return flask.jsonify({'success': False, 'error': 'У вас вже є створений чат. Ви не можете створити більше одного.'})

                chosen_name = flask.request.form.get('custom_group_name', '').strip()
                if not chosen_name:
                    user_name = flask_login.current_user.username or f"User{current_user_id}"
                    chosen_name = f"Group {user_name} #{random.randint(1000, 9999)}"

                color_index = random.randint(0, len(color_r_list) - 1)
                group = Groups(
                    group_name=chosen_name,
                    owner_id=current_user_id,
                    color_r=color_r_list[color_index],
                    color_g=color_g_list[color_index],
                    color_b=color_b_list[color_index],
                )
                
                # Спочатку додаємо групу в базу, щоб вона отримала свій ID
                DATABASE.session.add(group)
                DATABASE.session.flush()  # Отримуємо group.id без повного коміту

                # Додаємо зв'язок користувача з групою
                if flask_login.current_user not in group.users:
                    group.users.append(flask_login.current_user)
                
                DATABASE.session.commit()

                group_payload = {
                    'id': group.id,
                    'group_name': group.group_name,
                    'owner_id': group.owner_id,
                    'color_r': group.color_r,
                    'color_g': group.color_g,
                    'color_b': group.color_b,
                }

                # ✅ Emit через об'єкт socket з broadcast=True
                socket.emit('group_created', group_payload)

                return flask.jsonify({'success': True, 'group': group_payload})

            except Exception as e:
                DATABASE.session.rollback()
                print(f"[create_chat ERROR] {e}")
                return flask.jsonify({'success': False, 'error': f'Помилка сервера при створенні чату: {str(e)}'})
        # Оновлення профілю
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

        # Видалення чату
        elif action == "delete_chat":
            try:
                current_user_id = int(flask_login.current_user.id)
                chat_to_delete = Groups.query.filter_by(owner_id=current_user_id).first()

                if chat_to_delete:
                    deleted_group_id = chat_to_delete.id
                    chat_to_delete.users.clear()
                    DATABASE.session.delete(chat_to_delete)
                    DATABASE.session.commit()

                    # ✅ ВИПРАВЛЕННЯ: emit через об'єкт socket з broadcast=True
                    socket.emit('group_deleted', {'id': deleted_group_id})

                    return flask.jsonify({'success': True, 'id': deleted_group_id})

                return flask.jsonify({'success': False, 'error': 'Чат не знайдено'}), 404

            except Exception as e:
                DATABASE.session.rollback()
                print(f"[delete_chat ERROR] {e}")
                return flask.jsonify({'success': False, 'error': 'Помилка сервера при видаленні чату'}), 500

    # GET-запит — формування даних для шаблону
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
        need_to_join=need_to_join
    )