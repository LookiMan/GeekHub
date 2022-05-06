import { storageGet } from '../../utils.js';


export function updateSiteTitle() {
    const unreadMessages = storageGet('unreadMessages');
    const title = 'SUPPORT CHAT';
    let amountUnreadMessages = 0;

    $.each(unreadMessages, function(ucid, messages) {
        amountUnreadMessages += Object.keys(messages).length;
    })

    if (amountUnreadMessages === 0) {
        document.title = title;
    } else {
        document.title = title + ` (${amountUnreadMessages})`;
    }
}
