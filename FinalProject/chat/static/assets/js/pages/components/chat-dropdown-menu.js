import { showBlockBanner, hideBlockBanner } from './chat.js'; 


export function updateDropdownMenu(user) {
    $('#chat-more-actions').removeClass('d-none');
    $('#chat-more-actions-menu').removeClass('d-none');
    const blockItem = $('#block-user');
    const unblockItem = $('#unblock-user');
    if (user.is_blocked === true) {
        unblockItem.attr('data-user-id', user.id);
        unblockItem.parent().removeClass('d-none');
        blockItem.parent().addClass('d-none');
    } else {
        blockItem.attr('data-user-id', user.id);
        blockItem.parent().removeClass('d-none');
        unblockItem.parent().addClass('d-none');
    }
    if (user.is_blocked) {
        showBlockBanner();
    } else {
        hideBlockBanner();
    }
}

export function hideDropdownMenu() {
    $('#chat-more-actions').addClass('d-none');
    $('#chat-more-actions-menu').addClass('d-none');
}
