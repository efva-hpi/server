//HTML Elements
var createLobbyBtn = document.getElementById('createLobbyBtn');
var createLobbyForm = document.getElementById('createLobbyForm');
var lobbyCodeInp = document.getElementById('lobbyCodeInp');
var lobbyCodeInpLabel = document.querySelector('label[for="lobbyCodeInp"]');
var cancelLobbyDialogBtn = document.getElementById('cancelLobbyDialogBtn');
var createLobbyDialog = document.getElementById('createLobbyDialog');
//Lobby vars
var lobbyCode;
//Event listeners
createLobbyBtn === null || createLobbyBtn === void 0 ? void 0 : createLobbyBtn.addEventListener('click', function () {
    console.log("createLobbyBtn clicked");
    createLobbyDialog.showModal();
    lobbyCode = Math.random().toString(36).substring(2, 8).toUpperCase();
    lobbyCodeInp.value = lobbyCode;
    lobbyCodeInpLabel.innerHTML = "Lobby entry code: ".concat(lobbyCode);
});
cancelLobbyDialogBtn === null || cancelLobbyDialogBtn === void 0 ? void 0 : cancelLobbyDialogBtn.addEventListener('click', function () {
    createLobbyDialog.close();
});
function getFormAction(form) {
    if (form === createLobbyForm) {
        form.action = "/lobby/".concat(lobbyCode);
    }
}
