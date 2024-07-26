async function getToken(username, password) {
    let formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
      
    let token = fetch('http://127.0.0.1:8000/api/token', {
        method: 'POST',
        body: formData,
    }).then(
        response => response.json()
    ).then(message => message.access_token);

    return token;
}

async function getUserInfo(token) {
    let formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
      
    let message = fetch('http://127.0.0.1:8000/api/user_info', {
        method: 'POST',
        headers: new Headers({
            'Authorization': 'Bearer '+token, 
        }), 
    }).then(
        response => response.json()
    );

    return message;
}