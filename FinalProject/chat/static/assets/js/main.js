/*



*/


var chatSocket;
var connected = false;

const emojiMenuToggleStates = {
    open: 1,
    close: 2,
}


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
        return '[нет сообщений]';
    }
}


function makeReplyText(message) {
    const username = message?.staff ? "Вы" : message.user.first_name;
    const html = `<div class="username"><strong>${username}</strong></div>`;

    if (message.photo) {
        return html + `<div class="content">[фото 🖼]</div>`;
    } else if (message.document) {
        return html + `<div class="content">[файл 📁] ${message.file_name}</div>`;
    } else if (message.text) {
        return html + `<div class="content">${message.text}</div>`;
    } else {
        return html + '<div class="content">[сообщение удалено]</div>';
    }
}


function renderChatMessage(message, userType) {
    /* userType = "manager" || "client" */

    const captionBlock = message.caption ? `<div class="telegram-text-message">${message.caption}</div>` : "";

    var messageHtml = `<div class="message-in-chat" data-message-id="${message.id}">
                        <div class="message message-${userType}">`;

    if (message.reply_to_message) {
        messageHtml += `<div class="telegram-reply-message" data-target-message-id="${message.reply_to_message.id}">
                            ${makeReplyText(message.reply_to_message)}
                        </div>`;
    }

    if (message.photo) {  
        messageHtml += `<div class="telegram-photo-message">
                            <img src="${message.photo}"></img>
                            ${captionBlock}
                        </div>`;
        
    } else if (message.document) {
        messageHtml += `<div class="telegram-document-message">
                            <a href="${message.document}"><i class="bi bi-file-earmark"></i>${message.file_name}</a>
                            ${captionBlock}
                        </div>`;
    } else {
        messageHtml += `<div class="telegram-text-message">
                            <span>${message.text}</span>
                        </div>`;                   
    }

    messageHtml += `<div class="message-metadata">
                        <span class="time time-${userType === "manager" ? "right" : "left"}">${message.created_at_short}</span>
                    </div>
                </div>
            </div>`;

    messageDiv = $(messageHtml).on("dblclick", setReplyMessage);

    return messageDiv;
}


function renderManagerMessage(message) {
    const chat = document.querySelector("#chat-and-message");
    const messageBlock = renderChatMessage(message, "manager");

    $(chat).append(messageBlock);
    chat.scrollTop = chat.scrollHeight;
}


function renderClientMessage(message) {
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
    const lastMessageText = makePreviewText(chat.last_message);
    const lastMessagePreffix = chat.last_message?.employee === null ? 'Клиент:' : 'Вы:';

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
            renderClientMessage(message);
        } else {
            renderManagerMessage(message);
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
            $('#aside-chats-menu-spinner').remove();
            //
            renderNote(note);

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
                    $('#aside-chats-menu-spinner').remove();
                    //
                    renderChatList(rawChatsList);
                },
                error: function(data) {
                    console.error(data);
                }
            });
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

    $('#chat-title').html(`<span class="chat-name">${firstName} ${lastName}</span><div><span class="username">${username}</span></div>`);
    //
    let image = $('#chat .control-panel img.telegram-user-image')[0];
    // TODO:
    if (chat.user) {
        image.src = chat.user.image;
        //
        if (chat.user.is_blocked === true) {
            let blockItem = $('#block-user');
            let unblockItem = $('#unblock-user');
            unblockItem.attr('data-user-id', chat.user.id);
            unblockItem.parent().removeClass('d-none');
            blockItem.parent().addClass('d-none');
        } else {
            let blockItem = $('#block-user');
            let unblockItem = $('#unblock-user');
            blockItem.attr('data-user-id', chat.user.id);
            blockItem.parent().removeClass('d-none');
            unblockItem.parent().addClass('d-none');
        }
    } else {
        image.src = "/static/assets/images/note.png";
    }
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
            renderClientMessage(message);
        } else {
            renderManagerMessage(message);
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


function sendFormData(formData) {
    $.ajax({
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]')[0].value,
        },
        url: $('#upload-url').val(),
        cache: false,
        contentType: false,
        enctype: 'multipart/form-data',
        processData: false,
        data: formData,
        type: 'post',
    });
}


function sendFile() {
    const ucid = storageGet('activeChatUcid');
    const replyToMessage = storageGet('replyToMessage');

    var formData = new FormData();
    var fileData = $('#upload-file-modal-form input[type=file]').prop('files')[0];

    if (replyToMessage && replyToMessage.ucid === ucid) {
        formData.append('reply_to_message_id', replyToMessage.messageId);
        unsetReplyMessage();
    }

    formData.append('caption', $('#upload-file-modal-form .file-caption-input').val());
    formData.append('ucid', storageGet("activeChatUcid"));
    formData.append('document', fileData);

    sendFormData(formData);
}


function sendImage() {
    const ucid = storageGet('activeChatUcid');
    const replyToMessage = storageGet('replyToMessage');

    var formData = new FormData();
    var fileData = $('#upload-image-modal-form input[type=file]').prop('files')[0];

    if (replyToMessage && replyToMessage.ucid === ucid) {
        formData.append('reply_to_message_id', replyToMessage.messageId);
        unsetReplyMessage();
    }

    formData.append('caption', $('#upload-image-modal-form .image-caption-input').val());
    formData.append('ucid', storageGet("activeChatUcid"));
    formData.append('photo', fileData);

    sendFormData(formData);
}


function setReplyMessage(event) {
    const ucid = storageGet('activeChatUcid');
    const lastRecord = storageGet('replyToMessage'); 
    const messageId = $(event.currentTarget).data('message-id');

    if (lastRecord && lastRecord.messageId === messageId) {
        unsetReplyMessage();
    } else {
        unsetReplyMessage();
        const chatsMessages = storageGet('chatsMessages');
        const messages = chatsMessages[ucid] || {};
        const replyMessage = $(`<div class="reply-message">
                <button class="button" onclick="unsetReplyMessage();">
                    <i class="bi bi-x-lg"></i>
                </button>
                <span> ${makePreviewText(messages[messageId])}</span>
            </div>`);

        storageSet('replyToMessage', {
            ucid: ucid,
            messageId: messageId,
        });

        $(event.currentTarget).addClass('selected-message');
        $('div#chat-and-message').append(replyMessage);
    }
}


function unsetReplyMessage() {
    try {
        storageSet('replyToMessage', {
            chatId: 0,
            messageId: 0,
        });
        $('div#chat-and-message div.selected-message').removeClass('selected-message');
        $('div#chat-and-message div.reply-message').remove();
    } catch (exc) {
        alert(`Ууупс! Что-то пошло не так!\nОшибка: ${exc}`);
    } 
}


function openEmojiMenu() {
    $('#emoji-menu').removeClass('d-none');
    $('#chat').removeClass('col-9');
    $('#chat').addClass('col-6');
    $('div.input-area .emoji-button').addClass('active-emoji');
}


function closeEmojiMenu() {
    $('#emoji-menu').addClass('d-none');
    $('#chat').removeClass('col-6');
    $('#chat').addClass('col-9');
    $('div.input-area .emoji-button').removeClass('active-emoji');
}


function toggleEmojiMenu() {
    const emojiMenuState = storageGet('emojiMenuState');

    if (emojiMenuState === null || emojiMenuState === emojiMenuToggleStates.close) {
        openEmojiMenu();
        storageSet('emojiMenuState', emojiMenuToggleStates.open);

    } else if (emojiMenuState === emojiMenuToggleStates.open) {
        closeEmojiMenu();
        storageSet('emojiMenuState', emojiMenuToggleStates.close);
    } 
}


function preview(image) { 
    var previewImage = $("#previewImage")[0];
    previewImage.src = URL.createObjectURL(image.files[0]);
}


function dropdownToggle() {
    $("#chat-more-actions-menu").toggleClass("d-block");
}


function blockUser(event) {
    const target = $(event.currentTarget);
    const user_id = $(target).data('user-id');
    const url = $(target).data('url').replace('/0/', `/${user_id}/`);

    $.ajax({
        url: url,
        method: 'get',
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]')[0].value,
        },
        success: function (response) {
            console.log(response);
        },
        error: function(data) {
            console.error(data);
        }
    });
}


function unblockUser(event) {
    const target = $(event.currentTarget);
    const user_id = $(target).data('user-id');
    const url = $(target).data('url').replace('/0/', `/${user_id}/`);

    $.ajax({
        url: url,
        method: 'get',
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]')[0].value,
        },
        success: function (response) {
            console.log(response);
        },
        error: function(data) {
            console.error(data);
        }
    });
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

    $('#upload-file-modal-form button#send-file').on('click', sendFile);
    $('#upload-image-modal-form button#send-image').on('click', sendImage);
    $('.input-area .emoji-button').on('click', toggleEmojiMenu);
    $('#block-user').on('click', blockUser);
    $('#unblock-user').on('click', unblockUser);

    const emojiMenuState = storageGet('emojiMenuState');

    if (emojiMenuState === null || emojiMenuState === emojiMenuToggleStates.close) {
        closeEmojiMenu();
    } else {
        openEmojiMenu();
    }

    $.ajax({
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]')[0].value,
        },
        url: 'http://127.0.0.1:8000/chat/api/v1/emoji',
        cache: false,
        contentType: false,
        type: 'get',
        success: function (html) {
            $('#emoji-spinner').remove();
            $('#emoji-menu').html(html);
            $('#emoji-menu .emoji').click((event) => {
                const input = $('#chat-message-input');
                input.val(input.val() + $(event.currentTarget).text());
                input.focus();
            })    
        },
        error: function(data) {
            console.error(data);
        },
    });
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
