import { chatMessage } from './chat-message.js';


export function managerMessage(message) {
    return chatMessage(message, "manager");
}
