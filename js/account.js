const account_navbar_noname = document.getElementById('account-navbar-noname');
const account_navbar_auth = document.getElementById('account-navbar-auth');

async function setUserInfo(token) {
    account_navbar_auth.classList.remove('no-seen');
    const user_info = await getUserInfo(token);
    if (user_info.status) {
        document.getElementById('account-navbar-auth__login').textContent = user_info.username;
        document.getElementById('account-navbar-menu__login').textContent = user_info.username;
        document.getElementById('account-info-form__username').textContent = user_info.username;
        document.getElementById('account-navbar-menu__email').textContent = user_info.email;
        document.getElementById('account-navbar-menu__balance').textContent = user_info.balance;
    } else {
        deleteCookie('access_token');
        account_navbar_auth.classList.add('no-seen');
        account_navbar_noname.classList.remove('no-seen');
    }
}

function logout() {
    deleteCookie('access_token');
    location.reload();
}

const token = getCookie('access_token');
if (!token) {
    account_navbar_noname.classList.remove('no-seen');
} else {
    setUserInfo(token);
}