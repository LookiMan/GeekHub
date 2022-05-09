import { updateSiteTitle } from './components/site-title.js';
import { renderNote, renderChatItem, renderChatList, openFirstChat, updateChatListItem } from './components/side-chat-menu.js';
import { renderClientMessage, renderManagerMessage, updateChatMessage, unsetReplyMessage } from './components/chat.js';
import { updateDropdownMenu } from './components/chat-dropdown-menu.js';
import { openEmojiMenu, closeEmojiMenu, toggleEmojiMenu, emojiMenuToggleStates } from './components/emoji.js';
import { storageSet, storageGet, dropdownToggle, previewImage } from '../utils.js';


let chatSocket;

class BackendURLS {
    static csrfmiddlewaretoken() {
        return $('input[name="csrfmiddlewaretoken"]').val();
    } 
    static jwtToken() {
        $('input[name="jwt-token"]').val();
    }
    static newChat(ucid) {
        return $('input[name="new-chat-url"]').val().replace('/0/', `/${ucid}/`);
    }
    static note() {
        return $('input[name="note-url"]').val();
    }
    static chats() {
        return $('input[name="chats-url"]').val();
    }
    static fileUpload() {
        return $('input[name="file-upload-url"]').val();
    }
    static emoji() {
        return $('input[name="emoji-url"]').val();
    }
}

function setupWebSocket() {
    const requestId = new Date().getTime();
    const token = BackendURLS.jwtToken()
    let webSocketIsConnected = false;

    chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/?token=${token}`);

    (function connect() {
        chatSocket.onopen = event => {
            const chats = storageGet('allChats');

            chatSocket.send(
                JSON.stringify({
                    action: 'join_to_chats',
                    request_id: requestId,
                })
            );

            $.each(chats, function (index, chat) {
                const { ucid } = chat; 

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

            switch (data.action) {
                case 'createNewChat':
                    createNewChat(data.data.ucid);
                case 'retrieve':
                    console.log(data.action, data.data.messages);
                    for (const message of data?.data?.messages || []) {
                        processRetrievedMessage(message);
                    }
                    break;
                case 'create':
                    processCreatedMessage(data.data);
                    break;
                case 'update':
                    processUpdatedMessage(data.data)
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
        url: BackendURLS.newChat(ucid),
        headers: {
		    'content-type': 'application/json',
		    'X-CSRFToken': BackendURLS.csrfmiddlewaretoken(),
        },
        success: function (chat) {
            const requestId = new Date().getTime();
            const { ucid } = chat;
            const allChats = storageGet('allChats');
            
            allChats[ucid] = chat;
            
            storageSet('allChats', allChats);
            renderChatItem(chat);

            chatSocket.send(
                JSON.stringify({
                    ucid,
                    action: 'subscribe_to_messages_in_chat',
                    request_id: requestId,
                })
            );
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
        url: BackendURLS.note(),
        headers: {
            'content-type': 'application/json',
            'X-CSRFToken': BackendURLS.csrfmiddlewaretoken(),
        },
        success: function (note) {
            const chats = {};
            chats[note.ucid] = note;
            
            storageSet('allChats', chats);
            renderNote(note);
        },
        error: function (error) {
            console.error(error);
        }
    });
}

async function loadChats() {
    await $.ajax({
        url: BackendURLS.chats(),
        headers: {
            'content-type': 'application/json',
            'X-CSRFToken': BackendURLS.csrfmiddlewaretoken(),
        },
        success: function (rawChatsList) {
            const allChats = storageGet('allChats');
            
            $.each(rawChatsList, function (index, chat) {
                allChats[chat.ucid] = chat;
            });
            
            $('#aside-chats-menu-spinner').remove();  
            storageSet('allChats', allChats);
            renderChatList(rawChatsList);
        },
        error: function(error) {
            console.error(error);
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
    const activeChatUcid = storageGet('activeChatUcid');
    
    if (!ucid) {
        console.error('Полученное сообщение неимет атрибута "ucid"');
        console.error(message);
        return;
    }

    const chatMessages = chatsMessages[ucid] || {};
    chatMessages[message.id] = message;
    chatsMessages[ucid] = chatMessages;
    storageSet('chatsMessages', chatsMessages);

    if (Number(activeChatUcid) === ucid) {
        if (!message.staff) {
            renderClientMessage(message);
        } else {
            renderManagerMessage(message);
        }
    }
}

function processCreatedMessage(message) {
    const { ucid } = message.chat || {};
    const activeChatUcid = storageGet('activeChatUcid');
    const unreadMessages = storageGet('unreadMessages');
    const chatsMessages = storageGet('chatsMessages');

    if (!ucid) {
        console.error('Полученное сообщение неимет атрибута "ucid"');
        console.error(message);
        return;
    }

    const chatMessages = chatsMessages[ucid] || {};
    chatMessages[message.id] = message;
    chatsMessages[ucid] = chatMessages;
    storageSet('chatsMessages', chatsMessages);

    if (activeChatUcid === ucid) {
        if (!message.staff) {
            renderClientMessage(message);
        } else {
            renderManagerMessage(message);
        }
    
    } else if (!message.staff) {
        const messages = unreadMessages[ucid] || {};
        messages[message.id] = message;  
        unreadMessages[ucid] = messages;
        storageSet('unreadMessages', unreadMessages);
    }

    updateChatListItem(message);
    updateSiteTitle();
}

function processUpdatedMessage(message) {
    const { ucid } = message.chat || {};
    const activeChatUcid = storageGet('activeChatUcid');
    const chatsMessages = storageGet('chatsMessages');

    if (!ucid) {
        console.error('Полученное сообщение неимет атрибута "ucid"');
        console.error(message);
        return;
    }
    
    const chatMessages = chatsMessages[ucid] || {};
    chatMessages[message.id] = message;
    chatsMessages[ucid] = chatMessages;
    storageSet('chatsMessages', chatsMessages);

    if (activeChatUcid === ucid) {
        updateChatMessage(message);
    }
    updateChatListItem(message);
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

    chatSocket.send(
        JSON.stringify({
            ucid,
            text,
            reply_to_message_id: replyToMessageId,
            action: 'send_text_message',
            request_id: requestId,
        })
    );
    $('#chat-message-input').val('');
}

function sendFormData(formData) {
    $.ajax({
        headers: {
            'X-CSRFToken': BackendURLS.csrfmiddlewaretoken(),
        },
        url: BackendURLS.fileUpload(),
        cache: false,
        contentType: false,
        enctype: 'multipart/form-data',
        processData: false,
        data: formData,
        type: 'post',
        success: function (response) {
            // TODO:
        },
        error: function (error) {
            console.error(error);
        }
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

function changeBlockStateUser(event) {
    const target = $(event.currentTarget);
    const userId = $(target).data('user-id');
    const url = $(target).data('url').replace('/0/', `/${userId}/`);

    $.ajax({
        url,
        headers: {
            'X-CSRFToken': BackendURLS.csrfmiddlewaretoken(),
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
        error: function(error) {
            console.error(error);
        }
    });
}

function blockUser(event) {
    changeBlockStateUser(event);
}

function unblockUser(event) {
    changeBlockStateUser(event)
}

function archiveChat(event) {
    const target = $(event.currentTarget);
    const ucid = storageGet('activeChatUcid');

    if (!ucid) {
        alert('Не удалось получить "ucid" текущего чата для архивации');
        return;
    }

    const url = $(target).data('url').replace('/0/', `/${ucid}/`);

    $.ajax({
        url,
        headers: {
            'X-CSRFToken': BackendURLS.csrfmiddlewaretoken(),
        },
        success: function (response) {
            if (!response.success) {
                alert(`Упс! Что-то пошло не так...\n${response.description}`);
            } else {
                const allChats = storageGet('allChats');
                const chatsMessages = storageGet('chatsMessages');
                const { ucid } = response;

                if (!ucid) {
                    console.error('Ответ не имеет атрибута "ucid"');
                    console.error(response);
                    return;
                }
                
                try {
                    delete allChats[ucid];
                    delete chatsMessages[ucid];
                } catch (error) {
                    console.error(error);
                }

                $(`li[data-chat-ucid="${ucid}"]`).remove();
                
                storageSet('allChats', allChats);
                storageSet('chatsMessages', chatsMessages);
                openFirstChat();
            }
        },
        error: function(error) {
            console.error(error);
        }
    });
}

function setupEvents() {
    $('#upload-file-modal-form button#send-file').on('click', sendFile);
    $('#upload-image-modal-form button#send-image').on('click', sendImage);
    $('.input-area .emoji-button').on('click', toggleEmojiMenu);
    $('#block-user').on('click', blockUser);
    $('#unblock-user').on('click', unblockUser);
    $('#archive-chat').on('click', archiveChat);
    $('#chat-more-actions').on('click', dropdownToggle);
    $('#form-image').on('change', previewImage);

    const emojiMenuState = storageGet('emojiMenuState');

    if (!emojiMenuState || emojiMenuState === emojiMenuToggleStates.close) {
        closeEmojiMenu();
    } else {
        openEmojiMenu();
    }

    $.ajax({
        headers: {
            'X-CSRFToken': BackendURLS.csrfmiddlewaretoken(),
        },
        url: BackendURLS.emoji(),
        cache: true,
        contentType: false,
        type: 'get',
        success: function (html) {
            $('#emoji-spinner').remove();
            $('#emoji-menu').html(html);
            $('#emoji-menu .emoji').click((event) => {
                const input = $('#chat-message-input');
                if (!input.prop('disabled')) {
                    input.val(input.val() + $(event.currentTarget).text()).focus();
                }
            })    
        },
        error: function(error) {
            console.error(error);
        },
    });   
}

$(document).ready(async function () {
    await loadSideChatsMenu();
    await setupWebSocket();
    await setupEvents();

    openFirstChat();
});
