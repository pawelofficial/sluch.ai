document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById('loginForm');
    const loginMessage = document.getElementById('loginMessage');
    const loginContainer = document.getElementById('loginContainer');
    const appContainer = document.getElementById('appContainer');
    const userInfo = document.getElementById('userInfo');
    const usernameDisplay = document.getElementById('usernameDisplay');

    loginForm.onsubmit = async (event) => {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        const response = await fetch('http://127.0.0.1:8000/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        loginMessage.textContent = data.text;
        loginMessage.style.color = data.success ? 'green' : 'red';

        if (data.success) {
            setTimeout(() => {
                loginContainer.style.display = 'none'; // Hide login form
                appContainer.style.display = 'block'; // Show main app
                userInfo.style.display = 'block'; // Show username display
                usernameDisplay.textContent = username; // Set username text
            }, 500);
        }
    };
});
