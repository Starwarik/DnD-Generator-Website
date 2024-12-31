let params = new URLSearchParams(document.location.search);
let reset_token = params.get("reset_token");
let transaction_status = params.get("transactionstatus");

if (!!reset_token) {
    show_reset_password_second();
}

if (transaction_status == "success") {
    show_payment_success();
} else if (transaction_status == "fail") {
    show_payment_fail();
}