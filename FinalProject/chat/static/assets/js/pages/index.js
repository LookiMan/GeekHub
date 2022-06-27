import { updateSiteTitle } from './components/site-title.js';
import { renderNote, renderChatItem, renderChatList, openFirstChat, updateChatListItem } from './components/side-chat-menu.js';
import { renderClientMessage, renderManagerMessage, updateChatMessage } from './components/chat.js';
import { setEditMessage, unsetEditMessage, setReplyMessage, unsetReplyMessage } from './components/chat.js';
import { updateDropdownMenu } from './components/chat-dropdown-menu.js';
import { openEmojiMenu, closeEmojiMenu, toggleEmojiMenu, emojiMenuToggleStates } from './components/emoji.js';
import { storageSet, storageGet, dropdownToggle, previewImage } from '../utils.js';
import { clearFileModalForm, clearImageModalForm, copyToClipboard, showError, BackendURLS } from '../utils.js'


let chatSocket;

function setupWebSocket() {
    const requestId = new Date().getTime();
    const token = BackendURLS.jwtToken();
    const ws_scheme = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    let webSocketIsConnected = false;

    chatSocket = new WebSocket(`${ws_scheme}${window.location.host}/ws/chat/?token=${token}`);

    (function connect() {
        chatSocket.onopen = event => {
            const chats = storageGet('allChats');

            chatSocket.send(
                JSON.stringify({
                    action: 'join_to_chats',
                    request_id: requestId,
                })
            );

            $.each(chats, (index, chat) => {
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
                case 'error':
                    showError(data.data);
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
        const keyId = event.keyCode || event.which || event.key || 0;

        if (keyId === 13) {
            const message = $(event.currentTarget).val().trim();

            if (message.length > 0) {
                event.preventDefault();
                if (Object.keys(storageGet('editMessage')).length === 0) {
                    sendMessage(chatSocket);
                } else {
                    editMessage(chatSocket);
                }
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
        error: function(error) {
            showError(error);
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
            showError(error);
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
            showError(error);
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
        showError('Полученное сообщение не имеет атрибута "ucid"');
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
        showError('Полученное сообщение неимет атрибута "ucid"');
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
        showError('Полученное сообщение неимет атрибута "ucid"');
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

    if (text.length === 0) {
        return;
    }

    if (replyToMessage && replyToMessage.ucid === ucid) {
        replyToMessageId = replyToMessage.messageId;
        unsetReplyMessage();
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

function editMessage(chatSocket) {
    const ucid = storageGet('activeChatUcid');
    const requestId = new Date().getTime();
    const text = $('#chat-message-input').val().trim();
    const editMessage = storageGet('editMessage');

    let editMessageId;

    if (text.length === 0) {
        return;
    }

    if (editMessage && editMessage.ucid === ucid) {
        editMessageId = editMessage.messageId;
        unsetEditMessage();
    }

    chatSocket.send(
        JSON.stringify({
            ucid,
            text,
            message_id: editMessageId,
            action: 'edit_text_message',
            request_id: requestId,
        })
    );
    $('#chat-message-input').val('');   
}

function sendFormData(formData) {
    formData.append('message_id', new Date().getTime());
    formData.append('date', (new Date().getTime() / 1000).toFixed());

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
            $('.modal.fade.show').modal('hide');
            $('.modal-upload-spinner.active').addClass('d-none');
        },
        error: function (error) {
            showError(error);
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
    formData.append('file_name', fileData.name);

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
    formData.append('file_name', fileData.name);

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
        method: "PUT",
        success: function (response) {
            if (!response.success) {
                showError(`Упс! Что-то пошло не так...\n${response.description}`);
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
                        $('#chat-more-actions-menu').removeClass('d-block');
                        return;
                    }
                });
            }
        },
        error: function(error) {
            showError(error);
        }
    });
}

function blockUser(event) {
    changeBlockStateUser(event);
}

function unblockUser(event) {
    changeBlockStateUser(event)
}

function deleteMessage(messageId) {
    $.ajax({
        url: BackendURLS.deleteMessage(messageId),
        headers: {
            'X-CSRFToken': BackendURLS.csrfmiddlewaretoken(),
        },
        method: "DELETE",
        success: function (response) {
            if (!response.success) {
                showError(`Упс! Что-то пошло не так...\n\n${response.description}`);
            }
        },
        error: function(error) {
            showError(error);
        }
    }); 
}

function archiveChat(event) {
    const target = $(event.currentTarget);
    const ucid = storageGet('activeChatUcid');

    if (!ucid) {
        showError('Не удалось получить "ucid" текущего чата для архивации');
        return;
    }

    const url = $(target).data('url').replace('/0/', `/${ucid}/`);

    $.ajax({
        url,
        headers: {
            'X-CSRFToken': BackendURLS.csrfmiddlewaretoken(),
        },
        method: "PUT",
        success: function (response) {
            if (!response.success) {
                showError(`Упс! Что-то пошло не так...\n\n${response.description}`);
            } else {
                const allChats = storageGet('allChats');
                const chatsMessages = storageGet('chatsMessages');
                const { ucid } = response;

                if (!ucid) {
                    showError('Ответ не имеет атрибута "ucid"');
                    return;
                }
                
                try {
                    delete allChats[ucid];
                    delete chatsMessages[ucid];
                } catch (error) {
                    showError(error);
                }

                $(`li[data-chat-ucid="${ucid}"]`).remove();
                $('#chat-more-actions-menu').removeClass('d-block');
                
                storageSet('allChats', allChats);
                storageSet('chatsMessages', chatsMessages);
                openFirstChat();
            }
        },
        error: function(error) {
            showError(error);
        }
    });
}

function setupEvents() {
    $('#upload-file-modal-form button#send-file').on('click', function (event) {
        if ($('#upload-file-modal-form input[type=file]').prop('files').length > 0) {
            $('#upload-file-modal-form .modal-upload-spinner').addClass('active').removeClass('d-none');
            sendFile();
        }
    });
    $('#upload-image-modal-form button#send-image').on('click', function (event) {
        if ($('#upload-image-modal-form input[type=file]').prop('files').length > 0) {
            $('#upload-image-modal-form .modal-upload-spinner').addClass('active').removeClass('d-none');
            sendImage();
        }
    });
    $('.input-area .emoji-button').on('click', toggleEmojiMenu);
    $('#block-user').on('click', blockUser);
    $('#unblock-user').on('click', unblockUser);
    $('#archive-chat').on('click', archiveChat);
    $('#chat-more-actions').on('click', dropdownToggle);
    $('#form-image').on('change', previewImage);
        
    $('#chat-more-actions-menu').on('mouseleave', function () {
        $(this).removeClass('d-block');
    });

    $(".modal").on('hidden.bs.modal', function (event) {
        switch (event.currentTarget.id) { 
            case 'upload-image-modal-form':
                clearImageModalForm();
                break;
            case 'upload-file-modal-form':
                clearFileModalForm();
                break; 
        }
    });

    $(document).on('mousedown', '#jqcontext-menu li', function () {
        const messageId = $(this).data('id');

        switch ($(this).data('key')) { 
            case 'reply':
                setReplyMessage(messageId);
                break;
            case 'copy':
                copyToClipboard(messageId);
                break;
            case 'edit':
                setEditMessage(messageId);
                break;
            case 'delete':
                deleteMessage(messageId);
                break;
        }
    });

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
            $('#emoji-menu .emoji').on('click', (event) => {
                const input = $('#chat-message-input');
                if (!input.prop('disabled')) {
                    input.val(input.val() + $(event.currentTarget).text()).focus();
                }
            })    
        },
        error: function(error) {
            showError(error);
        },
    });   
}

$(document).ready(async function () {
    await loadSideChatsMenu();
    await setupWebSocket();
    await setupEvents();

    openFirstChat();
});
