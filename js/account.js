const account_navbar_noname = document.getElementById('account-navbar-noname');
const account_navbar_auth = document.getElementById('account-navbar-auth');

async function setUserInfo(token) {
    const user_info = await getUserInfo(token);
    document.getElementById('account-navbar-auth__login').textContent = user_info.username;
    account_navbar_auth.classList.remove('no-seen');
}

const token = getCookie('access_token');
if (!token) {
    account_navbar_noname.classList.remove('no-seen');
} else {
    setUserInfo(token);
}