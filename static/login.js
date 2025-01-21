const apiUrl = `${window.location.origin}/api`;
async function login(userData) {
    try {
        const response = await fetch(`${apiUrl}/login`, {
            method: "POST", // Método HTTP
            headers: {
                "Content-Type": "application/json" // Informar que estamos enviando JSON
            },
            body: JSON.stringify(userData) // Converter objeto para JSON
        });

        // Verificar se a requisição foi bem-sucedida
        if (!response.ok) {
            if (response.status == 404) {
                alert("Usuário não cadastrado");
            } else if (response.status == 401) {
                alert("Email/Senha Inválidos");
            } else {
                throw new Error(`Erro: ${response.status} - ${response.statusText}`);
            }
        }

        console.log(response);
        // Obter a resposta do servidor
        const result = await response.json();
        console.log("Resposta da API:", result);
        window.location = `${result.redirect_url}`


    } catch (error) {
        console.error("Erro ao logar:", error);
    }
}

function disable_inputs() {
    document.getElementById("email").disabled = true;
    document.getElementById("password").disabled = true;
}

function enable_inputs() {
    document.getElementById("email").disabled = false;
    document.getElementById("password").disabled = false;
}


document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("login-form");

    // Submissão do formulário
    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        // Simula envio para API
        const data = {
            email: form.email.value,
            password: form.password.value
        };
        disable_inputs();
        await login(data)
        enable_inputs();
        console.log("Dados enviados:", data);

    });
});