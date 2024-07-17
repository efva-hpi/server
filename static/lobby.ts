

// HTML Elements
const leaveBtn = document.getElementById("leaveBtn");
const messageDialog = <HTMLDialogElement> document.getElementById('messageDialog');
const guestUsernameInp = document.getElementById('guestUsernameInp');
const submitUsernameBtn = document.getElementById('submitUsernameBtn');

// WebSockets
 let href = window.location.href;
// href = href.substring(href.indexOf(':'));
// console.log(`ws${href}`);
// const lobbySocket: WebSocket = new WebSocket(`ws${href}`);
//
// const currentUrl: string = href.slice(0, -12);
// const currentLobbyCode: string = href.slice(-6);
// const gameUrl: string = `ws${currentUrl}game/${currentLobbyCode}`;
// const gameSocket: WebSocket = new WebSocket(gameUrl);

// Event listeners
// lobbySocket.addEventListener("open", (event: Event): void => {
//     lobbySocket.send("Hello Server!")
// });
//
// lobbySocket.addEventListener("message", (event: MessageEvent): void => {
//     console.log(`Message from Server: ${event.data}`)
// });

// update qr code
let qrcode = document.getElementById("qrcode") as HTMLImageElement;
let qrUrl = "https://api.qrserver.com/v1/create-qr-code/?data=" + href + "&amp;size=150x150";
qrcode.src = qrUrl;
console.log(qrUrl);

window.onload = () => {
    messageDialog?.showModal();
}

//leave lobby
leaveBtn?.addEventListener('click', () => {
    window.location.href = `${window.location.pathname}/leave`;
})

function joinAsGuest(form: HTMLFormElement) {
    form.action
}