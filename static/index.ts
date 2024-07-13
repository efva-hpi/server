// HTML Elements
// Login
const loginBtn = document.getElementById('loginBtn');
const loginDialog = <HTMLDialogElement>document.getElementById('loginDialog');
const loginForm = document.getElementById('loginForm');
// Registrierung
const registerBtn = document.getElementById('registerBtn');
const registerDialog = <HTMLDialogElement>document.getElementById('registerDialog');
const registerForm = document.getElementById('registerForm');
const registerPasswordInp = <HTMLInputElement>document.getElementById('registerPasswordInp');
const confirmPasswordInp = <HTMLInputElement>document.getElementById('confirmPasswordInp');
// Lobby erstellen
const createLobbyBtn = document.getElementById('createLobbyBtn');
const createLobbyForm = document.getElementById('createLobbyForm');
const lobbyCodeHdn = <HTMLInputElement> document.getElementById('lobbyCodeHdn');
const lobbyCodeHdnLabel = <HTMLLabelElement> document.querySelector('label[for="lobbyCodeHdn"]');
const cancelLobbyDialogBtn = document.getElementById('cancelLobbyDialogBtn');
const createLobbyDialog = <HTMLDialogElement>document.getElementById('createLobbyDialog');
const joinLobbyForm = document.getElementById('joinLobbyForm');
const joinLobbyCodeInp = <HTMLInputElement> document.getElementById('joinLobbyCodeInp');
const joinLobbyCodeInpLabel = <HTMLLabelElement> document.querySelector('label[for="joinLobbyCodeInp"]');
// Error dialog
const errorDialog = <HTMLDialogElement>document.getElementById('errorDialog');
const closeErrorDialogBtn = document.getElementById('closeErrorDialogBtn');

//Lobby vars
var lobbyCode: string;


//Event listeners
createLobbyBtn?.addEventListener('click', () => {
    // console.log("createLobbyBtn clicked");
    createLobbyDialog.showModal();
    lobbyCode = Math.random().toString(36).substring(2, 8).toUpperCase();
    lobbyCodeHdn.value = lobbyCode;
    lobbyCodeHdnLabel.innerHTML = `Lobby entry code: ${lobbyCode}`;
});

cancelLobbyDialogBtn?.addEventListener('click', () => {
    createLobbyDialog.close();
});

loginBtn?.addEventListener('click', () => {
    loginDialog.showModal();
});

registerBtn?.addEventListener('click', () => {
    registerDialog.showModal();
});

closeErrorDialogBtn?.addEventListener('click', () => {
    errorDialog.close();
});

function getFormAction(form: HTMLFormElement){
    switch (form) {
        case createLobbyForm:
            form.action = `/lobby/${lobbyCode}`;
            return true;
        case joinLobbyForm:
            let joinCode: string = joinLobbyCodeInp.value;
            form.action = `/lobby/${joinCode}`;
            return true;
        case loginForm:
            form.action = `/login`;
            return true;
        case registerForm:
            form.action = `/register`;
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
    } else {
        confirmPasswordInp.setCustomValidity('');
    }
}