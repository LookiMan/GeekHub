
export function previewText(message) {
    if (message.is_deleted) {
        return '🗑 <i>сообщение удалено</i>';
    } else if (message.photo) {
        return '🖼 <i>фото</i>';
    } else if (message.document) {
        return `📁 <i>файл</i> ${message.file_name}`;
    } else if (message.text) {
        return message.is_edited ? message.edited_text : message.text;
    } else {
        return '<i>нет сообщений</i>';
    }
}
