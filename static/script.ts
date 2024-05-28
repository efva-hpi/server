//HTML Elements
const createLobbyBtn = document.getElementById('createLobbyBtn');
const createLobbyForm = document.getElementById('createLobbyForm');
const lobbyCodeInp = <HTMLInputElement> document.getElementById('lobbyCodeInp');
const lobbyCodeInpLabel = <HTMLLabelElement> document.querySelector('label[for="lobbyCodeInp"]');
const cancelLobbyDialogBtn = document.getElementById('cancelLobbyDialogBtn');
const createLobbyDialog = <HTMLDialogElement>document.getElementById('createLobbyDialog');

//Lobby vars
var lobbyCode: string;


//Event listeners
createLobbyBtn?.addEventListener('click', () => {
    console.log("createLobbyBtn clicked");
    createLobbyDialog.showModal();
    lobbyCode = Math.random().toString(36).substring(2, 8).toUpperCase();
    lobbyCodeInp.value = lobbyCode;
    lobbyCodeInpLabel.innerHTML = `Lobby entry code: ${lobbyCode}`;
})

cancelLobbyDialogBtn?.addEventListener('click', () => {
    createLobbyDialog.close();
})

function getFormAction(form: HTMLFormElement){
    if(form === createLobbyForm){
        form.action = `/lobby/${lobbyCode}`;
    }
}