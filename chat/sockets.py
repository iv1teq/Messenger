# import datetime
# import flask_socketio
# import flask
# from auth.models import Groups , Message 
# from app.settings import app , socket
# from app.database import DATABASE
# import flask_login
# from .app import online_users


# @socket.on('connect')
# def handle_connect(auth=None):
#     print('Connected')
#     if not flask_login.current_user.is_authenticated:
#         return

#     user_id = flask_login.current_user.id

#     if user_id in online_users:
#         online_users[user_id].add(flask.request.sid)
#     else:
#         online_users[user_id] = {flask.request.sid}
        
#         # Находим все группы, в которых состоит зашедший пользователь
#         user_groups = Groups.query.filter(Groups.users.any(id=user_id)).all()
#         for group in user_groups:
#             # Прямо здесь собираем статусы для участников этой группы
#             data = {
#                 "title": group.group_name,
#                 "members": []
#             }
#             for user in group.users:
#                 status = "online" if user.id in online_users else "offline"
#                 data["members"].append({
#                     "status": status,
#                     "email": user.email,
#                     "username": user.username,
#                     "first_name": user.first_name,
#                     "last_name": user.last_name,
#                     "color_r": user.color_r,
#                     "color_g": user.color_g,
#                     "color_b": user.color_b,
#                 })
#             # Отправляем обновленный список в комнату этой группы
#             flask_socketio.emit('display_status', data, to=f'room_{group.id}')


# @socket.on('disconnect')
# def handle_disconnect():
#     print('Disconnected')
#     if not flask_login.current_user.is_authenticated:
#         return

#     user_id = flask_login.current_user.id

#     if user_id in online_users:
#         online_users[user_id].discard(flask.request.sid)
#         if not online_users[user_id]:
#             del online_users[user_id]
            
#             # Находим все группы пользователя, который ушел в оффлайн
#             user_groups = Groups.query.filter(Groups.users.any(id=user_id)).all()
#             for group in user_groups:
#                 # Прямо здесь собираем актуальные статусы заново
#                 data = {
#                     "title": group.group_name,
#                     "members": []
#                 }
#                 for user in group.users:
#                     status = "online" if user.id in online_users else "offline"
#                     data["members"].append({
#                         "status": status,
#                         "email": user.email,
#                         "username": user.username,
#                         "first_name": user.first_name,
#                         "last_name": user.last_name,
#                         "color_r": user.color_r,
#                         "color_g": user.color_g,
#                         "color_b": user.color_b,
#                     })
#                 # Отправляем измененные статусы всем оставшимся в комнате
#                 flask_socketio.emit('display_status', data, to=f'room_{group.id}')


# @socket.on('join_room')
# def handle_join_room(data):
#     group_id = data.get('groupId')
#     user_id = flask_login.current_user.id

#     if not group_id:
#         flask_socketio.emit('error', {'msg': 'groupId не передан'})
#         return

#     group = Groups.query.get(group_id)

#     if not group:
#         flask_socketio.emit('error', {'msg': 'группа не найдена'})
#         return

#     user_in_group = any(user.id == user_id for user in group.users)

#     if user_in_group:
#         flask_socketio.join_room(f'room_{group.id}')
#         flask_socketio.emit('joined', {'room': f'room_{group.id}'})
#         print(f'Пользователь {user_id} вошёл в room_{group.id}')

#         data = {
#             "title": group.group_name,
#             "members": []
#         }

#         for user in group.users:
#             status = "online" if user.id in online_users else "offline"
#             data["members"].append({
#                 "status": status,
#                 "email": user.email,
#                 "username": user.username,
#                 "first_name": user.first_name,
#                 "last_name": user.last_name,
#                 "color_r": user.color_r,
#                 "color_g": user.color_g,
#                 "color_b": user.color_b,
#             }) 

#         flask_socketio.emit('display_status', data, to=f'room_{group.id}')
#     else:
#         flask_socketio.emit('error', {'msg': 'нет доступа'})


# @socket.on('message')
# def handle_message_event(data):
#     if not flask_login.current_user.is_authenticated:
#         flask_socketio.emit('error', {'msg': 'Ошибка отправки: вы не авторизованы'})
#         return

#     group_id = data.get('group_id')
#     content = data.get('content', '').strip()
    
#     if not content or not group_id:
#         return

#     current_user_name = flask_login.current_user.username 
#     current_user_id = flask_login.current_user.id

#     new_message = Message(content=content, group_id=int(group_id), user_id=current_user_id)
#     DATABASE.session.add(new_message)
#     DATABASE.session.commit()
#     formatted_time = new_message.created_at.strftime("%H:%M")

#     payload = {
#         'message': content,
#         'username': current_user_name,
#         'user_id': current_user_id,
#         'group_id': group_id,
#         'color_r': flask_login.current_user.color_r or 255,
#         'color_g': flask_login.current_user.color_g or 255,
#         'color_b': flask_login.current_user.color_b or 255,
#         'time': formatted_time
#     }

#     flask_socketio.emit('message', payload, to=f'room_{group_id}')
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
        
        # Находим все группы, в которых состоит зашедший пользователь
        user_groups = Groups.query.filter(Groups.users.any(id=user_id)).all()
        for group in user_groups:
            # Прямо здесь собираем статусы для участников этой группы
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
                    "color_r": user.color_r,
                    "color_g": user.color_g,
                    "color_b": user.color_b,
                })
            # Отправляем обновленный список в комнату этой группы
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
            
            # Находим все группы пользователя, который ушел в оффлайн
            user_groups = Groups.query.filter(Groups.users.any(id=user_id)).all()
            for group in user_groups:
                # Прямо здесь собираем актуальные статусы заново
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
                        "color_r": user.color_r,
                        "color_g": user.color_g,
                        "color_b": user.color_b,
                    })
                # Отправляем измененные статусы всем оставшимся в комнате
                flask_socketio.emit('display_status', data, to=f'room_{group.id}')


@socket.on('join_room')
def handle_join_room(data):
    group_id = data.get('groupId')
    user_id = flask_login.current_user.id

    if not group_id:
        flask_socketio.emit('error', {'msg': 'groupId не передан'})
        return

    # ИСПРАВЛЕНО: Приводим к int на случай, если с фронтенда пришла строка
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

    current_user_name = flask_login.current_user.username 
    current_user_id = flask_login.current_user.id

    # 1. СНАЧАЛА создаем сообщение и сохраняем его в базу данных
    new_message = Message(content=content, group_id=int(group_id), user_id=current_user_id)
    DATABASE.session.add(new_message)
    DATABASE.session.commit()

    # 2. ИСПРАВЛЕНО: Только ПОСЛЕ commit берем время из созданной записи
    formatted_time = new_message.created_at.strftime("%H:%M")

    payload = {
        'message': content,
        'username': current_user_name,
        'user_id': current_user_id,
        'group_id': group_id,
        'color_r': flask_login.current_user.color_r or 255,
        'color_g': flask_login.current_user.color_g or 255,
        'color_b': flask_login.current_user.color_b or 255,
        'time': formatted_time
    }

    flask_socketio.emit('message', payload, to=f'room_{group_id}')