export function storageSet(key, object) {
	localStorage.setItem(key, JSON.stringify(object));
}

export function storageGet(key) {
    const raw = localStorage.getItem(key);
	return JSON.parse(raw);
}

export function storageRemove(key) {
    localStorage.removeItem(key);
}

export function dropdownToggle() {
    $("#chat-more-actions-menu").toggleClass("d-block");
}

export function previewImage(event) { 
    let previewImage = $("#preview-image")[0];
    previewImage.src = URL.createObjectURL(event.currentTarget.files[0]);
}

export function clearFileModalForm() {
    $('#form-file').val('');
    $('#upload-file-modal-form .file-caption-input').val('');
}

export function clearImageModalForm() {
    $('#preview-image')[0].src = '';
    $('#form-image').val('');
    $('#upload-image-modal-form .image-caption-input').val('');
}

export function getMessageById(messageId) {
    const messages = storageGet('chatsMessages');
    let targetMessage;

    $.each(messages, function (key, values) {
        const message = values[messageId];
        if (message) {
            targetMessage = message;
            return;
        }
    });

    return targetMessage;
}

export function copyToClipboard(messageId) {
    const message = getMessageById(messageId);
    const text = message.edited_text || message.text || message.caption || message.file_name;
    const $temp = $("<input>");

    $("body").append($temp);
    $temp.val(text).select();
    document.execCommand("copy");
    $temp.remove();
}

export function showError(error) {
    const modal = new bootstrap.Modal($('#display-errors-modal-form'), {
        background: true,
        keyboard: true,
    });

    $('#display-errors-modal-form-content').html(`<p>${JSON.stringify(error)}</p>`);
    modal.show();
} 

export class BackendURLS {
    static csrfmiddlewaretoken() {
        return $('input[name="csrfmiddlewaretoken"]').val();
    } 
    static jwtToken() {
        return $('input[name="jwt-token"]').val();
    }
    static newChat(ucid) {
        return $('input[name="new-chat-url"]').val().replace('/0/', `/${ucid}/`);
    }
    static note() {
        return $('input[name="note-url"]').val();
    }
    static chats() {
        return $('input[name="chats-url"]').val();
    }
    static fileUpload() {
        return $('input[name="file-upload-url"]').val();
    }
    static deleteMessage(messageId) {
        return $('input[name="delete-message-url"]').val().replace('/0/', `/${messageId}/`);
    }
    static emoji() {
        return $('input[name="emoji-url"]').val();
    }
    static archivedChatsUrl() {
        return $('input[name="archived-chats-url"]').val();
    }
    static messagesUrl(ucid) {
        return $('input[name="messages-url"]').val().replace("/0/", `/${ucid}/`);
    }
}
