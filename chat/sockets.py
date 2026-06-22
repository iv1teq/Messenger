import datetime
import flask_socketio
import flask
from auth.models import Groups, Message 
from app.settings import app, socket
from app.database import DATABASE
import flask_login
from .app import online_users


@socket.on('connect')
def handle_connect(auth=None):
    print('Connected')
    if not flask_login.current_user.is_authenticated:
        return

    user_id = flask_login.current_user.id

    if user_id in online_users:
        online_users[user_id].add(flask.request.sid)
    else:
        online_users[user_id] = {flask.request.sid}
        
        # Знаходимо всі групи, в яких перебуває користувач
        user_groups = Groups.query.filter(Groups.users.any(id=user_id)).all()
        for group in user_groups:
            data = {
                "title": group.group_name,
                "members": []
            }
            for user in group.users:
                status = "online" if user.id in online_users else "offline"
                data["members"].append({
                    "status": status,
                    "email": user.email,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "avatar": user.avatar,  # 🌟 ДОДАНО: передаємо URL аватара
                    "color_r": user.color_r,
                    "color_g": user.color_g,
                    "color_b": user.color_b,
                })
            # Відправляємо оновлений список у кімнату цієї групи
            flask_socketio.emit('display_status', data, to=f'room_{group.id}')


@socket.on('disconnect')
def handle_disconnect():
    print('Disconnected')
    if not flask_login.current_user.is_authenticated:
        return

    user_id = flask_login.current_user.id

    if user_id in online_users:
        online_users[user_id].discard(flask.request.sid)
        if not online_users[user_id]:
            del online_users[user_id]
            
            # Знаходимо всі групи користувача, який пішов в офлайн
            user_groups = Groups.query.filter(Groups.users.any(id=user_id)).all()
            for group in user_groups:
                data = {
                    "title": group.group_name,
                    "members": []
                }
                for user in group.users:
                    status = "online" if user.id in online_users else "offline"
                    data["members"].append({
                        "status": status,
                        "email": user.email,
                        "username": user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "avatar": user.avatar,  # 🌟 ДОДАНО: передаємо URL аватара
                        "color_r": user.color_r,
                        "color_g": user.color_g,
                        "color_b": user.color_b,
                    })
                # Відправляємо змінені статуси всім, хто залишився в кімнаті
                flask_socketio.emit('display_status', data, to=f'room_{group.id}')


@socket.on('join_room')
def handle_join_room(data):
    group_id = data.get('groupId')
    user_id = flask_login.current_user.id

    if not group_id:
        flask_socketio.emit('error', {'msg': 'groupId не передан'})
        return

    # Приводимо до int на випадок, якщо з фронтенду прийшов рядок
    group = Groups.query.get(int(group_id))

    if not group:
        flask_socketio.emit('error', {'msg': 'группа не найдена'})
        return

    user_in_group = any(user.id == user_id for user in group.users)

    if user_in_group:
        flask_socketio.join_room(f'room_{group.id}')
        flask_socketio.emit('joined', {'room': f'room_{group.id}'})
        print(f'Пользователь {user_id} вошёл в room_{group.id}')

        data = {
            "title": group.group_name,
            "members": []
        }

        for user in group.users:
            status = "online" if user.id in online_users else "offline"
            data["members"].append({
                "status": status,
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "avatar": user.avatar,  # 🌟 ДОДАНО: передаємо URL аватара
                "color_r": user.color_r,
                "color_g": user.color_g,
                "color_b": user.color_b,
            }) 

        flask_socketio.emit('display_status', data, to=f'room_{group.id}')
    else:
        flask_socketio.emit('error', {'msg': 'нет доступа'})


@socket.on('message')
def handle_message_event(data):
    if not flask_login.current_user.is_authenticated:
        flask_socketio.emit('error', {'msg': 'Ошибка отправки: вы не авторизованы'})
        return

    group_id = data.get('group_id')
    content = data.get('content', '').strip()
    
    if not content or not group_id:
        return

    current_user = flask_login.current_user

    # 1. СНАЧАЛA створюємо повідомлення і зберігаємо його в базу даних
    new_message = Message(content=content, group_id=int(group_id), user_id=current_user.id)
    DATABASE.session.add(new_message)
    DATABASE.session.commit()

    # 2. Тільки ПІСЛЯ commit беремо час із створеного запису
    formatted_time = new_message.created_at.strftime("%H:%M")

    payload = {
        'message': content,
        'username': current_user.username,
        'user_id': current_user.id,
        'group_id': group_id,
        'avatar': current_user.avatar,  # 🌟 ДОДАНО: передаємо аватар того, хто пише повідомлення
        'color_r': current_user.color_r or 255,
        'color_g': current_user.color_g or 255,
        'color_b': current_user.color_b or 255,
        'time': formatted_time
    }

    flask_socketio.emit('message', payload, to=f'room_{group_id}')