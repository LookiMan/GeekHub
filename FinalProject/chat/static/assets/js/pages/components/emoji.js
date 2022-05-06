import { storageSet, storageGet } from '../../utils.js';


export const emojiMenuToggleStates = {
    open: 1,
    close: 2,
}

export function openEmojiMenu() {
    $('#emoji-menu').removeClass('d-none');
    $('#chat').removeClass('col-9').addClass('col-6');
    $('div.input-area .emoji-button').addClass('active-emoji');
}

export function closeEmojiMenu() {
    $('#emoji-menu').addClass('d-none');
    $('#chat').removeClass('col-6').addClass('col-9');
    $('div.input-area .emoji-button').removeClass('active-emoji');
}

export function toggleEmojiMenu() {
    const emojiMenuState = storageGet('emojiMenuState');

    if (emojiMenuState === null || emojiMenuState === emojiMenuToggleStates.close) {
        openEmojiMenu();
        storageSet('emojiMenuState', emojiMenuToggleStates.open);

    } else if (emojiMenuState === emojiMenuToggleStates.open) {
        closeEmojiMenu();
        storageSet('emojiMenuState', emojiMenuToggleStates.close);
    } 
}
