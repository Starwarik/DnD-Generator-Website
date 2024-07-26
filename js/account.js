async function getToken() {
    let user = {
        username: 'test',
        password: 'test'
    };
      
    let response = await fetch('https://fuckweb.ru/api/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(user)
    });
      
    let result = await response.json();
    alert(result.message);
}

getToken();