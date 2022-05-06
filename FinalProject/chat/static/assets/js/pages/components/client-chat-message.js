import { chatMessage } from './chat-message.js';


export function clientMessage(message) {
    return chatMessage(message, "client");
}
