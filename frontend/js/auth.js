async function register() {
  const username = document.getElementById("reg-username").value.trim();
  const email = document.getElementById("reg-email").value.trim();
  const password = document.getElementById("reg-password").value.trim();
  const confirm = document.getElementById("reg-confirm").value.trim();
  const resultDiv = document.getElementById("result");

  // --- Vérifications ---
  if (!username || !email || !password || !confirm) {
    resultDiv.className = "error";
    resultDiv.innerText = "⚠️ Veuillez remplir tous les champs.";
    return;
  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    resultDiv.className = "error";
    resultDiv.innerText = "⚠️ Adresse email invalide.";
    return;
  }
  if (password !== confirm) {
    resultDiv.className = "error";
    resultDiv.innerText = "⚠️ Les mots de passe ne correspondent pas.";
    return;
  }
  if (password.length < 6) {
    resultDiv.className = "error";
    resultDiv.innerText = "⚠️ Le mot de passe doit contenir au moins 6 caractères.";
    return;
  }
  const complexityRegex = /^(?=.*[A-Z])(?=.*\d).+$/;
  if (!complexityRegex.test(password)) {
    resultDiv.className = "error";
    resultDiv.innerText = "⚠️ Le mot de passe doit contenir au moins une majuscule et un chiffre.";
    return;
  }
  if (/\s/.test(password)) {
    resultDiv.className = "error";
    resultDiv.innerText = "⚠️ Le mot de passe ne doit pas contenir d'espaces.";
    return;
  }

  // --- Envoi au backend ---
  try {
    const response = await fetch("http://localhost:5000/auth/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password })
    });

    if (response.status === 201) {
      resultDiv.className = "success";
      resultDiv.innerText = "✅ Compte créé avec succès !";
      setTimeout(() => (window.location.href = "login.html"), 1500);
    } else {
      const error = await response.json();
      resultDiv.className = "error";
      resultDiv.innerText = "❌ Erreur : " + (error.error || "Inscription échouée");
    }
  } catch (err) {
    resultDiv.className = "error";
    resultDiv.innerText = "⚠️ Erreur réseau : " + err;
  }
}