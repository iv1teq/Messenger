<div align="center">

# 💬 Viktor's Messenger

**Веб-месенджер у реальному часі на Flask, Jinja2, SQLAlchemy та Socket.IO**
**A real-time web messenger built with Flask, Jinja2, SQLAlchemy, and Socket.IO**

</div>

---

## 🇺🇦 Українська версія

### 📋 Зміст

1. [Мета створення проєкту](#-1-мета-створення-проєкту)
2. [Склад команди](#-2-склад-команди)
3. [Перелік модулів та технологій](#-3-перелік-модулів-та-технологій)
4. [Як запустити проєкт](#-4-як-запустити-проєкт)
5. [Зміст проєкту](#-5-зміст-проєкту)
6. [Висновок по роботі](#-6-висновок-по-роботі)

---

### 🎯 1. Мета створення проєкту

**Viktor's Messenger** — навчальний full-stack проєкт, створений для того, щоб на практиці розібратись, як працює веб-месенджер «під капотом»: від реєстрації користувача до обміну повідомленнями в реальному часі.

Проєкт буде корисним початківцю, тому що тут наочно показано:

- як побудувати backend на **Flask** з кількома blueprint-модулями (реєстрація, авторизація, чат);
- як організувати роботу з базою даних через **SQLAlchemy ORM** (моделі користувачів, груп, повідомлень, зв'язки many-to-many);
- як реалізувати **онлайн-комунікацію в реальному часі** за допомогою **Socket.IO** (кімнати, статуси «онлайн/офлайн», миттєва доставка повідомлень);
- як зверстати адаптивний інтерфейс на чистому **HTML/CSS/JS** без важких фреймворків на фронтенді;
- як працювати із завантаженням файлів (аватарів користувачів) на сервері.

Тобто це хороша «навчальна пісочниця» для розуміння архітектури реальних месенджерів (Telegram, Discord) у спрощеному вигляді.

---

### 👥 2. Склад команди

Проєкт виконано **самостійно (solo)**, без команди.

| Учасник | GitHub |
|---|---|
| Viktor Horiunov | [github.com/iv1teq](https://github.com/iv1teq) |

---

### 🛠 3. Перелік модулів та технологій

**Backend:**
- **Python 3** — основна мова розробки
- **Flask** — мікрофреймворк для веб-застосунку та маршрутизації
- **Flask-Login** — авторизація та керування сесіями користувачів
- **Flask-SocketIO** — обгортка над Socket.IO для Flask
- **SQLAlchemy** — ORM для роботи з базою даних
- **Jinja2** — шаблонізатор для серверного рендерингу HTML-сторінок
- **Werkzeug** — утиліти (безпечні імена файлів, хешування паролів тощо)

**Real-time комунікація:**
- **Socket.IO** (server + client) — обмін повідомленнями та статусами користувачів у реальному часі через WebSocket-кімнати

**Frontend:**
- **HTML5 / CSS3** — верстка інтерфейсу (трипанельний layout: чати / повідомлення / учасники)
- **Vanilla JavaScript** — динамічна логіка інтерфейсу, робота з Socket.IO-клієнтом, AJAX-запити (Fetch API)

**База даних:**
- SQL-база даних (через SQLAlchemy ORM, з моделями `User`, `Groups`, `Message`)

---

### 🚀 4. Як запустити проєкт

#### Крок 1. Клонувати репозиторій

```bash
git clone https://github.com/iv1teq/Messenger.git
cd Messenger
```

#### Крок 2. Створити та активувати віртуальне середовище

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

#### Крок 3. Встановити залежності

```bash
pip install -r requirements.txt
```

> Якщо файлу `requirements.txt` немає — встанови вручну основні пакети:
> ```bash
> pip install flask flask-login flask-socketio flask-sqlalchemy werkzeug
> ```

#### Крок 4. Налаштувати базу даних

Переконайся, що в конфігурації застосунку (`app/settings.py` або аналогічний файл) вказано правильний шлях/рядок підключення до бази даних. За потреби виконай ініціалізацію таблиць (наприклад, через `db.create_all()` у скрипті ініціалізації).

#### Крок 5. Запустити застосунок

```bash
python run.py
```

(назва файлу запуску може відрізнятись — перевір `main.py` / `app.py` / `run.py` у корені проєкту)

#### Крок 6. Відкрити у браузері

Перейди за адресою:

```
http://127.0.0.1:5000
```

---

### 📂 5. Зміст проєкту

Нижче — загальна схема того, з яких частин складається застосунок:

> 🖼️ *[Місце для зображення/скріншоту загальної архітектури або інтерфейсу застосунку]*

| Модуль / Додаток | Роль у проєкті |
|---|---|
| **`auth/`** | Модуль реєстрації та авторизації користувачів. Містить моделі бази даних (`User`, `Groups`, `Message`) та логіку входу/реєстрації через Flask-Login |
| **`chat_page/`** | Основний модуль чату (blueprint). Обробляє маршрут `/chat/`, логіку створення/видалення груп, приєднання до чату, оновлення профілю та аватара |
| **`templates/`** | HTML-шаблони на Jinja2 (сторінка чату, реєстрації, логіну), які рендеряться на сервері |
| **`static/css/`** | Стилі інтерфейсу — трипанельний layout (список чатів, область повідомлень, список учасників), адаптивна верстка |
| **`static/js/`** | Клієнтська логіка: підключення до Socket.IO, відправка/отримання повідомлень у реальному часі, керування модальними вікнами (створення чату, налаштування профілю, видалення чату), живий пошук чатів, emoji-панель |
| **`static/avatars/`** | Папка для зберігання завантажених користувачами аватарів |
| **socket-обробники (`sockets.py`)** | Серверна логіка реального часу: підключення/відключення користувача, статус «онлайн/офлайн», вхід у кімнату чату, надсилання та трансляція повідомлень усім учасникам кімнати |
| **`app/database.py`** | Інініціалізація з'єднання з базою даних (SQLAlchemy) |
| **`app/settings.py`** | Конфігурація Flask-застосунку та об'єкта Socket.IO |

**Як це працює разом:** користувач реєструється/логіниться → потрапляє на сторінку чату → може створити свою групу або приєднатись до чужої → після приєднання клієнт підключається до Socket.IO-кімнати цієї групи → усі повідомлення та статуси учасників синхронізуються в реальному часі між усіма, хто перебуває в кімнаті.

---

### ✅ 6. Висновок по роботі

Робота над **Viktor's Messenger** дала змогу на практиці пройти повний цикл розробки full-stack веб-застосунку — від проєктування бази даних до реального часу комунікації між користувачами.

**Чому проєкт був корисний:**
- дозволив зрозуміти різницю між звичайним HTTP-запитом (REST/AJAX) та постійним WebSocket-з'єднанням;
- навчив працювати з кімнатами (rooms) у Socket.IO для ізоляції повідомлень між різними чатами;
- показав, як побудувати relational-модель даних (користувачі ↔ групи ↔ повідомлення) через SQLAlchemy;
- дав досвід верстки складного UI (трипанельний адаптивний layout) без важких фронтенд-фреймворків.

**Чого навчились:**
- структурувати Flask-застосунок через blueprint-модулі;
- синхронізувати серверний рендеринг (Jinja2) з динамічними оновленнями через JavaScript та Socket.IO;
- обробляти файли (завантаження аватарів) безпечно на сервері;
- дебажити та виправляти несумісності версій бібліотек (наприклад, зміни в API `Flask-SocketIO`).

**Як можна розвивати проєкт далі:**
- додати підтримку групових чатів із кількома учасниками одночасно (не лише «один власник — один чат»);
- реалізувати приватні повідомлення (1-на-1) окремо від групових чатів;
- додати читання статусів повідомлень («прочитано»/«доставлено»);
- впровадити шифрування повідомлень;
- додати push-сповіщення та підтримку медіафайлів (зображення, відео, голосові повідомлення);
- покрити проєкт автотестами та налаштувати CI/CD.

---
---

## 🇬🇧 English Version

### 📋 Table of Contents

1. [Project Purpose](#-1-project-purpose)
2. [Team Members](#-2-team-members)
3. [Modules and Technologies](#-3-modules-and-technologies)
4. [How to Run the Project](#-4-how-to-run-the-project)
5. [Project Structure](#-5-project-structure)
6. [Conclusion](#-6-conclusion)

---

### 🎯 1. Project Purpose

**Viktor's Messenger** is a learning-oriented full-stack project created to understand, hands-on, how a real-time web messenger works under the hood — from user registration to real-time message exchange.

This project is useful for beginners because it clearly demonstrates:

- how to build a **Flask** backend using multiple blueprint modules (registration, authentication, chat);
- how to work with a database through the **SQLAlchemy ORM** (user, group, and message models, many-to-many relationships);
- how to implement **real-time communication** using **Socket.IO** (rooms, online/offline status, instant message delivery);
- how to build a responsive interface using plain **HTML/CSS/JS** without heavy frontend frameworks;
- how to handle file uploads (user avatars) on the server side.

In short, it's a solid "learning sandbox" for understanding the architecture of real messengers (like Telegram or Discord) in a simplified form.

---

### 👥 2. Team Members

This project was completed **solo**, without a team.

| Member | GitHub |
|---|---|
| Viktor Horiunov | [github.com/iv1teq](https://github.com/iv1teq) |

---

### 🛠 3. Modules and Technologies

**Backend:**
- **Python 3** — core programming language
- **Flask** — micro-framework for the web app and routing
- **Flask-Login** — user authentication and session management
- **Flask-SocketIO** — Socket.IO wrapper for Flask
- **SQLAlchemy** — ORM for database operations
- **Jinja2** — server-side HTML templating engine
- **Werkzeug** — utilities (secure filenames, password hashing, etc.)

**Real-time communication:**
- **Socket.IO** (server + client) — real-time message exchange and user status updates via WebSocket rooms

**Frontend:**
- **HTML5 / CSS3** — interface layout (three-panel layout: chats / messages / members)
- **Vanilla JavaScript** — dynamic UI logic, Socket.IO client integration, AJAX requests (Fetch API)

**Database:**
- SQL database (via SQLAlchemy ORM, with `User`, `Groups`, and `Message` models)

---

### 🚀 4. How to Run the Project

#### Step 1. Clone the repository

```bash
git clone https://github.com/iv1teq/Messenger.git
cd Messenger
```

#### Step 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

#### Step 3. Install dependencies

```bash
pip install -r requirements.txt
```

> If there's no `requirements.txt` file, install the core packages manually:
> ```bash
> pip install flask flask-login flask-socketio flask-sqlalchemy werkzeug
> ```

#### Step 4. Set up the database

Make sure the application configuration (`app/settings.py` or a similar file) points to the correct database connection string. If needed, run the table initialization (e.g., via `db.create_all()` in an init script).

#### Step 5. Run the application

```bash
python run.py
```

(the entry-point filename may differ — check for `main.py` / `app.py` / `run.py` in the project root)

#### Step 6. Open in your browser

Navigate to:

```
http://127.0.0.1:5000
```

---

### 📂 5. Project Structure

Below is a general overview of how the application is organized:

> 🖼️ *[Placeholder for a screenshot/image of the overall app architecture or interface]*

| Module / App | Role in the Project |
|---|---|
| **`auth/`** | Registration and authentication module. Contains database models (`User`, `Groups`, `Message`) and login/registration logic via Flask-Login |
| **`chat_page/`** | Main chat module (blueprint). Handles the `/chat/` route, group creation/deletion logic, joining chats, profile and avatar updates |
| **`templates/`** | Jinja2 HTML templates (chat page, registration, login) rendered server-side |
| **`static/css/`** | Interface styling — three-panel layout (chat list, message area, members list), responsive design |
| **`static/js/`** | Client-side logic: Socket.IO connection, real-time message sending/receiving, modal management (create chat, profile settings, delete chat), live chat search, emoji panel |
| **`static/avatars/`** | Folder for storing user-uploaded avatars |
| **Socket handlers (`sockets.py`)** | Server-side real-time logic: user connect/disconnect, online/offline status, joining chat rooms, sending and broadcasting messages to all room members |
| **`app/database.py`** | Database connection initialization (SQLAlchemy) |
| **`app/settings.py`** | Flask application and Socket.IO object configuration |

**How it works together:** a user registers/logs in → lands on the chat page → can create their own group or join someone else's → after joining, the client connects to that group's Socket.IO room → all messages and member statuses are synced in real time among everyone present in the room.

---

### ✅ 6. Conclusion

Working on **Viktor's Messenger** made it possible to go through a full development cycle of a full-stack web application in practice — from database design to real-time communication between users.

**Why the project was useful:**
- helped understand the difference between a regular HTTP request (REST/AJAX) and a persistent WebSocket connection;
- taught how to work with Socket.IO rooms to isolate messages between different chats;
- demonstrated how to build a relational data model (users ↔ groups ↔ messages) using SQLAlchemy;
- provided experience building a complex UI (responsive three-panel layout) without heavy frontend frameworks.

**What we learned:**
- structuring a Flask application using blueprint modules;
- syncing server-side rendering (Jinja2) with dynamic updates via JavaScript and Socket.IO;
- handling file uploads (avatars) securely on the server;
- debugging and fixing library version incompatibilities (e.g., changes in the `Flask-SocketIO` API).

**How the project could be developed further:**
- add support for group chats with multiple participants at once (not just "one owner — one chat");
- implement private one-on-one messaging separate from group chats;
- add message read/delivered status tracking;
- introduce message encryption;
- add push notifications and media file support (images, video, voice messages);
- cover the project with automated tests and set up CI/CD.