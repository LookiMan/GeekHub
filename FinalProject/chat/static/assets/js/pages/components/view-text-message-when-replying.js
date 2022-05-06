import { previewText } from './chat-item-preview-text.js';


export function viewTextMessageWhenReplying(message) {
    return $(`<div class="reply-message">
                <button class="button">
                    <i class="bi bi-x-lg"></i>
                </button>
                <span> ${previewText(message)}</span>
            </div>`);
}
