const dialog_from_login = document.getElementById('dialog-form-login');

dialog_from_login.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(dialog_from_login);

    const login = formData.get('login');
    const password = formData.get('pass');
    const token = await getToken(login, password);
    setCookie('access_token', token, 1);
    location.reload();
});