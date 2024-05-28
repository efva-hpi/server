//HTML Elements
const createLobbyBtn = document.getElementById('createLobbyBtn');
const createLobbyForm = document.getElementById('createLobbyForm');
const lobbyCodeHdn = <HTMLInputElement> document.getElementById('lobbyCodeHdn');
const lobbyCodeHdnLabel = <HTMLLabelElement> document.querySelector('label[for="lobbyCodeHdn"]');
const cancelLobbyDialogBtn = document.getElementById('cancelLobbyDialogBtn');
const createLobbyDialog = <HTMLDialogElement>document.getElementById('createLobbyDialog');
const joinLobbyForm = document.getElementById('joinLobbyForm');
const joinLobbyCodeInp = <HTMLInputElement> document.getElementById('joinLobbyCodeInp');
const joinLobbyCodeInpLabel = <HTMLLabelElement> document.querySelector('label[for="joinLobbyCodeInp"]');

//Lobby vars
var lobbyCode: string;


//Event listeners
createLobbyBtn?.addEventListener('click', () => {
    console.log("createLobbyBtn clicked");
    createLobbyDialog.showModal();
    lobbyCode = Math.random().toString(36).substring(2, 8).toUpperCase();
    lobbyCodeHdn.value = lobbyCode;
    lobbyCodeHdnLabel.innerHTML = `Lobby entry code: ${lobbyCode}`;
})

cancelLobbyDialogBtn?.addEventListener('click', () => {
    createLobbyDialog.close();
})

function getFormAction(form: HTMLFormElement){
    if(form === createLobbyForm){
        form.action = `/lobby/${lobbyCode}`;
    }
    if(form === joinLobbyForm){
        let joinCode: string = joinLobbyCodeInp.value;
        if(/^([A-Z0-9]){6}$/.test(joinCode)){
            form.action = `/lobby/${joinCode}`;
            return true;
        }
        joinLobbyCodeInpLabel.innerHTML = "Bitte einen gültigen Lobby code eingeben.<br>";
        form.action="";
        return false;
    }
}