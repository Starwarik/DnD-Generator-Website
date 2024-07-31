const account_navbar_menu = document.getElementById('account-navbar-menu');
var is_shown_navbar_menu = false;

function show_navbar_menu() {
    account_navbar_menu.classList.remove('no-seen');
}

function hide_navbar_menu() {
    account_navbar_menu.classList.add('no-seen');
}

function toggle_navbar_menu() {
    if (is_shown_navbar_menu) {
        hide_navbar_menu();
        is_shown_navbar_menu = false;
    } else {
        show_navbar_menu();
        is_shown_navbar_menu = true;
    }
}