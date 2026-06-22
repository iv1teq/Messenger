document.addEventListener('DOMContentLoaded', function () {
    const chatsDiv = document.getElementById('chats-div');
    const messagesDiv = document.getElementById('messages-div');
    const membersDiv = document.getElementById('members-div');
    const logoArea = document.querySelector('.logo-area');
    const groupNameLink = document.getElementById('group-name-link');
    const arrowMessages = document.getElementById('arrow-messages');
    const arrowMembers = document.getElementById('arrow-members');

    // Хардкодований URL — не залежить від form.action
    const CHAT_API_URL = '/chat/';

    // 1. ІНІЦІАЛІЗАЦІЯ SOCKET.IO
    const socket = io();

    socket.on('connect', () => console.log('Connected'));
    socket.on('disconnect', () => console.log('Disconnected'));
    socket.on('joined', (data) => console.log('Вошёл в комнату:', data.room));
    socket.on('error', (data) => console.log('Ошибка сокета:', data.msg));

    socket.on('display_status', (data) => {
        const members = data.members;
        const membersListDiv = membersDiv.querySelector('.members-list');
        if (!membersListDiv) return;
        membersListDiv.innerHTML = '';

        let amountMembers = 0;
        let amountOnlineMembers = 0;

        members.forEach((member) => {
            const memberDiv = document.createElement('div');
            amountMembers++;
            memberDiv.classList.add('member');
            memberDiv.dataset.username = member.username;
            memberDiv.dataset.fullname = `${member.first_name || ''} ${member.last_name || ''}`;
            memberDiv.dataset.initials = `${(member.first_name || '').slice(0, 1)}${(member.last_name || '').slice(0, 1)}`;

            const avatarDiv = document.createElement('div');
            avatarDiv.classList.add('members-avatar');
            avatarDiv.style.backgroundColor = `rgb(${member.color_r}, ${member.color_g}, ${member.color_b})`;
            avatarDiv.style.position = 'relative';

            const lettersDiv = document.createElement('div');
            lettersDiv.textContent = memberDiv.dataset.initials || (member.username || '?').slice(0, 1).toUpperCase();
            avatarDiv.appendChild(lettersDiv);

            if (member.status === 'online') {
                const statusDiv = document.createElement('div');
                statusDiv.classList.add('status');
                avatarDiv.appendChild(statusDiv);
                amountOnlineMembers++;
            }

            const usernameP = document.createElement('p');
            usernameP.id = 'username_right';
            usernameP.textContent = member.username;

            memberDiv.appendChild(avatarDiv);
            memberDiv.appendChild(usernameP);
            membersListDiv.appendChild(memberDiv);
        });

        const membersCount = document.querySelector('.members-count');
        if (membersCount) {
            membersCount.textContent = `${amountMembers} учасників · ${amountOnlineMembers} online`;
        }
    });

    const urlParts = window.location.pathname.split('/');
    const GROUP_ID = urlParts[urlParts.length - 1];

    const sendBtn = document.getElementById('send-button');
    const msgInput = document.getElementById('message-input');
    const messagesDisplay = document.getElementById('chat-messages-display');

    function scrollToBottom() {
        if (messagesDisplay) messagesDisplay.scrollTop = messagesDisplay.scrollHeight;
    }
    scrollToBottom();

    // 2. ВІДПРАВКА ТА ОТРИМАННЯ ПОВІДОМЛЕНЬ
    if (GROUP_ID && !isNaN(GROUP_ID) && msgInput) {
        socket.emit('join_room', { groupId: parseInt(GROUP_ID) });

        function SendMessage() {
            const inputValue = msgInput.value.trim();
            if (!inputValue) return;
            socket.emit('message', { content: inputValue, group_id: GROUP_ID });
            msgInput.value = '';
        }

        if (sendBtn) sendBtn.addEventListener('click', SendMessage);
        msgInput.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') { event.preventDefault(); SendMessage(); }
        });
    }

    socket.on('message', (data) => {
        if (data.group_id == GROUP_ID) {
            const messagesList = document.querySelector('.messages-list');
            if (!messagesList) return;

            const isOwn = data.user_id == CURRENT_USER_ID;
            const row = document.createElement('div');
            row.classList.add('message-row', isOwn ? 'message-out' : 'message-in');

            const avatar = document.createElement('div');
            avatar.classList.add('msg-avatar');
            avatar.style.backgroundColor = `rgb(${data.color_r || 128}, ${data.color_g || 128}, ${data.color_b || 128})`;
            avatar.textContent = (data.username || '?').slice(0, 1).toUpperCase();

            const wrapper = document.createElement('div');
            wrapper.classList.add('msg-bubble-wrapper');

            const meta = document.createElement('div');
            meta.classList.add('msg-meta');

            const author = document.createElement('span');
            author.classList.add('msg-username');
            author.textContent = isOwn ? 'You' : data.username;

            const time = document.createElement('span');
            time.classList.add('msg-time');
            time.textContent = data.time;

            meta.appendChild(author);
            meta.appendChild(time);

            const text = document.createElement('span');
            text.classList.add('message-text');
            text.textContent = data.message;

            wrapper.appendChild(meta);
            wrapper.appendChild(text);
            row.appendChild(avatar);
            row.appendChild(wrapper);
            messagesList.appendChild(row);
            scrollToBottom();
        }
    });

    // 3. НАВІГАЦІЯ МІЖ ПАНЕЛЯМИ
    if (logoArea) logoArea.addEventListener('click', () => {
        messagesDiv?.classList.remove('active');
        chatsDiv?.classList.add('active');
        membersDiv?.classList.remove('active');
    });

    attachChatLinkListener();

    if (sessionStorage.getItem('showMessages') === '1') {
        sessionStorage.removeItem('showMessages');
        messagesDiv?.classList.add('active');
        chatsDiv?.classList.remove('active');
        membersDiv?.classList.remove('active');
    }

    if (groupNameLink) groupNameLink.addEventListener('click', () => {
        messagesDiv?.classList.remove('active');
        chatsDiv?.classList.remove('active');
        membersDiv?.classList.add('active');
    });

    if (arrowMessages) arrowMessages.addEventListener('click', () => {
        messagesDiv?.classList.remove('active');
        chatsDiv?.classList.add('active');
        membersDiv?.classList.remove('active');
    });

    if (arrowMembers) arrowMembers.addEventListener('click', () => {
        messagesDiv?.classList.add('active');
        chatsDiv?.classList.remove('active');
        membersDiv?.classList.remove('active');
    });

    // 4. МОДАЛКА СТВОРЕННЯ ЧАТУ
    const openModalBtn = document.getElementById('open_modal_btn');
    const closeModalBtn = document.getElementById('close_modal_btn');
    const createChatModal = document.getElementById('create_chat-modal');
    const closeModalX = document.getElementById('close_modal_x');

    if (openModalBtn) openModalBtn.addEventListener('click', () => createChatModal.style.display = 'flex');
    if (closeModalBtn) closeModalBtn.addEventListener('click', () => createChatModal.style.display = 'none');
    if (closeModalX) closeModalX.addEventListener('click', () => createChatModal.style.display = 'none');

    // 5. ЖИВИЙ ПОШУК ЧАТІВ
    const searchInput = document.getElementById('chat-search');
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const filter = this.value.toLowerCase();
            document.querySelectorAll('.chat-link').forEach(link => {
                const title = link.querySelector('.chat-title');
                if (title) link.style.display = title.textContent.toLowerCase().includes(filter) ? 'block' : 'none';
            });
        });
    }

    // 6. МОДАЛКА ВИДАЛЕННЯ ЧАТУ
    const deleteModal = document.getElementById('delete-confirm-modal');
    const cancelDeleteBtn = document.getElementById('cancel-delete-btn');

    // делегування, бо кнопка видалення чату може зʼявитись динамічно (через socket)
    document.addEventListener('click', function (e) {
        const btn = e.target.closest('.delete-chat-btn');
        if (!btn || !deleteModal) return;
        e.preventDefault();
        e.stopPropagation();
        deleteModal.style.display = 'flex';
    });

    if (cancelDeleteBtn) cancelDeleteBtn.addEventListener('click', () => deleteModal.style.display = 'none');

    window.addEventListener('click', function(e) {
        if (deleteModal && e.target === deleteModal) deleteModal.style.display = 'none';
        if (createChatModal && e.target === createChatModal) createChatModal.style.display = 'none';
    });

    // 7. НАЛАШТУВАННЯ ПРОФІЛЮ
    const settingsBtn = document.getElementById('settings-btn');
    const cancelModalBtn = document.getElementById('cancel-modal-btn');
    const closeModalBtnSettings = document.getElementById('close-modal-btn');
    const settingsModal = document.querySelector('.modal');

    if (settingsBtn) settingsBtn.addEventListener('click', () => settingsModal.style.display = 'flex');
    function closeSettings() { if (settingsModal) settingsModal.style.display = 'none'; }
    if (cancelModalBtn) cancelModalBtn.addEventListener('click', closeSettings);
    if (closeModalBtnSettings) closeModalBtnSettings.addEventListener('click', closeSettings);

    // 8. КЛІК ПО УЧАСНИКАХ
    const membersList = document.querySelector('.members-list');
    const profileBlock = document.getElementById('profile');
    const profileLetters = document.getElementById('profile-letters');
    const profileFullname = document.getElementById('profile-fullname');
    const profileUsername = document.getElementById('profile-username');
    const closeProfileBtn = document.getElementById('close-profile-btn');

    if (membersList) {
        membersList.addEventListener('click', (e) => {
            const member = e.target.closest('.member');
            if (!member) return;
            if (profileLetters) profileLetters.textContent = member.dataset.initials || 'CH';
            if (profileFullname) profileFullname.textContent = member.dataset.fullname?.trim() || 'Без імені';
            if (profileUsername) profileUsername.textContent = `@${member.dataset.username}`;
            if (profileBlock) profileBlock.style.display = 'flex';
        });
    }
    if (closeProfileBtn) closeProfileBtn.addEventListener('click', () => profileBlock.style.display = 'none');

    // 9. ЕМОДЗІ ПАНЕЛЬ
    const EMOJIS = [
        "😀","😁","😂","🤣","😃","😄","😅","😆","😉","😊","😋","😎","😍","😘","🥰",
        "😗","😙","😚","🙂","🤗","🤔","🤨","😐","😑","😶","🙄","😏","😣","😥","😮",
        "😯","😪","😫","🥱","😴","😌","😛","😜","🤪","😝","🤤","😒","😓","😔","😕",
        "🙃","🤑","😲","☹️","🙁","😖","😞","😟","😤","😢","😭","😦","😧","😨","😩",
        "🤯","😬","😰","😱","🥵","🥶","😳","😡","😠","🤬","😷","🤒","🤕","🤢","🤮",
        "🥴","😇","🥳","🥺","🤡","👍","👎","👏","🙌","🙏","🤝","💪","✌️","🤞","👋",
        "❤️","🧡","💛","💚","💙","💜","🖤","🤍","💔","💯","🔥","✨","🎉","🎂","☕","🍕","⚽","🏀","🎵","⭐"
    ];

    const emojiIcon = document.getElementById('emoji-icon');
    const emojiPanel = document.getElementById('emoji-panel');

    if (emojiIcon && emojiPanel && msgInput) {
        EMOJIS.forEach(emoji => {
            const item = document.createElement('button');
            item.type = 'button';
            item.textContent = emoji;
            item.addEventListener('click', () => {
                const start = msgInput.selectionStart ?? msgInput.value.length;
                const end = msgInput.selectionEnd ?? msgInput.value.length;
                msgInput.value = msgInput.value.slice(0, start) + emoji + msgInput.value.slice(end);
                msgInput.focus();
                msgInput.selectionStart = msgInput.selectionEnd = start + emoji.length;
            });
            emojiPanel.appendChild(item);
        });
        emojiIcon.addEventListener('click', (e) => { e.stopPropagation(); emojiPanel.classList.toggle('show'); });
        document.addEventListener('click', (e) => {
            if (!emojiPanel.contains(e.target) && e.target !== emojiIcon) emojiPanel.classList.remove('show');
        });
    }

    // =============================================================
// 10. АВАТАР (ФІНАЛЬНА ВЕРСІЯ З ПРАВИЛЬНИМИ ІНІЦІАЛАМИ)
// =============================================================
    const changeAvatarBtn = document.getElementById('change-avatar-btn');
    const deleteAvatarBtn = document.getElementById('delete-avatar-btn');
    const avatarInput = document.getElementById('avatarInput');

    // Використовуємо шлях до вашого єдиного обробника чату
    const PROFILE_API_URL = '/chat/'; 

    function updateAvatarUI(avatarUrl) {
        const settingsAvatarWrapper = document.getElementById('settings-avatar-wrapper');
        const headerPp = document.getElementById('header_pp');
        
        // Безпечно беремо ініціали, згенеровані через Jinja в HTML
        const initials = window.USER_INITIALS || 'U';

        if (avatarUrl) {
            // Якщо аватар успішно завантажено — рендеримо тільки картинку без зайвого тексту
            const imgStyle = "width:100%; height:100%; object-fit:cover; border-radius:50%; display:block;";
            
            if (settingsAvatarWrapper) {
                settingsAvatarWrapper.innerHTML = `<img src="${avatarUrl}" alt="Avatar" class="avatar-img" style="${imgStyle}">`;
            }
            if (headerPp) {
                headerPp.innerHTML = `<img src="${avatarUrl}" alt="Avatar" style="${imgStyle}">`;
            }
        } else {
            // Якщо аватара немає або його видалили — повертаємо назад гарні чисті літери
            if (settingsAvatarWrapper) {
                settingsAvatarWrapper.innerHTML = `<span id="avatarLetters">${initials}</span>`;
            }
            if (headerPp) {
                headerPp.innerHTML = `<span id="header_letters">${initials}</span>`;
            }
        }
    }

    // Подія натискання на кнопку "Змінити"
    if (changeAvatarBtn && avatarInput) {
        changeAvatarBtn.addEventListener('click', () => avatarInput.click());
    }

    // Завантаження файлу на сервер
    if (avatarInput) {
        avatarInput.addEventListener('change', function () {
            const file = this.files[0];
            if (!file) return;
            
            const fd = new FormData();
            fd.append('action', 'update_avatar');
            fd.append('avatar', file);

            fetch(PROFILE_API_URL, { method: 'POST', body: fd })
                .then(r => r.json())
                .then(d => { 
                    if (d.success) {
                        updateAvatarUI(d.avatar_url); 
                    } else { 
                        alert('Помилка: ' + (d.error || 'Не вдалося оновити аватар')); 
                    } 
                })
                .catch(err => {
                    console.error('Помилка завантаження аватара:', err);
                });
        });
    }

    // Видалення аватара
    if (deleteAvatarBtn) {
        deleteAvatarBtn.addEventListener('click', () => {
            if (!confirm('Видалити аватар?')) return;
            
            const fd = new FormData();
            fd.append('action', 'delete_avatar');

            fetch(PROFILE_API_URL, { method: 'POST', body: fd })
                .then(r => r.json())
                .then(d => { 
                    if (d.success) {
                        updateAvatarUI(null); 
                    } else { 
                        alert('Помилка: ' + (d.error || 'Не вдалося видалити аватар')); 
                    } 
                })
                .catch(err => {
                    console.error('Помилка видалення аватара:', err);
                });
        });
    }

    // =============================================================
    // 11. СТВОРЕННЯ / ВИДАЛЕННЯ ЧАТІВ
    // =============================================================

    // Раніше відсутні оголошення — саме через це ламався весь блок
    const createChatForm = document.getElementById('create-chat-form');
    const deleteChatForm = document.getElementById('delete-chat-form');
    const myChatSection = document.getElementById('my-chat-section');
    const myChatContainer = document.getElementById('my-chat-container');
    const makeChatBtnWrapper = document.getElementById('make-chat-button-wrapper');
    const otherChatsList = document.getElementById('other-chats-list');
    const noOtherChatsPlaceholder = document.getElementById('no-other-chats-placeholder');

    // Функція генерації HTML-картки чату
    function buildChatCardHTML(group, isOwn) {
        const initials = (group.group_name || 'CH').slice(0, 2).toUpperCase();
        const rgb = `rgb(${group.color_r}, ${group.color_g}, ${group.color_b})`;
        const deleteBtnHTML = isOwn ? `<button class="delete-chat-btn" style="position:absolute;right:10px;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;padding:6px;">🗑</button>` : '';
        return `
            <div style="position: relative;">
                <a href="/chat/${group.id}" class="chat-link" data-group-id="${group.id}">
                    <div class="your_chat ${isOwn ? 'owned-chat' : ''}">
                        <div class="group-avatar" style="background-color: ${rgb};">${initials}</div>
                        <div class="saved_messages_text">
                            <div class="saved_time_text">
                                <h1 class="chat-name-heading ${isOwn ? 'font-bold' : 'font-medium'} chat-title">${group.group_name}</h1>
                                <p id="saved_time">щойно</p>
                            </div>
                            <p class="chat-subtext">Немає повідомлень</p>
                        </div>
                    </div>
                </a>
                ${deleteBtnHTML}
            </div>`;
    }

    // 1. Створення чату — перехоплюємо submit форми, замість окремого fetch без preventDefault-конфлікту
    if (createChatForm) {
        createChatForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const chatName = document.getElementById('custom_group_name')?.value?.trim();
            if (!chatName) return;

            const fd = new FormData();
            fd.append('action', 'create_chat');
            fd.append('custom_group_name', chatName);

            fetch(CHAT_API_URL, {
                method: 'POST',
                body: fd,
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
                .then(r => {
                    if (!r.ok) throw new Error(`Server error: ${r.status}`);
                    const contentType = r.headers.get('content-type') || '';
                    if (!contentType.includes('application/json')) {
                        throw new Error('Сервер повернув не JSON (можливо, ендпоінт не обробляє AJAX-запит)');
                    }
                    return r.json();
                })
                .then(data => {
                    if (data.success) {
                        if (createChatModal) createChatModal.style.display = 'none';
                        createChatForm.reset();
                        // якщо сервер не шле socket-подію group_created, підстрахуємось і оновимо список самостійно
                        if (data.group) {
                            const exists = document.querySelector(`.chat-link[data-group-id="${data.group.id}"]`);
                            if (!exists) {
                                const currentUserId = typeof CURRENT_USER_ID !== 'undefined' ? CURRENT_USER_ID : null;
                                const isOwn = currentUserId && data.group.owner_id == currentUserId;
                                if (isOwn && myChatSection && myChatContainer) {
                                    myChatSection.style.display = '';
                                    myChatContainer.innerHTML = buildChatCardHTML(data.group, true);
                                    if (makeChatBtnWrapper) makeChatBtnWrapper.style.display = 'none';
                                } else if (otherChatsList) {
                                    otherChatsList.insertAdjacentHTML('beforeend', buildChatCardHTML(data.group, false));
                                    if (noOtherChatsPlaceholder) noOtherChatsPlaceholder.style.display = 'none';
                                }
                                attachChatLinkListener();
                            }
                        }
                    } else {
                        alert(data.error || 'Не вдалося створити чат');
                    }
                })
                .catch(err => {
                    console.error('create_chat error:', err);
                    alert('Помилка при створенні чату: ' + err.message);
                });
        });
    }

    // 2. Видалення чату — перехоплюємо submit форми delete-chat-form
    if (deleteChatForm) {
        deleteChatForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const fd = new FormData();
            fd.append('action', 'delete_chat');

            fetch(CHAT_API_URL, {
                method: 'POST',
                body: fd,
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
                .then(r => {
                    if (!r.ok) throw new Error(`Server error: ${r.status}`);
                    const contentType = r.headers.get('content-type') || '';
                    if (!contentType.includes('application/json')) {
                        throw new Error('Сервер повернув не JSON (можливо, ендпоінт не обробляє AJAX-запит)');
                    }
                    return r.json();
                })
                .then(data => {
                    if (data.success) {
                        if (deleteModal) deleteModal.style.display = 'none';
                        // підстраховка, якщо socket-подія group_deleted не прийде
                        if (myChatSection && myChatContainer) {
                            myChatContainer.innerHTML = '';
                            myChatSection.style.display = 'none';
                            if (makeChatBtnWrapper) makeChatBtnWrapper.style.display = '';
                        }
                        const mDiv = document.getElementById('messages-div');
                        const cDiv = document.getElementById('chats-div');
                        if (mDiv && mDiv.classList.contains('active')) {
                            mDiv.classList.remove('active');
                            cDiv?.classList.add('active');
                        }
                    } else {
                        alert(data.error || 'Не вдалося видалити чат');
                    }
                })
                .catch(err => {
                    console.error('delete_chat error:', err);
                    alert('Помилка при видаленні чату: ' + err.message);
                });
        });
    }

    // 3. Робота з WebSockets через Socket.io
    socket.on('group_created', (group) => {
        // якщо картка вже додана в обробнику fetch вище — не дублюємо
        if (document.querySelector(`.chat-link[data-group-id="${group.id}"]`)) return;

        const currentUserId = typeof CURRENT_USER_ID !== 'undefined' ? CURRENT_USER_ID : null;
        const isOwn = currentUserId && group.owner_id == currentUserId;

        if (isOwn) {
            if (myChatSection) myChatSection.style.display = '';
            if (myChatContainer) myChatContainer.innerHTML = buildChatCardHTML(group, true);
            if (makeChatBtnWrapper) makeChatBtnWrapper.style.display = 'none';
        } else {
            if (otherChatsList) otherChatsList.insertAdjacentHTML('beforeend', buildChatCardHTML(group, false));
            if (noOtherChatsPlaceholder) noOtherChatsPlaceholder.style.display = 'none';
        }
        attachChatLinkListener();
    });

    // Слухач події видалення чату
    socket.on('group_deleted', (data) => {
        document.querySelectorAll(`.chat-link[data-group-id="${data.id}"]`).forEach(link => {
            const wasActive = link.querySelector('.active-chat-style') !== null;
            const wrapper = link.closest('div[style*="position: relative"]') || link;
            wrapper.remove();

            if (wasActive) {
                const mDiv = document.getElementById('messages-div');
                const cDiv = document.getElementById('chats-div');
                mDiv?.classList.remove('active');
                cDiv?.classList.add('active');
            }
        });

        if (myChatSection && myChatContainer && !myChatContainer.querySelector('.chat-link')) {
            myChatSection.style.display = 'none';
            if (makeChatBtnWrapper) makeChatBtnWrapper.style.display = '';
        }

        if (otherChatsList && otherChatsList.querySelectorAll('.chat-link').length === 0 && noOtherChatsPlaceholder) {
            noOtherChatsPlaceholder.style.display = '';
        }
    });

    // 4. Функція ініціалізації кліків по чатах
    function attachChatLinkListener() {
        document.querySelectorAll('.chat-link').forEach(link => {
            if (link.dataset.listenerAttached) return;
            link.dataset.listenerAttached = '1';
            link.addEventListener('click', function (e) {
                e.preventDefault();
                sessionStorage.setItem('showMessages', '1');
                window.location.href = this.href;
            });
        });
    }

}); // Кінець DOMContentLoaded