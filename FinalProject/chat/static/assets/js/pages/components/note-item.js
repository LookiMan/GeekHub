import { previewText } from './chat-item-preview-text.js';


export function noteItem(chat) {
    const firstName = chat.first_name;
    const lastMessageText = previewText(chat.last_message);
    const lastMessagePrefix = chat.last_message.id ? 'Вы' : '';

    const item = $(`<li class="aside-chat-tab list-group-item d-flex justify-content-between align-items-start" data-chat-ucid="${chat.ucid}">
                <div>
                    <img class="telegram-note-image" src="/static/assets/images/note.png" alt="">
                </div>
                <div class="preview-container ms-2 me-auto">
                    <div class="fw-bold">${firstName}</div>
                    <div class="preview"><strong>${lastMessagePrefix}</strong> ${lastMessageText}</div>
                </div>
                <span class="badge bg-primary rounded-pill">${$(chat.messages).length}</span>
            </li>`);
    
    return item;
}
