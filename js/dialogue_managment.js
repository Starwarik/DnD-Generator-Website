const dialog_register = document.getElementById('dialog-register');
const dialog_login = document.getElementById('dialog-login');
const dialog_reset_password = document.getElementById('dialog-reset-password');
const dialog_reset_password_second = document.getElementById('dialog-reset-password-second');

dialog_register.addEventListener('click', () => dialog_register.close());
dialog_login.addEventListener('click', () => dialog_login.close());
dialog_reset_password.addEventListener('click', () => dialog_reset_password.close());
dialog_reset_password_second.addEventListener('click', () => dialog_reset_password_second.close());


let dialog_viewports = document.getElementsByClassName("dialog-viewport");

for (let i = 0; i < dialog_viewports.length; i++) {
    dialog_viewports[i].addEventListener('click', (event) => event.stopPropagation());
}

function close_all_dialogues() {
    dialog_register.close();
    dialog_login.close();
    dialog_reset_password.close();
    dialog_reset_password_second.close();
}

function show_login() {
    close_all_dialogues();
    dialog_login.showModal();
}

function show_register() {
    close_all_dialogues();
    dialog_register.showModal();
}

function show_reset_password() {
    close_all_dialogues();
    dialog_reset_password.showModal();
}