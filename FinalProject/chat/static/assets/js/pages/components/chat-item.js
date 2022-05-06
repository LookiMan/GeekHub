import { previewText } from './chat-item-preview-text.js';


export function chatItem(chat) {
    const firstName = chat.first_name;
    const lastName = chat.last_name || '';
    const lastMessageText = previewText(chat.last_message);
    const lastMessagePrefix = chat.last_message?.employee === null ? 'Клиент:' : 'Вы:';

    const item = $(`<li class="aside-chat-tab list-group-item d-flex justify-content-between align-items-start" data-chat-ucid="${chat.ucid}">
                <div>
                    <img class="telegram-user-image" src="${chat.user.image}" alt="">
                </div>
                <div class="preview-container ms-2 me-auto">
                    <div class="fw-bold">${firstName} ${lastName}</div>
                    <div class="preview"><strong>${lastMessagePrefix}</strong> ${lastMessageText}</div>
                </div>
                <span class="badge bg-primary rounded-pill">${$(chat.messages).length}</span>
            </li>`);

    return item;
}
