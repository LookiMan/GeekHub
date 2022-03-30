/*



*/


var chatSocket;
var connected = false;


function setupWebSocket() {
    const requestId = new Date().getTime();
    const token = $('#jwt-token').val();

    typeof WebSocket !== 'undefined' && function connect() {
        chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/?token=${token}`);

        chatSocket.onopen = event => {
            console.info('websocket opened!');
            const chats = storageGet("allChats");

            chatSocket.send(
                JSON.stringify({
                    action: "join_to_chats",
                    request_id: requestId,
                })
            );

            $.each(chats, function (index, chat) {
                console.log('subscride', chat.ucid);

                chatSocket.send(
                    JSON.stringify({
                        ucid: chat.ucid,
                        action: "retrieve",
                        request_id: requestId,
                    })
                );
                chatSocket.send(
                    JSON.stringify({
                        ucid: chat.ucid,
                        action: "subscribe_to_messages_in_chat",
                        request_id: requestId,
                    })
                );
            });
        };

        chatSocket.onmessage = event => {
            const data = JSON.parse(event.data);

            switch (data.action) {
                case "create_new_chat":
                    renderNewChatItem(data.telegram_chat_id);

                case "retrieve":
                    console.log(data.data)
                    for (let message of data?.data?.messages || []) {
                        processRetrievedMessage(message);
                        console.log(data.action, data.data);
                    }
                    break;
                case "create":
                    processReceivedMessage(data.data);
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


function storageSet(key, object) {
	return localStorage.getItem(key, JSON.stringify(object));
}


function storageGet(key) {
    const raw = localStorage.getItem(key);
	return JSON.parse(raw);
}


function asideChatMenuClickHandler(event) {
    let chats = storageGet("chatsMessages");
    let receivedMessages = storageGet("receivedMessages");
    let target = $(event.currentTarget);

    const ucid = $(target).data("chat-ucid");

    if (ucid === null) {
        console.error("Attribute 'data-chat-ucid' not found in target element!");
        return;
    } else {
        loadChatMessages(ucid);
    }

    $("li.active-aside-chat-menu-tab")?.removeClass("active-aside-chat-menu-tab");
    $(target).addClass("active-aside-chat-menu-tab");

    let badge = $(`li[data-chat-ucid=${ucid}] span.badge`);
    badge.removeClass("bg-danger");
    badge.addClass("bg-primary");
    badge.text($(chats[ucid]).length);

    delete receivedMessages[ucid];
    storageSet("receivedMessages", receivedMessages);
}


function renderChatMessage(message, userType) {
    const captionBlock = message.caption ? `<div class="telegram-text-message">${message.caption}</div>` : "";
    var replyBlock;

    if (message.reply_to_message) {
        replyBlock = `<div class="telegram-reply-message" data-target-message-id="${message.reply_to_message.id}">
                            ${makePreviewText(message.reply_to_message)}
                        </div>`;
    } else {
        replyBlock = '';
    }

    if (message.photo) {  
        return $(`<div class="message-in-chat" data-message-id="${message.id}">
                            <div class="message-${userType}">
                                ${replyBlock}
                                <div class="telegram-photo-message">
                                    <img src="${message.photo}"></img>
                                    ${captionBlock}
                                </div>
                            </div>
                        </div>`);
        
    } else if (message.document) {
        return $(`<div class="message-in-chat" data-message-id="${message.id}">
                            <div class="message-${userType}">
                                ${replyBlock}
                                <div class="telegram-document-message">
                                    <a href="${message.document}"><i class="bi bi-file-earmark"></i>${message.file_name}</a>
                                    ${captionBlock}
                                </div>
                            </div>
                        </div>`);
    } else {
        return $(`<div class="message-in-chat" data-message-id="${message.id}">
                        <div class="message-${userType}">
                            ${replyBlock}
                            <div class="telegram-text-message">
                                <span>${message.text}</span>
                            </div>
                        </div>
                    </div>`);                   
    }
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


function renderChatItem(chat) {
    const ol = $('#aside-chats-menu > ol');

    const firstName = chat.first_name;
    const lastName = chat.last_name || '';
    const lastMessagePreffix = chat.last_message.employee !== null ? 'Вы:' : 'Клиент:';
    const lastMessageText = makePreviewText(chat.last_message);

    const li = $(`<li class="aside-chat-tab list-group-item d-flex justify-content-between align-items-start" data-chat-ucid="${chat.ucid}">
                <div>
                    <img class="telegram-user-image" src="${chat.client.image_url}" alt="">
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
    $('#aside-chats-menu').append($('<ol class="mx-0 px-0"></ol>'));

    $.each(chats, function (index, chat) {
        renderChatItem(chat);
    });
}


function renderNewChatItem(chat_id) {
    $.ajax({
        url: `http://127.0.0.1:8000/chat/api/v1/chat/${chat_id}`, // TODO 
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
                    action: "subscribe_to_messages_in_chat",
                    request_id: requestId,
                })
            );
            //
            chatSocket.send(
                JSON.stringify({
                    ucid: chat.ucid,
                    action: "retrieve",
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
        if (message?.employee === null) {
            appendClientMessage(message);
        } else {
            appendManagerMessage(message);
        }
    });
}


function loadChats() {
    $.ajax({
        url: 'http://127.0.0.1:8000/chat/api/v1/chats', // TODO 
        method: 'get',
        headers: {
		    'content-type': 'application/json',
		    'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]')[0].value,
        },
        success: function (rawChatsList) {
            //
            let allChats = {};
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


function loadChatMessages(ucid) {
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


function updateChatListItem(message) {
    const ucid = message.chat.ucid;
    const activeChatUcid = storageGet('activeChatUcid');
    const previewMessagePreffix = message?.employee === null ? 'Клиент:' : 'Вы:';
    const lastMessageText = makePreviewText(message);
    
    const receivedMessages = storageGet('receivedMessages');
    const chatsMessages = storageGet('chatsMessages');

    let badge = $(`li[data-chat-ucid=${ucid}] span.badge`);
    let preview = $(`li[data-chat-ucid=${ucid}] div.preview`);

    if (activeChatUcid === ucid) {
        badge.removeClass('bg-danger');
        badge.addClass('bg-primary');
        badge.text($(chatsMessages[ucid]).length);
    } else {
        badge.removeClass('bg-primary');
        badge.addClass('bg-danger');
        badge.text($(receivedMessages[ucid]).length);
    }

    preview.html(`<strong>${previewMessagePreffix}</strong> ${lastMessageText}`);
}


function processReceivedMessage(message) {
    const ucid = message.chat.ucid;
    const activeChatUcid = storageGet('activeChatUcid');

    let receivedMessages = storageGet('receivedMessages');
    let chatsMessages = storageGet("chatsMessages");

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
        if (message?.employee === null) {
            appendClientMessage(message);
        } else {
            appendManagerMessage(message);
        }
    
    } else if (message.employee === null) {
        //
        let messages = receivedMessages[ucid] || {};
        messages[message.id] = message;
        //
        receivedMessages[ucid] = messages;
        storageSet('receivedMessages', receivedMessages);
    }

    updateChatListItem(message);
}


function sendMessage(chatSocket) {
    const ucid = storageGet('activeChatUcid');
    const requestId = new Date().getTime();
    const message = $('#chat-message-input').val().trim();

    if (message.length === 0) {
        return;
    } else {
        chatSocket.send(JSON.stringify({
            ucid: ucid,
            message: message,
            action: "send_text_message",
            request_id: requestId,
        }));
        // Очищаем поле для ввода текста
        $('#chat-message-input').val('');
    }
}


function setupData() {
    // 
    storageSet('receivedMessages', {});
    // 
    storageSet('chatsMessages', {});
}


function setupEvents() {
    //
    $('li.aside-chat-tab').first().click();

    $('input[type=file]').change(function(){
        console.log(this.files);
    });

    $('#send').on('click', function() { 
        const imageMimeTypes = ["image/png", "image/jpeg"];

        var file_data = $('input[type=file]').prop('files')[0];
        var form_data = new FormData();

        if ($('#sendAsFileCheck').is(":checked")) {
            form_data.append('document', file_data);

        } else if ($.inArray(file_data.type, imageMimeTypes) != -1) {
            form_data.append('photo', file_data);

        } else {
            form_data.append('document', file_data);
        }

        form_data.append('caption', $('#caption-input').val());
        form_data.append('chat_id', storageGet("activeChatUcid"));

        $.ajax({
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]')[0].value,
            },
            url: $('#uploadUrl').val(),
            cache: false,
            contentType: false,
            enctype: 'multipart/form-data',
            processData: false,
            data: form_data,
            type: 'post',
        });
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