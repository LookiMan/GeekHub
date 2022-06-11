import { renderChatList } from './components/side-chat-menu.js';
import { openFirstChat } from './components/side-chat-menu.js';
import { storageSet, storageGet, BackendURLS } from '../utils.js';


async function loadChats() {
    const match = location.pathname.match(/\d+/);

    if (!match) {
        showError('Не удалось найти совпадений');
        return;
    }

    const offset = match[0];

    await $.ajax({
        url: BackendURLS.archivedChatsUrl(offset),
        headers: {
            'content-type': 'application/json',
            'X-CSRFToken': BackendURLS.csrfmiddlewaretoken(),
        },
        success: function (rawChatsList) {
            const allChats = storageGet('allChats') || {};
            
            $.each(rawChatsList, function (index, chat) {
                allChats[chat.ucid] = chat;
            });
            
            storageSet('allChats', allChats);
            
            $('#aside-chats-menu-spinner').remove();
            $('#aside-chats-menu').append($('<ol class="mx-0 px-0"></ol>'));
            
            if ($(rawChatsList).length === 0) {
                archiveEmpty();
            } else {
                renderChatList(rawChatsList);
            }
        },
        error: function(error) {
            console.error(error);
        }
    });
}

async function loadMessages() {
    const chats = storageGet('allChats');

    $.each(chats, async function (index, chat) {
        const { ucid } = chat;

        await $.ajax({
            url: BackendURLS.messagesUrl(ucid),
            headers: {
                'content-type': 'application/json',
                'X-CSRFToken': BackendURLS.csrfmiddlewaretoken(),
            },
            success: function (messages) {
                $.each(messages, function (index, message) {
                    const { ucid } = message.chat || { };
                    const chatsMessages = storageGet('chatsMessages') || { };
                    
                    if (!ucid) {
                        console.error('Полученное сообщение неимет атрибута "ucid"');
                        console.error(message);
                        return;
                    }

                    const chatMessages = chatsMessages[ucid] || { };
                    chatMessages[message.id] = message;
                    chatsMessages[ucid] = chatMessages;
                    storageSet('chatsMessages', chatsMessages);
                });
            },
            error: function(error) {
                console.error(error);
            }
        });
    });
}

function unarchiveChat(event) {
    event.preventDefault();

    const target = $(event.currentTarget);
    const ucid = storageGet('activeChatUcid');

    if (!ucid) {
        alert('Не удалось получить "ucid" текущего чата для архивации');
        return;
    }

    const url = $(target).attr('href').replace('/0/', `/${ucid}/`)

    $.ajax({
        url,
        headers: {
            'X-CSRFToken': BackendURLS.csrfmiddlewaretoken(),
        },
        method: "PUT",
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

                storageSet('allChats', allChats);
                storageSet('chatsMessages', chatsMessages);
                
                $(`li[data-chat-ucid="${ucid}"]`).remove();

                if (Object.keys(allChats).length === 0) {
                    archiveEmpty();
                } else {
                    openFirstChat();
                }
            }
        },
        error: function(error) {
            console.error(error);
        }
    });
}

function archiveEmpty() {
    $('#chat-and-message').html('');
    $('#chat-control-panel').html('');
    $('.unblock-user').remove();
    $('#archive-empty').removeClass('d-none');
}

async function setupEvents() {
    $('#unblockUser').on('click', unarchiveChat);
}

$(document).ready(async function () {
    await loadChats();
    await loadMessages();
    await setupEvents();
    setTimeout(openFirstChat, 250);
});
