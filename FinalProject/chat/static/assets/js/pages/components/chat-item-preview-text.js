
export function previewText(message) {
    if (message.photo) {
        return '🖼 <i>фото</i>';
    } else if (message.document) {
        return `📁 <i>файл</i> ${message.file_name}`;
    } else if (message.text) {
        return message.text;
    } else {
        return '<i>нет сообщений</i>';
    }
}
