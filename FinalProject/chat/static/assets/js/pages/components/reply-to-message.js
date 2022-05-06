
export function replyToMessage(message) {
    const username = message?.staff ? 'Вы' : message.user.first_name;
    const html = `<div class="username"><strong>${username}</strong></div>`;

    if (message.photo) {
        return html + `<div class="content">🖼 <i>фото</i> </div>`;
    } else if (message.document) {
        return html + `<div class="content">📁 <i>файл</i> ${message.file_name}</div>`;
    } else if (message.text) {
        return html + `<div class="content">${message.text}</div>`;
    } else {
        return html + '<div class="content">[сообщение удалено]</div>';
    }
}
