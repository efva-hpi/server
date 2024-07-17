// HTML Elements
const leaveBtn = document.getElementById("leaveBtn");
const messageDialog = <HTMLDialogElement> document.getElementById('messageDialog');
const guestUsernameInp = document.getElementById('guestUsernameInp');
const submitUsernameBtn = document.getElementById('submitUsernameBtn');
// Event listeners

// update qr code
let qrcode = document.getElementById("qrcode") as HTMLImageElement;
let url = "https://api.qrserver.com/v1/create-qr-code/?data=" + window.location.href + "&amp;size=150x150";
qrcode.src = url;
console.log(url);

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