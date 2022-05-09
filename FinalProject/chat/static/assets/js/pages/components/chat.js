import { storageSet, storageGet } from '../../utils.js';
import { clientMessage } from './client-chat-message.js';
import { managerMessage } from './manager-chat-message.js';
import { updateDropdownMenu, hideDropdownMenu } from './chat-dropdown-menu.js';
import { viewTextMessageWhenReplying } from './view-text-message-when-replying.js';


function updateChatTitle(chat) {
    const firstName = chat.first_name;
    const lastName = chat.last_name || '';
    const username = !chat.username ? '' : '@' + chat.username;

    $('#chat-title').html(`<span class="chat-name">${firstName} ${lastName}</span><div><span class="username">${username}</span></div>`);
    //
    const image = $('#chat .control-panel img.telegram-user-image')[0];
    // TODO:
    if (chat.user) {
        image.src = chat.user.image;
    } else {
        image.src = "/static/assets/images/note.png";
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

export function setReplyMessage(event) {
    const ucid = storageGet('activeChatUcid');
    const lastRecord = storageGet('replyToMessage'); 
    const messageId = $(event.currentTarget).data('message-id');

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

        $(event.currentTarget).addClass('selected-message');
        $('div#chat-and-message').append(replyToMessage);
    }
}

export function unsetReplyMessage() {
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

function renderChatMessage(messageHTML) {
    const chat = document.querySelector("#chat-and-message");
    const message = $(messageHTML).on("dblclick", setReplyMessage);
    $(chat).append(message);
    chat.scrollTop = chat.scrollHeight;
}

export function updateChatMessage(message) {
    const editedMessage = $(document.querySelector(`div[data-message-id="${message.id}"]`));

    if (!message.staff) {
        editedMessage.replaceWith(clientMessage(message));
    } else {
        editedMessage.replaceWith(managerMessage(message));
    }
}

export function renderClientMessage(message) {
    renderChatMessage(clientMessage(message));
}

export function renderManagerMessage(message) {
    renderChatMessage(managerMessage(message));
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
