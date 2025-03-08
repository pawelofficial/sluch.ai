document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const loginMessage = document.getElementById('loginMessage');
    const formContainer = document.getElementById('formContainer');
    const appContainer = document.getElementById('appContainer');
    const userInfo = document.getElementById('userInfo');
    const usernameDisplay = document.getElementById('usernameDisplay');
    const toggleSwitch = document.getElementById('toggleSwitch');

    // Handle form submission dynamically based on the toggle state
    formContainer.addEventListener("submit", async (event) => {
        event.preventDefault();

        const isRegistering = toggleSwitch.checked; // Check if toggle is in "Register" mode
        let endpoint = isRegistering ? "/register" : "/login"; // Choose correct endpoint
        let requestData = {};

        if (isRegistering) {
            requestData = {
                username: document.getElementById('registerUsername').value,
                password: document.getElementById('registerPassword').value,
                email: document.getElementById('email').value
            };
        } else {
            requestData = {
                username: document.getElementById('loginUsername').value,
                password: document.getElementById('loginPassword').value
            };
        }

        // Send request to the selected endpoint
        const response = await fetch(`http://127.0.0.1:8000${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();
        loginMessage.textContent = data.text;
        loginMessage.style.color = data.success ? 'green' : 'red';

        if (data.success && !isRegistering) {
            setTimeout(() => {
                formContainer.style.display = 'none'; // Hide login form
                appContainer.style.display = 'block'; // Show main app
                userInfo.style.display = 'block'; // Show username display
                usernameDisplay.textContent = requestData.username; // Set username text
            }, 500);
        }
    });
});
