import { replyToMessage } from './reply-to-message.js';


export function chatMessage(message, userType) {
    /* userType = "manager" || "client" */
    const captionBlock = message.caption ? `<div class="telegram-text-message">${message.caption}</div>` : "";

    let messageHTML = `<div class="message-in-chat" data-message-id="${message.id}">
                        <div class="message message-${userType}">`;

    if (message.reply_to_message) {
        messageHTML += `<div class="telegram-reply-message" data-target-message-id="${message.reply_to_message.id}">
                            ${replyToMessage(message.reply_to_message)}
                        </div>`;
    }

    if (message.photo) {  
        messageHTML += `<div class="telegram-photo-message">
                            <img src="${message.photo}"></img>
                            ${captionBlock}
                        </div>`;
        
    } else if (message.document) {
        messageHTML += `<div class="telegram-document-message">
                            <a href="${message.document}"><i class="bi bi-file-earmark"></i>${message.file_name}</a>
                            ${captionBlock}
                        </div>`;
    } else {
        messageHTML += `<div class="telegram-text-message">
                            <span>${message.text}</span>
                        </div>`;                   
    }

    messageHTML += `<div class="message-metadata">
                        <span class="time time-${userType === "manager" ? "right" : "left"}">${message.created_at_short}</span>
                    </div>
                </div>
            </div>`;

    return messageHTML;
}
