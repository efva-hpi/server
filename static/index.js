// HTML Elements
// Login
var loginBtn = document.getElementById('loginBtn');
var loginDialog = document.getElementById('loginDialog');
var loginForm = document.getElementById('loginForm');
// Registrierung
var registerBtn = document.getElementById('registerBtn');
var registerDialog = document.getElementById('registerDialog');
var registerForm = document.getElementById('registerForm');
var registerPasswordInp = document.getElementById('registerPasswordInp');
var confirmPasswordInp = document.getElementById('confirmPasswordInp');
// Lobby erstellen
var createLobbyBtn = document.getElementById('createLobbyBtn');
var createLobbyForm = document.getElementById('createLobbyForm');
var lobbyCodeHdn = document.getElementById('lobbyCodeHdn');
var lobbyCodeHdnLabel = document.querySelector('label[for="lobbyCodeHdn"]');
var cancelLobbyDialogBtn = document.getElementById('cancelLobbyDialogBtn');
var createLobbyDialog = document.getElementById('createLobbyDialog');
var joinLobbyForm = document.getElementById('joinLobbyForm');
var joinLobbyCodeInp = document.getElementById('joinLobbyCodeInp');
var joinLobbyCodeInpLabel = document.querySelector('label[for="joinLobbyCodeInp"]');
// Error dialog
var errorDialog = document.getElementById('errorDialog');
var closeErrorDialogBtn = document.getElementById('closeErrorDialogBtn');
//Lobby vars
var lobbyCode;
//Event listeners
createLobbyBtn === null || createLobbyBtn === void 0 ? void 0 : createLobbyBtn.addEventListener('click', function () {
    // console.log("createLobbyBtn clicked");
    createLobbyDialog.showModal();
    lobbyCode = Math.random().toString(36).substring(2, 8).toUpperCase();
    lobbyCodeHdn.value = lobbyCode;
    lobbyCodeHdnLabel.innerHTML = "Lobby entry code: ".concat(lobbyCode);
});
cancelLobbyDialogBtn === null || cancelLobbyDialogBtn === void 0 ? void 0 : cancelLobbyDialogBtn.addEventListener('click', function () {
    createLobbyDialog.close();
});
loginBtn === null || loginBtn === void 0 ? void 0 : loginBtn.addEventListener('click', function () {
    loginDialog.showModal();
});
registerBtn === null || registerBtn === void 0 ? void 0 : registerBtn.addEventListener('click', function () {
    registerDialog.showModal();
});
closeErrorDialogBtn === null || closeErrorDialogBtn === void 0 ? void 0 : closeErrorDialogBtn.addEventListener('click', function () {
    errorDialog.close();
});
function getFormAction(form) {
    switch (form) {
        case createLobbyForm:
            form.action = "/lobby/".concat(lobbyCode);
            return true;
        case joinLobbyForm:
            var joinCode = joinLobbyCodeInp.value;
            form.action = "/lobby/".concat(joinCode);
            return true;
        case loginForm:
            form.action = "/login";
            return true;
        case registerForm:
            form.action = "/register";
            return true;
    }
}
registerPasswordInp.onchange = validatePassword;
confirmPasswordInp.onkeyup = validatePassword;
// Functions
function validatePassword() {
    if (registerPasswordInp.value != confirmPasswordInp.value) {
        confirmPasswordInp.setCustomValidity("Passwords Don't Match");
        return false;
    }
    else {
        confirmPasswordInp.setCustomValidity('');
    }
}
