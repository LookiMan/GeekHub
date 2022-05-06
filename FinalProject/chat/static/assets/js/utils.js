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
    var previewImage = $("#preview-image")[0];
    previewImage.src = URL.createObjectURL(event.currentTarget.files[0]);
}
