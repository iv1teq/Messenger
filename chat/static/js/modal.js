document.addEventListener('DOMContentLoaded', function () {
    const chatsDiv = document.getElementById('chats-div');
    const messagesDiv = document.getElementById('messages-div');
    const membersDiv = document.getElementById('members-div');
    const logoArea = document.querySelector('.logo-area');
    const groupNameLink = document.getElementById('group-name-link');
    const arrowMessages = document.getElementById('arrow-messages');
    const arrowMembers = document.getElementById('arrow-members');

    // 1. ИНИЦИАЛИЗАЦИЯ SOCKET.IO

    const socket = io();

    socket.on('connect', () => {
        console.log('Connected');
    });

    socket.on('disconnect', () => {
        console.log('Disconnected');
    });

    socket.on('joined', (data) => {
        console.log('Вошёл в комнату:', data.room);
    });

    socket.on('error', (data) => {
        console.log('Ошибка сокета:', data.msg);
    });

    socket.on('display_status', (data) => {
        const members = data.members;
        const membersListDiv = membersDiv.querySelector('.members-list'); 
        membersListDiv.innerHTML = '';

        let amountMembers = 0;
        let amountOnlineMembers = 0;

        members.forEach((member) => {
            const memberDiv = document.createElement('div');
            amountMembers = amountMembers + 1;
            memberDiv.classList.add('member');
            memberDiv.style.cursor = 'pointer';
            memberDiv.dataset.username = member.username;
            memberDiv.dataset.fullname = `${member.first_name || ''} ${member.last_name || ''}`;
            memberDiv.dataset.initials = `${(member.first_name || '').slice(0, 1)}${(member.last_name || '').slice(0, 1)}`;
            
            const avatarDiv = document.createElement('div');
            avatarDiv.classList.add('members-avatar');
            avatarDiv.style.backgroundColor = `rgb(${member.color_r}, ${member.color_g}, ${member.color_b})`;

            const lettersDiv = document.createElement('div');
            lettersDiv.id = 'letters';
            lettersDiv.textContent = memberDiv.dataset.initials;
            avatarDiv.appendChild(lettersDiv);

            const statusDiv = document.createElement('div');
            if (member.status === 'online') {
                statusDiv.classList.add('status'); 
                amountOnlineMembers = amountOnlineMembers + 1;
            }

            const usernameP = document.createElement('p');
            usernameP.id = 'username_right';
            usernameP.textContent = member.username;

            memberDiv.appendChild(avatarDiv);
            memberDiv.appendChild(statusDiv);
            memberDiv.appendChild(usernameP);
            membersListDiv.appendChild(memberDiv);
        });

        const membersCount = document.querySelector('.members-count');
        if (membersCount) {
            membersCount.textContent = `${amountMembers} пользователя, ${amountOnlineMembers} online`;
        }
    });

    const urlParts = window.location.pathname.split('/');
    const GROUP_ID = urlParts[urlParts.length - 1];

    const sendBtn = document.getElementById('send-button');
    const msgInput = document.getElementById('message-input');
    const messagesDisplay = document.getElementById('chat-messages-display');


    function scrollToBottom() {
        if (messagesDisplay) {
            messagesDisplay.scrollTop = messagesDisplay.scrollHeight;
        }
    }


    scrollToBottom();


    // 2. ЛОГИКА ОТПРАВКИ И ПРИЕМА СООБЩЕНИЙ

    
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
            if (event.key === 'Enter') {
                event.preventDefault(); 
                SendMessage();
            }
        });
    }

    // Слушаем сервер и выводим сообщения
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

            const displayName = isOwn ? 'You' : data.username;
            
            avatar.textContent = (data.username || '?').slice(0, 1).toUpperCase();

            const wrapper = document.createElement('div');
            wrapper.classList.add('msg-bubble-wrapper');

            const meta = document.createElement('div');
            meta.classList.add('msg-meta');

            const author = document.createElement('span');
            author.classList.add('msg-username');
            author.textContent = displayName;

            const time = document.createElement('span');
            time.classList.add('msg-time');

            time.textContent = data.time; 

            meta.appendChild(author);
            meta.appendChild(time);

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

        // 3. ПЕРЕХОД ПО ЧАТАМ И АКТИВАЦИЯ ПАНЕЛЕЙ



        if (logoArea && messagesDiv && chatsDiv && membersDiv) {
            logoArea.addEventListener('click', () => {
                messagesDiv.classList.remove('active');
                chatsDiv.classList.add('active');
                membersDiv.classList.remove('active');
            });
        }

        document.querySelectorAll('.chat-link').forEach(link => {
            link.addEventListener('click', function(event) {
                event.preventDefault();
                sessionStorage.setItem('showMessages', '1'); 
                window.location.href = this.href;
            });
        });

        if (sessionStorage.getItem('showMessages') === '1' && messagesDiv && chatsDiv && membersDiv) {
            sessionStorage.removeItem('showMessages');
            messagesDiv.classList.add('active');
            chatsDiv.classList.remove('active');
            membersDiv.classList.remove('active');
        }

        if (groupNameLink && messagesDiv && chatsDiv && membersDiv) {
            groupNameLink.addEventListener('click', () => {
                messagesDiv.classList.remove('active');
                chatsDiv.classList.remove('active');
                membersDiv.classList.add('active');
            });
        }

        if (arrowMessages && messagesDiv && chatsDiv && membersDiv) {
            arrowMessages.addEventListener('click', () => {
                messagesDiv.classList.remove('active');
                chatsDiv.classList.add('active');
                membersDiv.classList.remove('active');
            });
        }

        if (arrowMembers && messagesDiv && chatsDiv && membersDiv) {
            arrowMembers.addEventListener('click', () => {
                messagesDiv.classList.add('active');
                chatsDiv.classList.remove('active');
                membersDiv.classList.remove('active');
            });
        }


        // 4. МОДАЛЬНОЕ ОКНО СОЗДАНИЯ ЧАТА 

        const openModalBtn = document.getElementById('open_modal_btn');
        const closeModalBtn = document.getElementById('close_modal_btn');
        const createChatModal = document.getElementById('create_chat-modal');
        const closeModalX = document.getElementById('close_modal_x');

        if (openModalBtn && createChatModal) {
            openModalBtn.addEventListener('click', function () {
                createChatModal.style.display = 'flex';
            });
        }

        if (closeModalBtn && createChatModal) {
            closeModalBtn.addEventListener('click', function () {
                createChatModal.style.display = 'none';
            });
        }

        if (closeModalX && createChatModal) {
            closeModalX.addEventListener('click', function () {
                createChatModal.style.display = 'none';
            });
        }


        // 5. ЖИВОЙ ПОИСК ЧАТОВ

        const searchInput = document.getElementById('chat-search');
        
        if (searchInput) {
            searchInput.addEventListener('input', function () {
                const filter = searchInput.value.toLowerCase();
                const chats = document.querySelectorAll('.your_chat');

                chats.forEach(function (chat) {
                    const titleElement = chat.querySelector('.chat-title');
                    if (titleElement) {
                        const chatName = titleElement.textContent.toLowerCase();
                        if (chatName.startsWith(filter)) {
                            chat.style.display = 'flex'; 
                        } else {
                            chat.style.display = 'none'; 
                        }
                    }
                });
            });
        }


    // 6. МОДАЛЬНОЕ ОКНО УДАЛЕНИЯ ЧАТА

    const deleteBtn = document.querySelector('.delete-chat-btn');
    const deleteModal = document.getElementById('delete-confirm-modal');
    const cancelDeleteBtn = document.getElementById('cancel-delete-btn');

    if (deleteBtn && deleteModal) {
        deleteBtn.addEventListener('click', function(event) {
            event.preventDefault();  
            event.stopPropagation(); 
            deleteModal.style.display = 'flex'; 
        });
    }

    if (cancelDeleteBtn && deleteModal) {
        cancelDeleteBtn.addEventListener('click', function() {
            deleteModal.style.display = 'none';
        });
    }

    window.addEventListener('click', function(event) {
        if (deleteModal && event.target === deleteModal) {
            deleteModal.style.display = 'none';
        }
        if (createChatModal && event.target === createChatModal) {
            createChatModal.style.display = 'none';
        }
    });


    // 7. НАСТРОЙКИ ПРОФИЛЯ

    const settingsBtn = document.getElementById('settings-btn');
    const cancelModalBtn = document.getElementById('cancel-modal-btn');
    const closeModalBtnSettings = document.getElementById('close-modal-btn');
    const settingsModal = document.querySelector('.modal');

    if (settingsBtn && settingsModal) {
        settingsBtn.addEventListener('click', () => {
            settingsModal.style.display = 'flex';
        });
    }

    function closeSettings() {
        if (settingsModal) settingsModal.style.display = 'none';
    }

    if (cancelModalBtn) cancelModalBtn.addEventListener('click', closeSettings);
    if (closeModalBtnSettings) closeModalBtnSettings.addEventListener('click', closeSettings);


    // 8. КЛИК ПО УЧАСТНИКАМ (ПРОФИЛЬ ВНИЗУ)

    const members = document.querySelectorAll('.member');
    const profileBlock = document.getElementById('profile');
    
    const profileLetters = document.getElementById('profile-letters');
    const profileFullname = document.getElementById('profile-fullname');
    const profileUsername = document.getElementById('profile-username');
    const closeBtn = document.getElementById('close-profile-btn');

    members.forEach(member => {
        member.addEventListener('click', () => {
            const username = member.getAttribute('data-username');
            const fullname = member.getAttribute('data-fullname');
            const initials = member.getAttribute('data-initials');

            if (profileLetters) profileLetters.textContent = initials || 'CH';
            if (profileFullname) profileFullname.textContent = fullname.trim() ? fullname : 'Без имени';
            if (profileUsername) profileUsername.textContent = `@${username}`;

            if (profileBlock) profileBlock.style.display = 'flex'; 
        });
    });

    if (closeBtn && profileBlock) {
        closeBtn.addEventListener('click', (e) => {
            e.stopPropagation(); 
            profileBlock.style.display = 'none'; 
        });
    }
});