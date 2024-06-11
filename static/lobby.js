// HTML Elements
var leaveBtn = document.getElementById("leaveBtn");
// Event listeners
//leave lobby
leaveBtn === null || leaveBtn === void 0 ? void 0 : leaveBtn.addEventListener('click', function () {
    window.location.href = "".concat(window.location.pathname, "/leave");
});
