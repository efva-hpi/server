//HTML Elements
var createLobbyBtn = document.getElementById('createLobbyBtn');
var createLobbyForm = document.getElementById('createLobbyForm');
var lobbyCodeHdn = document.getElementById('lobbyCodeHdn');
var lobbyCodeHdnLabel = document.querySelector('label[for="lobbyCodeHdn"]');
var cancelLobbyDialogBtn = document.getElementById('cancelLobbyDialogBtn');
var createLobbyDialog = document.getElementById('createLobbyDialog');
var joinLobbyForm = document.getElementById('joinLobbyForm');
var joinLobbyCodeInp = document.getElementById('joinLobbyCodeInp');
var joinLobbyCodeInpLabel = document.querySelector('label[for="joinLobbyCodeInp"]');
//Lobby vars
var lobbyCode;
//Event listeners
createLobbyBtn === null || createLobbyBtn === void 0 ? void 0 : createLobbyBtn.addEventListener('click', function () {
    console.log("createLobbyBtn clicked");
    createLobbyDialog.showModal();
    lobbyCode = Math.random().toString(36).substring(2, 8).toUpperCase();
    lobbyCodeHdn.value = lobbyCode;
    lobbyCodeHdnLabel.innerHTML = "Lobby entry code: ".concat(lobbyCode);
});
cancelLobbyDialogBtn === null || cancelLobbyDialogBtn === void 0 ? void 0 : cancelLobbyDialogBtn.addEventListener('click', function () {
    createLobbyDialog.close();
});
function getFormAction(form) {
    if (form === createLobbyForm) {
        form.action = "/lobby/".concat(lobbyCode);
    }
    if (form === joinLobbyForm) {
        var joinCode = joinLobbyCodeInp.value;
        if (/^([A-Z0-9]){6}$/.test(joinCode)) {
            form.action = "/lobby/".concat(joinCode);
            return true;
        }
        joinLobbyCodeInpLabel.innerHTML = "Bitte einen gültigen Lobby code eingeben.<br>";
        form.action = "";
        return false;
    }
}
