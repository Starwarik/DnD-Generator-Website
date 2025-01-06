const dialog_form_login = document.getElementById('dialog-form-login');
const dialog_form_register = document.getElementById('dialog-form-register');
const dialog_form_reset_password = document.getElementById('dialog-form-reset-password');
const dialog_form_reset_password_second = document.getElementById('dialog-form-reset-password-second');
const buy_tokens_form = document.getElementById('buy-tokens-form');
const account_navbar_form = document.getElementById('account-navbar-form');

dialog_form_login.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(dialog_form_login);

    const login = formData.get('login');
    const password = formData.get('pass');
    const token = await getToken(login, password);
    setCookie('access_token', token, {secure: true, 'max-age': 3600, samesite: 'strict'});
    location.reload();
});

dialog_form_register.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(dialog_form_register);

    const email = formData.get('email');
    const login = formData.get('login');
    const password = formData.get('pass');
    const password_repeat = formData.get('pass_repeat');

    if (password == password_repeat) {
        await register(login, password, email);

        const token = await getToken(login, password);
        setCookie('access_token', token, {secure: true, 'max-age': 3600, samesite: 'strict'});
        location.reload();
    }
});

dialog_form_reset_password.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(dialog_form_reset_password);

    const email = formData.get('email');

    await sendResetLetter(email);
    show_reset_password_letter();
});

dialog_form_reset_password_second.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(dialog_form_reset_password_second);

    const pass = formData.get('pass');
    const pass_repeat = formData.get('pass_repeat');

    if (pass == pass_repeat) {
        await resetPassword(reset_token, pass_repeat);
        location.href = domain;
    }
});

buy_tokens_form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(buy_tokens_form);

    const amount = Number(formData.get('amount'));

    if (amount >= 100) {
        await makePayment(amount);
    } else {
        show_payment_wrong_amount();
    }
});

account_navbar_form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(account_navbar_form);

    const amount = Number(formData.get('amount'));

    if (amount >= 100) {
        await makePayment(amount);
    } else {
        show_payment_wrong_amount();
    }
});
show_payment_wrong_amount();