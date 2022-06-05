import { storageSet, storageGet, getMessageById, showError } from '../../utils.js';
import { clientMessage } from './client-chat-message.js';
import { managerMessage } from './manager-chat-message.js';
import { updateDropdownMenu, hideDropdownMenu } from './chat-dropdown-menu.js';
import { viewTextMessageWhenReplying } from './view-text-message-when-replying.js';


function updateChatTitle(chat) {
    const firstName = chat.first_name;
    const lastName = chat.last_name || '';
    const username = !chat.username ? '' : '@' + chat.username;

    $('#chat-title').html(`<span class="chat-name">${firstName} ${lastName}</span><div><span class="username">${username}</span></div>`);
    
    const image = $('#chat .control-panel img.telegram-user-image')[0];
    
    if (chat.user) {
        image.src = chat.user.image;
    } else {
        image.src = '/static/assets/images/note.png';
    }
}

function scroll(messageId) {
    return function (event) {
        event.preventDefault();
        $('#chat-and-message').animate({
            scrollTop: $(`div[data-message-id="${messageId}"]`).offset().top
        }, 500);
    }
}

export function setReplyMessage(messageId) {
    const ucid = storageGet('activeChatUcid');
    const lastRecord = storageGet('replyToMessage'); 

    if (lastRecord && lastRecord.messageId === messageId) {
        unsetReplyMessage();
    } else {
        unsetReplyMessage();
        const chatsMessages = storageGet('chatsMessages');
        const messages = chatsMessages[ucid] || {};
        const replyToMessage = viewTextMessageWhenReplying(messages[messageId]);
        replyToMessage.on('click', '.button', unsetReplyMessage);
        replyToMessage.on('click', 'span', scroll(messageId));

        storageSet('replyToMessage', {
            ucid,
            messageId,
        });

        $(`#chat-and-message div[data-message-id="${messageId}"]`).addClass('selected-message');
        $('#chat-and-message').append(replyToMessage);
    }
}

export function unsetReplyMessage() {
    try {
        storageSet('replyToMessage', {});
        $('div#chat-and-message div.selected-message').removeClass('selected-message');
        $('div#chat-and-message div.reply-message').remove();
    } catch (exc) {
        showError(`Ууупс! Что-то пошло не так!\nОшибка: ${exc}`);
    } 
}

export function setEditMessage(messageId) {
    const ucid = storageGet('activeChatUcid');
    const lastRecord = storageGet('editMessage'); 

    if (lastRecord && lastRecord.messageId === messageId) {
        unsetEditMessage();
    } else {
        unsetEditMessage();
        const message = getMessageById(messageId);
        const editMessage = viewTextMessageWhenReplying(message);
        editMessage.on('click', '.button', unsetEditMessage);
        editMessage.on('click', 'span', scroll(messageId));

        storageSet('editMessage', {
            ucid,
            messageId,
        });

        $(`#chat-and-message div[data-message-id="${messageId}"]`).addClass('selected-message');
        $('#chat-and-message').append(editMessage);

        $('#chat-message-input').val(message.edited_text || message.text || message.caption);
    }
}

export function unsetEditMessage() {
    try {
        storageSet('editMessage', {});
        $('div#chat-and-message div.selected-message').removeClass('selected-message');
        $('div#chat-and-message div.reply-message').remove();
    } catch (exc) {
        showError(`Ууупс! Что-то пошло не так!\nОшибка: ${exc}`);
    } 
}

function bindActionsForMessage(message, messageData) {
    let contextMenu = [
        {
            icon: 'bi bi-reply',
            text: 'Ответить',
            dataKey: 'reply',
            dataId: messageData.id,
        },
    ];

    if (messageData.text || messageData.caption || messageData.document) {
        contextMenu = contextMenu.concat([
            {
                icon: 'bi bi-clipboard-check',
                text: 'Копировать',
                dataKey: 'copy',
                dataId: messageData.id,
            },
        ]);      
    }

    if (messageData?.staff) {
        if (messageData.text || messageData.caption) {
            contextMenu = contextMenu.concat([
                {
                    icon: 'bi bi-pen',
                    text: 'Редактировать',
                    dataKey: 'edit',
                    dataId: messageData.id,
                },
            ]);
        }

        contextMenu = contextMenu.concat([
            {
                icon: 'bi bi-x-lg',
                text: 'Удалить',
                dataKey: 'delete',
                dataId: messageData.id, 
            }
        ]);
    }

    if (!messageData.is_deleted) {
        $(message).find('.message').jqContextMenu({
            defaultStyle: 'jqcontext-menu-dark',
            contextMenu,
        });
    }

    if (messageData.photo) { 
        $(message).find('.message img').click(function() {
            $("#full-image").attr("src", $(this).attr("src"));
            $('#image-viewer').show();
        });
        
        $("#image-viewer .close").click(function(){
            $('#image-viewer').hide();
        });
    }
    return message;
}

function renderChatMessage(messageHTML, messageData) {
    const chat = document.querySelector('#chat-and-message');
    const message = bindActionsForMessage($(messageHTML), messageData);

    $(chat).append(message).scrollTop(chat.scrollHeight);
}

export function updateChatMessage(message) {
    const editedMessage = $(document.querySelector(`div[data-message-id="${message.id}"]`));

    if (!message.staff) {
        editedMessage.replaceWith(bindActionsForMessage($(clientMessage(message)), message));
    } else {
        editedMessage.replaceWith(bindActionsForMessage($(managerMessage(message)), message));
    }
}

export function renderClientMessage(message) {
    renderChatMessage(clientMessage(message), message);
}

export function renderManagerMessage(message) {
    renderChatMessage(managerMessage(message), message);
}

function renderChatMessages(messages) {
    $.each(messages, function(index, message) { 
        if (!message.staff) {
            renderClientMessage(message);
        } else {
            renderManagerMessage(message);
        }
    });
}

export function showBlockBanner() {
    $('#block-banner').removeClass('d-none');
    $('#chat-message-input').val('').attr('disabled', true);
}

export function hideBlockBanner() {
    $('#block-banner').addClass('d-none');
    $('#chat-message-input').attr('disabled', false);
}

export function renderChat(ucid) {
    const allChats = storageGet('allChats');
    const chat = allChats[ucid];

    if (!chat) {
        console.error(`Чат с ucid "${ucid}" не найден в локальном хранилище`);
        return;
    }

    const chatsMessages = storageGet('chatsMessages');
    const chatMessages = chatsMessages[ucid] || {};
    const { user } = chat || {};

    updateChatTitle(chat);

    if (user) {
        if (user.is_blocked) {
            showBlockBanner();
        } else {
            hideBlockBanner();
        }
        updateDropdownMenu(user);
    } else {
        hideDropdownMenu();
    }
    
    $('#chat-and-message').html('');
    
    renderChatMessages(chatMessages);
    storageSet('activeChatUcid', ucid);
}
