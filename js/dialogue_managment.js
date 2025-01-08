const dialog_register = document.getElementById('dialog-register');
const dialog_login = document.getElementById('dialog-login');
const dialog_reset_password = document.getElementById('dialog-reset-password');
const dialog_reset_password_second = document.getElementById('dialog-reset-password-second');
const dialog_reset_password_letter = document.getElementById('dialog-reset-password-letter');
const dialog__payment_success = document.getElementById('dialog__payment_success');
const dialog__payment_fail = document.getElementById('dialog__payment_fail');
const dialog__payment_wrong_amount = document.getElementById('dialog__payment_wrong-amount');
const dialog__busy_nickname = document.getElementById('dialog__busy_nickname');

dialog_register.addEventListener('mousedown', () => dialog_register.close());
dialog_login.addEventListener('mousedown', () => dialog_login.close());
dialog_reset_password.addEventListener('mousedown', () => dialog_reset_password.close());
dialog_reset_password_second.addEventListener('mousedown', () => dialog_reset_password_second.close());
dialog_reset_password_letter.addEventListener('mousedown', () => dialog_reset_password_letter.close());
dialog__payment_success.addEventListener('mousedown', () => dialog__payment_success.close());
dialog__payment_fail.addEventListener('mousedown', () => dialog__payment_fail.close());
dialog__payment_wrong_amount.addEventListener('mousedown', () => dialog__payment_wrong_amount.close());
dialog__busy_nickname.addEventListener('mousedown', () => dialog__busy_nickname.close());

let dialog_viewports = document.getElementsByClassName("dialog-viewport");

for (let i = 0; i < dialog_viewports.length; i++) {
    dialog_viewports[i].addEventListener('mousedown', (event) => event.stopPropagation());
}

window.addEventListener("load", () => {
    if (localStorage.getItem("busyNick") == true) {
        localStorage.removeItem("busyNick");
        show_busy_nickname();
    }
})

function close_all_dialogues() {
    dialog_register.close();
    dialog_login.close();
    dialog_reset_password.close();
    dialog_reset_password_second.close();
    dialog_reset_password_letter.close();
    dialog__payment_success.close();
    dialog__payment_fail.close();
    dialog__payment_wrong_amount.close();
    dialog__busy_nickname.close();
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

function show_reset_password_letter() {
    close_all_dialogues();
    dialog_reset_password_letter.showModal();
}

function show_reset_password_second() {
    close_all_dialogues();
    dialog_reset_password_second.showModal();
}

function show_payment_success() {
    close_all_dialogues();
    dialog__payment_success.showModal();
}

function show_payment_fail() {
    close_all_dialogues();
    dialog__payment_fail.showModal();
}

function show_payment_wrong_amount() {
    close_all_dialogues();
    dialog__payment_wrong_amount.showModal();
}

function show_busy_nickname() {
    close_all_dialogues();
    dialog__busy_nickname.showModal();
}