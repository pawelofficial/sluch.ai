document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const toggleSwitch = document.getElementById("toggleSwitch");
    const loginMessage = document.getElementById("loginMessage");

    toggleSwitch.addEventListener("change", () => {
        loginForm.classList.toggle("hidden", toggleSwitch.checked);
        registerForm.classList.toggle("hidden", !toggleSwitch.checked);
    });

    document.querySelectorAll(".auth-form").forEach(form => {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();
            const isRegistering = form.id === "registerForm";
            const endpoint = isRegistering ? "/register" : "/login";

            const requestData = {
                email: form.querySelector("input[type='email']").value,
                password: form.querySelector("input[type='password']").value
            };

            const response = await fetch(`http://127.0.0.1:8000${endpoint}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(requestData)
            });

            const data = await response.json();
            loginMessage.textContent = data.text;
            loginMessage.style.color = data.success ? "green" : "red";

            if (data.success && !isRegistering) {
                setTimeout(() => {
                    document.getElementById("formContainer").style.display = "none";
                }, 500);
            }
        });
    });
});
