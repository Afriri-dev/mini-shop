document.getElementById("login-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const email = document.getElementById("login-email").value.trim();
  const password = document.getElementById("login-password").value.trim();
  const resultDiv = document.getElementById("result");

  try {
    const response = await fetch("http://localhost:5000/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (response.ok && data.token) {
      // ✅ Stocker le token dans localStorage
      localStorage.setItem("token", data.token);

      // ✅ Redirection vers Orders
      window.location.href = data.redirect;
    } else {
      resultDiv.className = "error";
      resultDiv.innerText = "❌ Erreur : " + (data.error || "Connexion échouée");
    }
  } catch (err) {
    resultDiv.className = "error";
    resultDiv.innerText = "⚠️ Erreur réseau : " + err;
  }
});