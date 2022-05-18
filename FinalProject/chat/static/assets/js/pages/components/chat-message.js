import { replyToMessage } from './reply-to-message.js';


export function chatMessage(message, userType) {
    /* userType = "manager" || "client" */

    if (message.is_deleted) {
        return `<div class="message-in-chat" data-message-id="${message.id}">
                    <div id="${message.id}" class="message message-${userType}">
                        <div class="telegram-deleted-message">
                            <i class="bi bi-trash"></i><span><i>Сообщение удалено</i></span>
                        </div>
                    </div>
                </div>`;
    } else {
        const caption = message.is_edited ? message.edited_text : message.caption;
        const captionBlock = caption ? `<div class="telegram-text-message"> ${caption}</div>` : '';

        let messageHTML = `<div class="message-in-chat" data-message-id="${message.id}">
                            <div id="${message.id}" class="message message-${userType}">`;

        if (message.reply_to_message) {
            messageHTML += `<div class="telegram-reply-message" data-target-message-id="${message.reply_to_message.id}">
                                ${replyToMessage(message.reply_to_message)}
                            </div>`;
        }

        if (message.photo) {
            messageHTML += `<div class="telegram-photo-message default-image">
                                <img onload="$(this).parent().removeClass('default-image');" src="${message.photo}"></img>
                                ${captionBlock}
                            </div>`;
            
        } else if (message.document) {
            messageHTML += `<div class="telegram-document-message">
                                <a href="${message.document}" download="${message.file_name}"><i class="bi bi-file-earmark"></i>${message.file_name}</a>
                                ${captionBlock}
                            </div>`;
        } else {
            const text = message.is_edited ? message.edited_text : message.text;
            messageHTML += `<div class="telegram-text-message">
                                <span>${text}</span>
                            </div>`;
        }

        messageHTML += `<div class="message-metadata">
                            <span class="time ${userType === "manager" ? "right" : "left"}">${message.created_at_short}</span>
                        `
        
        if (message.is_edited) {
            messageHTML += `<span class="edited ${userType === "manager" ? "right" : "left"}">изменено</span>`;
        }
        
        messageHTML += `</div>
                    </div>
                </div>`;

        return messageHTML;
    }
}
