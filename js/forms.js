const dialog_form_login = document.getElementById('dialog-form-login');
const dialog_form_register = document.getElementById('dialog-form-register');
const dialog_form_reset_password = document.getElementById('dialog-form-reset-password');
const dialog_form_reset_password_second = document.getElementById('dialog-form-reset-password-second');

dialog_form_login.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(dialog_form_login);

    const login = formData.get('login');
    const password = formData.get('pass');
    const token = await getToken(login, password);
    setCookie('access_token', token, 1);
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
        setCookie('access_token', token, 1);
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
        //location.reload();
    }
});