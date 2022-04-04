/*



*/


var chatSocket;
var connected = false;


function storageSet(key, object) {
	localStorage.setItem(key, JSON.stringify(object));
}


function storageGet(key) {
    const raw = localStorage.getItem(key);
	return JSON.parse(raw);
}


function setupWebSocket() {
    const requestId = new Date().getTime();
    const token = $('#jwt-token').val();

    typeof WebSocket !== 'undefined' && function connect() {
        chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/?token=${token}`);

        chatSocket.onopen = event => {
            console.info('websocket opened!');
            const chats = storageGet('allChats');

            chatSocket.send(
                JSON.stringify({
                    action: 'join_to_chats',
                    request_id: requestId,
                })
            );

            $.each(chats, function (index, chat) {
                console.log('subscride', chat.ucid);

                chatSocket.send(
                    JSON.stringify({
                        ucid: chat.ucid,
                        action: 'retrieve',
                        request_id: requestId,
                    })
                );
                chatSocket.send(
                    JSON.stringify({
                        ucid: chat.ucid,
                        action: 'subscribe_to_messages_in_chat',
                        request_id: requestId,
                    })
                );
            });
        };

        chatSocket.onmessage = event => {
            const data = JSON.parse(event.data);
            console.log(data);

            switch (data.action) {
                case 'create_new_chat':
                    console.log(data);
                    renderNewChatItem(data.data.ucid);

                case 'retrieve':
                    console.log(data.data)
                    for (let message of data?.data?.messages || []) {
                        processRetrievedMessage(message);
                        console.log(data.action, message);
                    }
                    break;
                case 'create':
                    processReceivedMessage(data.data);
                    console.log(data.action, data.data);
                    break;
                case 'update':
                    console.log(data.action, data.data);
                    break;
                default:
                    break;
            }
        };

        chatSocket.onerror = err => {
            console.error(err);
            chatSocket.onclose = null;
            connected = false;
            chatSocket.close();
            connect();
        };

        chatSocket.onclose = event => {
            console.info(`WebSocket closed with code ${event.code}! ${event.reason}`);
            connected = false;
            if (event.wasClean) {
                return;
            }
            connect();
        };
    }();

    $('#chat-message-input').focus();
    $('#chat-message-input').on('keydown', function (event) {
        // enter, return
        if (event.keyCode === 13) {
            const message = $(event.currentTarget).val().trim();

            if (message.length > 0) {
                event.preventDefault();
                sendMessage(chatSocket);
            }
        }
    });

    $('#chat-message-submit').on('click', sendMessage.bind(chatSocket));
}


function asideChatMenuClickHandler(event) {
    let target = $(event.currentTarget);
    const chats = storageGet('chatsMessages');
    const ucid = $(target).data('chat-ucid');
    const chat = chats[ucid];
    
    let unreadMessages = storageGet('unreadMessages');
    
    if (ucid === null) {
        console.error('Attribute \"data-chat-ucid\" not found in target element');
        return;
    } else {
        renderChat(ucid);
    }

    if (chat === null) {
        console.error(`Chat with ucid \"${ucid}\" not found in chatsMessages`);
        return;      
    }

    $('li.active-aside-chat-menu-tab')?.removeClass('active-aside-chat-menu-tab');
    $(target).addClass('active-aside-chat-menu-tab');

    delete unreadMessages[ucid];
    storageSet('unreadMessages', unreadMessages);

    updateAmountMessagesBadge(ucid);
    updateSiteTitle();

}


function makePreviewText(message) {
    if (message.photo) {
        return '[фото 🖼]';
    } else if (message.document) {
        return `[файл 📁] ${message.file_name}`;
    } else if (message.text) {
        return message.text;
    } else {
        return'[нет сообщений]';
    }
}


function makeReplyText(message) {
    const username = message?.staff ? "Вы" : message.user.first_name;

    if (message.photo) {
        return `<i><strong>${username}:</strong></i> [фото 🖼]`;
    } else if (message.document) {
        return `<i><strong>${username}:</strong></i> [файл 📁] ${message.file_name}`;
    } else if (message.text) {
        return `<i><strong>${username}:</strong></i> ${message.text}`;
    } else {
        return'[сообщение удалено]';
    }
}


function renderChatMessage(message, userType) {
    const captionBlock = message.caption ? `<div class="telegram-text-message">${message.caption}</div>` : "";
    var messageBody;
    var replyBlock;

    if (message.reply_to_message) {
        replyBlock = `<div class="telegram-reply-message" data-target-message-id="${message.reply_to_message.id}">
                            ${makeReplyText(message.reply_to_message)}
                        </div>`;
    } else {
        replyBlock = '';
    }

    if (message.photo) {  
        messageBody = $(`<div class="message-in-chat" data-message-id="${message.id}">
                            <div class="message-${userType}">
                                ${replyBlock}
                                <div class="telegram-photo-message">
                                    <img src="${message.photo}"></img>
                                    ${captionBlock}
                                </div>
                            </div>
                        </div>`);
        
    } else if (message.document) {
        messageBody = $(`<div class="message-in-chat" data-message-id="${message.id}">
                            <div class="message-${userType}">
                                ${replyBlock}
                                <div class="telegram-document-message">
                                    <a href="${message.document}"><i class="bi bi-file-earmark"></i>${message.file_name}</a>
                                    ${captionBlock}
                                </div>
                            </div>
                        </div>`);
    } else {
        messageBody = $(`<div class="message-in-chat" data-message-id="${message.id}">
                        <div class="message-${userType}">
                            ${replyBlock}
                            <div class="telegram-text-message">
                                <span>${message.text}</span>
                            </div>
                        </div>
                    </div>`);                   
    }

    messageBody.on("dblclick", setReplyMessage);

    return messageBody;
}


function appendManagerMessage(message) {
    const chat = document.querySelector("#chat-and-message");
    const messageBlock = renderChatMessage(message, "manager");

    $(chat).append(messageBlock);
    chat.scrollTop = chat.scrollHeight;
}


function appendClientMessage(message) {
    const chat = document.querySelector("#chat-and-message");
    const messageBlock = renderChatMessage(message, "client");

    $(chat).append(messageBlock);
    chat.scrollTop = chat.scrollHeight;
}


function renderNote(chat) {
    $('#aside-chats-menu').append($('<ol class="mx-0 px-0"></ol>'));
    //
    renderNoteItem(chat);
    updateAmountMessagesBadge(chat.ucid);
    //
    const requestId = new Date().getTime();
    //
    chatSocket.send(
        JSON.stringify({
            ucid: chat.ucid,
            action: 'subscribe_to_messages_in_chat',
            request_id: requestId,
        })
    );
    //
    chatSocket.send(
        JSON.stringify({
            ucid: chat.ucid,
            action: 'retrieve',
            request_id: requestId,
        })
    );
}


function renderNoteItem(chat) {
    const ol = $('#aside-chats-menu > ol');

    const firstName = chat.first_name;
    const lastMessageText = makePreviewText(chat.last_message);
    const lastMessagePreffix = 'Вы';

    const li = $(`<li class="aside-chat-tab list-group-item d-flex justify-content-between align-items-start" data-chat-ucid="${chat.ucid}">
                <div>
                    <img class="telegram-note-image" src="/static/assets/images/note.png" alt="">
                </div>
                <div class="preview-container ms-2 me-auto">
                    <div class="fw-bold">${firstName}</div>
                    <div class="preview"><strong>${lastMessagePreffix}</strong> ${lastMessageText}</div>
                </div>
                <span class="badge bg-primary rounded-pill">0</span>
            </li>`);

    $(li).click(asideChatMenuClickHandler);
    $(ol).append(li);
}


function renderChatItem(chat) {
    const ol = $('#aside-chats-menu > ol');

    const firstName = chat.first_name;
    const lastName = chat.last_name || '';
    const lastMessagePreffix = chat.last_message?.employee !== null ? 'Вы:' : 'Клиент:';
    const lastMessageText = makePreviewText(chat.last_message);

    const li = $(`<li class="aside-chat-tab list-group-item d-flex justify-content-between align-items-start" data-chat-ucid="${chat.ucid}">
                <div>
                    <img class="telegram-user-image" src="${chat.user.image}" alt="">
                </div>
                <div class="preview-container ms-2 me-auto">
                    <div class="fw-bold">${firstName} ${lastName}</div>
                    <div class="preview"><strong>${lastMessagePreffix}</strong> ${lastMessageText}</div>
                </div>
                <span class="badge bg-primary rounded-pill">${$(chat.messages).length}</span>
            </li>`);

    $(li).click(asideChatMenuClickHandler);
    $(ol).append(li);
}


function renderChatList(chats) {
    //$('#aside-chats-menu').append($('<ol class="mx-0 px-0"></ol>'));
    
    $.each(chats, function (index, chat) {
        renderChatItem(chat);
    });
}


function renderNewChatItem(ucid) {
    $.ajax({
        url: `http://127.0.0.1:8000/chat/api/v1/new_chat/${ucid}`, // TODO 
        method: 'get',
        headers: {
		    'content-type': 'application/json',
		    'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]')[0].value,
        },
        success: function (chat) {
            //
            let allChats = storageGet('allChats');
            //
            allChats[chat.ucid] = chat;
            //
            storageSet('allChats', allChats);
            //
            renderChatItem(chat);
            //
            const requestId = new Date().getTime();
            //
            chatSocket.send(
                JSON.stringify({
                    ucid: chat.ucid,
                    action: 'subscribe_to_messages_in_chat',
                    request_id: requestId,
                })
            );
            //
            chatSocket.send(
                JSON.stringify({
                    ucid: chat.ucid,
                    action: 'retrieve',
                    request_id: requestId,
                })
            );
        },
        error: function(data) {
            console.error(data);
        }
    });  
}


function renderChatMessages(messages) {
    $.each(messages, function(index, message) { 
        if (message?.staff === null) {
            appendClientMessage(message);
        } else {
            appendManagerMessage(message);
        }
    });
}


function loadChats() {
    $.ajax({
        url: 'http://127.0.0.1:8000/chat/api/v1/note', // TODO 
        method: 'get',
        headers: {
		    'content-type': 'application/json',
		    'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]')[0].value,
        },
        success: function (note) {
            //
            let allChats = {};
            //
            allChats[note.ucid] = note;
            //
            storageSet('allChats', allChats);
            //
            $('#aside-chats-menu-spiner').remove();
            //
            renderNote(note);
        },
        error: function(data) {
            console.error(data);
        }
    });

    $.ajax({
        url: 'http://127.0.0.1:8000/chat/api/v1/chats', // TODO 
        method: 'get',
        headers: {
		    'content-type': 'application/json',
		    'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]')[0].value,
        },
        success: function (rawChatsList) {
            //
            let allChats = storageGet('allChats');
            //
            $.each(rawChatsList, function (index, chat) {
                allChats[chat.ucid] = chat;
            });
            //
            storageSet('allChats', allChats);
            //
            $('#aside-chats-menu-spiner').remove();
            //
            renderChatList(rawChatsList);
        },
        error: function(data) {
            console.error(data);
        }
    });
}


function renderChat(ucid) {
    const allChats = storageGet('allChats');
    const chat = allChats[ucid];

    if (chat === undefined) {
        console.error(`chat with ucid "${ucid}" not found in local storage!`);
        return;
    }
    
    const firstName = chat.first_name;
    const lastName = chat.last_name || '';
    const username = chat.username === null ? '' : '@' + chat.username;
    
    let chatsMessages = storageGet('chatsMessages');
    let chatMessages = chatsMessages[ucid] || {};

    $('#chat-title').html(`<span><small>${firstName} ${lastName}</span> ${username}</small>`);
    //
    $('#chat-and-message').html('');
    //
    renderChatMessages(chatMessages);
    //
    storageSet('activeChatUcid', ucid);
}


function processRetrievedMessage(message) {
    const ucid = message.chat.ucid;

    let chatsMessages = storageGet('chatsMessages');
    
    if (ucid === null) {
        console.error('Retrieved message does not have a "ucid" key');
        console.error(message);
        return;
    }

    let chatMessages = chatsMessages[ucid] || {};
    chatMessages[message.id] = message;
    
    chatsMessages[ucid] = chatMessages;
    storageSet('chatsMessages', chatsMessages);
}


function updateAmountMessagesBadge(ucid) {
    const activeChatUcid = storageGet('activeChatUcid'); 

    let badge = $(`li[data-chat-ucid=${ucid}] span.badge`);

    if (activeChatUcid === ucid) {
        const chatsMessages = storageGet('chatsMessages');
        const messages = chatsMessages[ucid] || {};

        badge.removeClass('bg-danger');
        badge.addClass('bg-primary');
        badge.text(Object.keys(messages).length);
    } else {
        const unreadMessages = storageGet('unreadMessages');
        const messages = unreadMessages[ucid] || {};

        badge.removeClass('bg-primary');
        badge.addClass('bg-danger');
        badge.text(Object.keys(messages).length);
    }
} 


function updateSiteTitle() {
    const unreadMessages = storageGet('unreadMessages');
    let amountUnreadMessages = 0;

    $.each(unreadMessages, function(ucid, messages) {
        amountUnreadMessages += Object.keys(messages).length;
    })

    if (amountUnreadMessages === 0) {
        document.title = 'SUPPORT';
    } else {
        document.title = `SUPPORT (${amountUnreadMessages})`;
    }
}


function updateChatListItem(message) {
    const ucid = message.chat.ucid;

    const previewMessagePreffix = message?.staff === null ? 'Клиент:' : 'Вы:';
    const lastMessageText = makePreviewText(message);

    let preview = $(`li[data-chat-ucid=${ucid}] div.preview`);

    preview.html(`<strong>${previewMessagePreffix}</strong> ${lastMessageText}`);

    updateAmountMessagesBadge(ucid);
}


function processReceivedMessage(message) {
    const ucid = message.chat.ucid;
    const activeChatUcid = storageGet('activeChatUcid');

    let unreadMessages = storageGet('unreadMessages');
    let chatsMessages = storageGet('chatsMessages');

    if (ucid === null) {
        console.error('Received message does not have a "ucid" key');
        console.error(message);
        return;
    }
    //
    let chatMessages = chatsMessages[ucid] || {};
    chatMessages[message.id] = message;
    //
    chatsMessages[ucid] = chatMessages;
    storageSet('chatsMessages', chatsMessages);

    if (activeChatUcid === ucid) {
        if (message?.staff === null) {
            appendClientMessage(message);
        } else {
            appendManagerMessage(message);
        }
    
    } else if (message?.staff === null) {
        //
        let messages = unreadMessages[ucid] || {};
        messages[message.id] = message;
        //
        unreadMessages[ucid] = messages;
        storageSet('unreadMessages', unreadMessages);
    }

    updateChatListItem(message);
    updateSiteTitle();
}


function sendMessage(chatSocket) {
    const ucid = storageGet('activeChatUcid');
    const requestId = new Date().getTime();
    const message = $('#chat-message-input').val().trim();
    var replyToMessageId;

    replyToMessage = storageGet('replyToMessage');

    if (replyToMessage && replyToMessage.ucid === ucid) {
        replyToMessageId = replyToMessage.messageId;
        unsetReplyMessage();
    }

    if (message.length === 0) {
        return;
    } else {
        chatSocket.send(JSON.stringify({
            ucid: ucid,
            text: message,
            reply_to_message_id: replyToMessageId,
            action: "send_text_message",
            request_id: requestId,
        }));
        // Очищаем поле для ввода текста
        $('#chat-message-input').val('');
    }
}


function sendFile() {
    const ucid = storageGet('activeChatUcid');

    var fileData = $('input[type=file]').prop('files')[0];
    var formData = new FormData();

    if ($('#sendAsFileCheck').is(":checked")) {
        formData.append('document', fileData);

    } else if (fileData.type.startsWith('image')) {
        formData.append('photo', fileData);

    } else {
        formData.append('document', fileData);
    }

    replyToMessage = storageGet('replyToMessage');

    if (replyToMessage && replyToMessage.ucid === ucid) {
        formData.append('reply_to_message_id', replyToMessage.messageId);
        unsetReplyMessage();
    }

    formData.append('caption', $('#caption-input').val());
    formData.append('ucid', storageGet("activeChatUcid"));

    $.ajax({
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]')[0].value,
        },
        url: $('#uploadUrl').val(),
        cache: false,
        contentType: false,
        enctype: 'multipart/form-data',
        processData: false,
        data: formData,
        type: 'post',
    });
}


function setReplyMessage(event) {
    const ucid = storageGet('activeChatUcid');
    const lastRecord = storageGet('replyToMessage'); 
    const messageId = $(event.currentTarget).data('message-id');

    if (lastRecord && lastRecord.messageId === messageId) {
        unsetReplyMessage();
    } else {
        const chatsMessages = storageGet('chatsMessages');
        const messages = chatsMessages[ucid] || {};
        const replyMessage = $(`<div class="reply-message">
                <i class="bi bi-x-lg" onclick="unsetReplyMessage();"></i>
                 <span> ${makePreviewText(messages[messageId])}</span>
            </div>`);

        storageSet('replyToMessage', {
            ucid: ucid,
            messageId: messageId,
        });

        $('div#chat-and-message').append(replyMessage);
    }
}


function unsetReplyMessage() {
    storageSet('replyToMessage', {
        chatId: 0,
        messageId: 0,
    });
    $('div#chat-and-message div.reply-message').remove();
}


function setupData() {
    // 
    storageSet('unreadMessages', {});
    // 
    storageSet('chatsMessages', {});
    //
    storageSet('replyToMessage', {});
}


function setupEvents() {
    //
    $('li.aside-chat-tab').first().click();

    $('#send').on('click', sendFile);

    $('div#emoji-menu .emoji').click((event) => {
        const input = $('#chat-message-input');
        const text = input.val();
        input.val(text + $(event.currentTarget).text());
    })
}


$(document).ready(function () {
    const promise = new Promise(function (resolve, reject) {
        resolve();

    }).then(function () {
        setupWebSocket();

    }).then(function () {
        setupData();

    }).then(function () {
        setupEvents();

    });

    promise.then(loadChats);
});