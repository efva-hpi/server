"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var socket_io_client_1 = require("socket.io-client");
// HTML Elements
var leaveBtn = document.getElementById("leaveBtn");
var messageDialog = document.getElementById('messageDialog');
var guestUsernameInp = document.getElementById('guestUsernameInp');
var submitUsernameBtn = document.getElementById('submitUsernameBtn');
// WebSockets
var href = window.location.href;
href = href.substring(href.indexOf(':'));
// console.log(`ws${href}`);
// const lobbySocket: WebSocket = new WebSocket(`ws${href}`);
//
// const currentUrl: string = href.slice(0, -12);
// const currentLobbyCode: string = href.slice(-6);
// const gameUrl: string = `ws${currentUrl}game/${currentLobbyCode}`;
// const gameSocket: WebSocket = new WebSocket(gameUrl);
var socket = (0, socket_io_client_1.default)();
socket.on('connect', function () {
    socket.emit('message', { data: "conn: ".concat(href.slice(-6)) });
});
// Event listeners
// lobbySocket.addEventListener("open", (event: Event): void => {
//     lobbySocket.send("Hello Server!")
// });
//
// lobbySocket.addEventListener("message", (event: MessageEvent): void => {
//     console.log(`Message from Server: ${event.data}`)
// });
// update qr code
var qrcode = document.getElementById("qrcode");
var qrUrl = "https://api.qrserver.com/v1/create-qr-code/?data=" + href + "&amp;size=150x150";
qrcode.src = qrUrl;
console.log(qrUrl);
window.onload = function () {
    messageDialog === null || messageDialog === void 0 ? void 0 : messageDialog.showModal();
};
//leave lobby
leaveBtn === null || leaveBtn === void 0 ? void 0 : leaveBtn.addEventListener('click', function () {
    window.location.href = "".concat(window.location.pathname, "/leave");
});
function joinAsGuest(form) {
    form.action;
}
