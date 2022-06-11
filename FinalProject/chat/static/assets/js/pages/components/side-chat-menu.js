import { noteItem } from './note-item.js';
import { chatItem } from './chat-item.js';
import { previewText } from './chat-item-preview-text.js';
import { updateSiteTitle } from './site-title.js';
import { renderChat } from './chat.js';
import { storageSet, storageGet, BackendURLS } from '../../utils.js';


function selectItem(target) {
    $('li.active-aside-chat-menu-tab').removeClass('active-aside-chat-menu-tab');
    $(target).addClass('active-aside-chat-menu-tab');
}

async function uploadMessages(ucid) {
    await $.ajax({
        url: BackendURLS.messagesUrl(ucid),
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]')[0].value,
        },
        success: function (messages) {
            const chatsMessages = storageGet('chatsMessages') || {};
            const chat = chatsMessages[ucid] || {};
            //
            $.each(messages, function (index, message) {
                chat[message.id] = message;
            });
            //
            chatsMessages[ucid] = chat;

            storageSet('chatsMessages', chatsMessages);
        },
        error: function (data) {
            console.error(data);
        }
    });
}

function sideChatMenuClickHandler(event) {
    const target = $(event.currentTarget);
    const chats = storageGet('chatsMessages');
    const ucid = $(target).data('chat-ucid');
    const chat = chats[ucid];
    const unreadMessages = storageGet('unreadMessages');
    
    if (!ucid) {
        console.error('Атрибут \"data-chat-ucid\"не найден в целевом элементе');
        return;
    }

    if (!chat) {
        uploadMessages(ucid);
    }

    renderChat(ucid);
    selectItem(target);

    delete unreadMessages[ucid];
    storageSet('unreadMessages', unreadMessages);

    updateAmountMessagesBadge(ucid);
    updateSiteTitle();
}

export function renderNote(chat) {
    $('#aside-chats-menu-spinner').remove();
    $('#aside-chats-menu').append($('<ol class="mx-0 px-0"></ol>'));
    renderNoteItem(chat);
}

function renderNoteItem(chat) {
    const parent = $('#aside-chats-menu > ol');
    const item = noteItem(chat);

    $(item).click(sideChatMenuClickHandler);
    $(parent).append(item);
}

export function renderChatItem(chat) {
    const parent = $('#aside-chats-menu > ol');
    const item = chatItem(chat);

    $(item).click(sideChatMenuClickHandler);
    $(parent).append(item);
}

export function renderChatList(chats) {
    $.each(chats, function (index, chat) {
        renderChatItem(chat);
    });
}

function updateAmountMessagesBadge(ucid) {
    const activeChatUcid = storageGet('activeChatUcid'); 
    const badge = $(`li[data-chat-ucid=${ucid}] span.badge`);
    let messages;

    if (activeChatUcid === ucid) {
        const chatsMessages = storageGet('chatsMessages');
        messages = chatsMessages[ucid] || {};

        if (Object.keys(messages).length === 0) {
            return;
        }

        badge.removeClass('bg-danger').addClass('bg-primary');
    } else {
        const unreadMessages = storageGet('unreadMessages');
        messages = unreadMessages[ucid] || {};

        badge.removeClass('bg-primary').addClass('bg-danger');
    }

    badge.text(Object.keys(messages).length);
}

export function updateChatListItem(message) {
    const { ucid } = message.chat || {};
    const previewMessagePrefix = !message.staff ? 'Клиент:' : 'Вы:';
    const preview = $(`li[data-chat-ucid=${ucid}] div.preview`);

    preview.html(`<strong>${previewMessagePrefix}</strong> ${previewText(message)}`);

    updateAmountMessagesBadge(ucid);
}

export async function openFirstChat() {
    const allChats = storageGet('allChats');
    const ucid = Object.keys(allChats)[0];
    const target = $(`li[data-chat-ucid="${ucid}"]`);

    await renderChat(ucid);
    selectItem(target);
}
