let params = new URLSearchParams(document.location.search);
let reset_token = params.get("reset_token");

if (!!reset_token) {
    show_reset_password_second();
}