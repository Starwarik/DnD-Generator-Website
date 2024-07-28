const domain = 'https://fuckweb.ru/';

async function register(username, password, email) {
    let formData = {
        username: username,
        password: password,
        email: email
    };
      
    await fetch(domain+'api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(formData),
    });
}

async function getToken(username, password) {
    let formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
      
    let token = fetch(domain+'api/token', {
        method: 'POST',
        body: formData,
    }).then(
        response => response.json()
    ).then(message => message.access_token);

    return token;
}

async function getUserInfo(token) {
    let message = fetch(domain+'api/user_info', {
        method: 'GET',
        headers: new Headers({
            'Authorization': 'Bearer '+token, 
        }), 
    }).then(
        response => response.json()
    );

    return message;
}

async function sendResetLetter(email) {
    await fetch(domain+'api/reset_password?email='+email, {
        method: 'GET', 
    });
}

async function resetPassword(token_reset, new_password) {
    let formData = {
        new_password: new_password,
        token_reset: token_reset
    };
      
    await fetch(domain+'api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(formData),
    });
}