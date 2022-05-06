import { storageSet, storageGet } from '../../utils.js';
import { noteItem } from './note-item.js';
import { chatItem } from './chat-item.js';
import { previewText } from './chat-item-preview-text.js';
import { updateSiteTitle } from './site-title.js';
import { renderChat } from './chat.js';


function sideChatMenuClickHandler(event) {
    const target = $(event.currentTarget);
    const chats = storageGet('chatsMessages');
    const ucid = $(target).data('chat-ucid');
    const chat = chats[ucid];
    const unreadMessages = storageGet('unreadMessages');
    
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

export function renderNote(chat) {
    $('#aside-chats-menu-spinner').remove();
    //
    $('#aside-chats-menu').append($('<ol class="mx-0 px-0"></ol>'));
    //
    renderNoteItem(chat);
    //
    updateAmountMessagesBadge(chat.ucid);
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

export function updateChatListItem(message) {
    const { ucid } = message.chat || {};
    const previewMessagePrefix = message?.staff === null ? 'Клиент:' : 'Вы:';
    const preview = $(`li[data-chat-ucid=${ucid}] div.preview`);

    preview.html(`<strong>${previewMessagePrefix}</strong> ${previewText(message)}`);

    updateAmountMessagesBadge(ucid);
}