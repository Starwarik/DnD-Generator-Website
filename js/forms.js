const dialog_from_login = document.getElementById('dialog-form-login');
const dialog_from_register = document.getElementById('dialog-form-register');

dialog_from_login.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(dialog_from_login);

    const login = formData.get('login');
    const password = formData.get('pass');
    const token = await getToken(login, password);
    setCookie('access_token', token, 1);
    location.reload();
});

dialog_from_register.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(dialog_from_register);

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