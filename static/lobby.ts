// HTML Elements
const leaveBtn = document.getElementById("leaveBtn");

// Event listeners

// update qr code
let qrcode = document.getElementById("qrcode") as HTMLImageElement;
let url = "https://api.qrserver.com/v1/create-qr-code/?data=" + window.location.href + "&amp;size=150x150";
qrcode.src = url;
console.log(url);

//leave lobby
leaveBtn?.addEventListener('click', () => {
    window.location.href = `${window.location.pathname}/leave`;
})