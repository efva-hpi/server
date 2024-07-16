// HTML Elements
var leaveBtn = document.getElementById("leaveBtn");
// Event listeners
// update qr code
var qrcode = document.getElementById("qrcode");
var url = "https://api.qrserver.com/v1/create-qr-code/?data=" + window.location.href + "&amp;size=150x150";
qrcode.src = url;
console.log(url);
//leave lobby
leaveBtn === null || leaveBtn === void 0 ? void 0 : leaveBtn.addEventListener('click', function () {
    window.location.href = "".concat(window.location.pathname, "/leave");
});
