import { updateSiteTitle } from './components/site-title.js';
import { renderNote, renderChatItem, renderChatList, updateChatListItem } from './components/side-chat-menu.js';
import { renderClientMessage, renderManagerMessage, unsetReplyMessage } from './components/chat.js';
import { updateDropdownMenu } from './components/chat-dropdown-menu.js';
import { openEmojiMenu, closeEmojiMenu, toggleEmojiMenu, emojiMenuToggleStates } from './components/emoji.js';
import { storageSet, storageGet, dropdownToggle, previewImage } from '../utils.js';


let chatSocket;

function setupWebSocket() {
    const requestId = new Date().getTime();
    const token = $('#jwt-token').val();
    let webSocketIsConnected = false;

    chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/?token=${token}`);

    (function connect() {
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
                const { ucid } = chat; 
                console.log('subscride', ucid);

                chatSocket.send(
                    JSON.stringify({
                        ucid,
                        action: 'retrieve',
                        request_id: requestId,
                    })
                );
                chatSocket.send(
                    JSON.stringify({
                        ucid,
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
                case 'createNewChat':
                    console.log(data);
                    createNewChat(data.data.ucid);

                case 'retrieve':
                    console.log(data.data)
                    for (const message of data?.data?.messages || []) {
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

        chatSocket.onerror = error => {
            console.error(error);
            chatSocket.onclose = null;
            webSocketIsConnected = false;
            chatSocket.close();
            connect();
        };

        chatSocket.onclose = event => {
            console.info(`WebSocket closed with code ${event.code}! ${event.reason}`);
            webSocketIsConnected = false;
            if (event.wasClean) {
                return;
            }
            connect();
        };
    })();

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

function createNewChat(ucid) {
    $.ajax({
        url: `http://127.0.0.1:8000/chat/api/v1/new_chat/${ucid}`, // TODO 
        method: 'get',
        headers: {
		    'content-type': 'application/json',
		    'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]')[0].value,
        },
        success: function (chat) {
            const { ucid } = chat;
            //
            const allChats = storageGet('allChats');
            //
            allChats[ucid] = chat;
            //
            storageSet('allChats', allChats);
            //
            renderChatItem(chat);
            //
            const requestId = new Date().getTime();
            //
            chatSocket.send(
                JSON.stringify({
                    ucid,
                    action: 'subscribe_to_messages_in_chat',
                    request_id: requestId,
                })
            );
            //
            chatSocket.send(
                JSON.stringify({
                    ucid,
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

async function loadNote() {
    await $.ajax({
        url: 'http://127.0.0.1:8000/chat/api/v1/note', // TODO 
        method: 'get',
        headers: {
            'content-type': 'application/json',
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]')[0].value,
        },
        success: function (note) {
            const chats = {};
            chats[note.ucid] = note;
            //
            storageSet('allChats', chats);
            //
            renderNote(note);
        },
        error: function (error) {
            console.log(error);
        }
    });
}

async function loadChats() {
    await $.ajax({
        url: 'http://127.0.0.1:8000/chat/api/v1/chats', // TODO 
        method: 'get',
        headers: {
            'content-type': 'application/json',
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]')[0].value,
        },
        success: function (rawChatsList) {
            //
            const allChats = storageGet('allChats');
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
}

async function loadSideChatsMenu() {
    await loadNote();
    await loadChats();
}

function processRetrievedMessage(message) {
    const { ucid } = message.chat || {};
    const chatsMessages = storageGet('chatsMessages');
    
    if (ucid === null) {
        console.error('Retrieved message does not have a "ucid" key');
        console.error(message);
        return;
    }

    const chatMessages = chatsMessages[ucid] || {};
    chatMessages[message.id] = message;
    
    chatsMessages[ucid] = chatMessages;
    storageSet('chatsMessages', chatsMessages);
}

function processReceivedMessage(message) {
    const { ucid } = message.chat || {};
    const activeChatUcid = storageGet('activeChatUcid');

    const unreadMessages = storageGet('unreadMessages');
    const chatsMessages = storageGet('chatsMessages');

    if (ucid === null) {
        console.error('Received message does not have a "ucid" key');
        console.error(message);
        return;
    }
    //
    const chatMessages = chatsMessages[ucid] || {};
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
        const messages = unreadMessages[ucid] || {};
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
    const text = $('#chat-message-input').val().trim();
    const replyToMessage = storageGet('replyToMessage');

    let replyToMessageId;

    if (replyToMessage && replyToMessage.ucid === ucid) {
        replyToMessageId = replyToMessage.messageId;
        unsetReplyMessage();
    }

    if (text.length === 0) {
        return;
    }

    const request = JSON.stringify({
        ucid,
        text,
        reply_to_message_id: replyToMessageId,
        action: 'send_text_message',
        request_id: requestId,
    })

    console.log(request);

    chatSocket.send(request);
    // Очищаем поле для ввода текста
    $('#chat-message-input').val('');
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

    const formData = new FormData();
    const fileData = $('#upload-file-modal-form input[type=file]').prop('files')[0];

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

    const formData = new FormData();
    const fileData = $('#upload-image-modal-form input[type=file]').prop('files')[0];

    if (replyToMessage && replyToMessage.ucid === ucid) {
        formData.append('reply_to_message_id', replyToMessage.messageId);
        unsetReplyMessage();
    }

    formData.append('caption', $('#upload-image-modal-form .image-caption-input').val());
    formData.append('ucid', storageGet("activeChatUcid"));
    formData.append('photo', fileData);

    sendFormData(formData);
}

function blockOrUnblockUser(event) {
    const target = $(event.currentTarget);
    const userId = $(target).data('user-id');
    const url = $(target).data('url').replace('/0/', `/${userId}/`);

    $.ajax({
        url,
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]')[0].value,
        },
        success: function (response) {
            if (!response.success) {
                alert(`Упс! Что-то пошло не так...\n${response.description}`);
            } else {
                const chats = storageGet('allChats');

                $.each(chats, function (key, value) {
                    const { user } = value;
                    if (user && user.id === response.user_id) {
                        user.is_blocked = response.is_blocked;
                        updateDropdownMenu(user);

                        value.user = user;
                        chats[key] = value;

                        storageSet('allChats', chats);
                        return;
                    }
                });
            }
        },
        error: function(data) {
            console.error(data);
        }
    });
}

function blockUser(event) {
    blockOrUnblockUser(event);
}

function unblockUser(event) {
    blockOrUnblockUser(event)
}

function setupEvents() {
    //
    $('li.aside-chat-tab').first().click();

    $('#upload-file-modal-form button#send-file').on('click', sendFile);
    $('#upload-image-modal-form button#send-image').on('click', sendImage);
    $('.input-area .emoji-button').on('click', toggleEmojiMenu);
    $('#block-user').on('click', blockUser);
    $('#unblock-user').on('click', unblockUser);
    $('#chat-more-actions').on('click', dropdownToggle);
    $('#form-image').on('change', previewImage);

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
        cache: true,
        contentType: false,
        type: 'get',
        success: function (html) {
            $('#emoji-spinner').remove();
            $('#emoji-menu').html(html);
            $('#emoji-menu .emoji').click((event) => {
                const input = $('#chat-message-input');
                input.val(input.val() + $(event.currentTarget).text()).focus();
            })    
        },
        error: function(data) {
            console.error(data);
        },
    });
}

$(document).ready(async function () {
    await loadSideChatsMenu();
    await setupWebSocket();
    await setupEvents();
});
