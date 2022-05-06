import {storageSet, storageGet, storageRemove} from './utils.js';


function testLocalStorage() {
    const key = "test key";
    const value = "test value";

    storageSet(key, value);
    
    if (storageGet(key) !== value) {
        alert("Локальное хранение недоступно!"+
            "Пожалуйста, включите локальное хранилище в настройках вашего браузера."+
            "В противном случае приложение не будет работать.");
    }

    storageRemove(key);
};

function setupInitialData() {
    const data = {
        'unreadMessages': { },
        'chatsMessages': { },
        'replyToMessage': { },
    }
    $.each(data, function (key, value) {
        storageSet(key, value);
    });    
}

(async function init() {
    await testLocalStorage();
    await setupInitialData();
})()
