let dialog_register = document.getElementById('dialog-register');
let dialog_login = document.getElementById('dialog-login');
let dialog_reset_password = document.getElementById('dialog-reset-password');
let dialog_reset_password_second = document.getElementById('dialog-reset-password-second');

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