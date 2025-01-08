const domain = 'https://adventuregenerator.ru/';

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
    let request = await fetch(domain+'api/user_info', {
        method: 'GET',
        headers: new Headers({
            'Authorization': 'Bearer '+token, 
        }), 
    })
    

    if (request.ok) {
        return request.json();
    } else if (request.status == 401) {
        localStorage.setItem("busyNick", true);
    }

    return {
        status: false
    };
}

async function sendResetLetter(email) {
    let reset_token = await fetch(domain+'api/reset_token?email='+email, {
        method: 'GET' 
    }).then(response => response.text());
    console.log(reset_token);
}

async function resetPassword(token_reset, new_password) {
    let formData = {
        new_password: new_password,
        token_reset: token_reset
    };
      
    await fetch(domain+'api/reset_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(formData),
    });
}

async function makePayment(amount) {
    await fetch(domain+'api/make_payment?amount='+amount, {
        method: 'GET',
        headers: new Headers({
            'Authorization': 'Bearer '+token, 
        })
    }).then(
		response => response.text()
	).then(
		url => window.location.replace(url.slice(1, -1))
	);
}