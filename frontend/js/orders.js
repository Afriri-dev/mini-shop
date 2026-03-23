// --- Récupération du token ---
const token = localStorage.getItem("token");
if (!token) {
  alert("Vous devez être connecté !");
  window.location.href = "login.html"; // redirection si pas de token
}

// --- Bouton Déconnexion ---
document.getElementById("logoutBtn").addEventListener("click", () => {
  localStorage.removeItem("token");
  showMessage("Déconnexion réussie !", "success");
  window.location.href = "login.html"; // redirection vers la page de login
});

// --- Créer une commande ---
document.getElementById("orderForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const product_id = document.getElementById("product_id").value;
  const quantity = document.getElementById("quantity").value;

  try {
    const res = await fetch("http://127.0.0.1:5001/orders", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ product_id: parseInt(product_id), quantity: parseInt(quantity) })
    });

    const data = await res.json();

    if (!res.ok) {
      showMessage(data.error || "Erreur lors de la création", "error");
      return;
    }

    showMessage(`✅ Commande créée: #${data.order.id} (Produit ${data.order.product_id}, Quantité ${data.order.quantity})`, "success");
    await loadOrders();
  } catch (err) {
    console.error("Erreur create_order:", err);
    showMessage("Impossible de créer la commande.", "error");
  }
});

// --- Rechercher une commande ---
document.getElementById("searchForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const order_id = document.getElementById("order_id").value;

  try {
    const res = await fetch(`http://127.0.0.1:5001/orders/${order_id}`, {
      headers: { "Authorization": "Bearer " + token }
    });

    const data = await res.json();
    const detail = document.getElementById("orderDetail");
    detail.innerHTML = "";

    if (!res.ok || data.error) {
      detail.textContent = data.error || "Commande introuvable.";
      detail.className = "error";
    } else {
      detail.className = "product-card";
      detail.textContent = `Commande #${data.id} - Produit ${data.product_id} - Quantité ${data.quantity} - Statut ${data.status}`;
    }
  } catch (err) {
    console.error("Erreur search_order:", err);
    const detail = document.getElementById("orderDetail");
    detail.textContent = "Impossible de récupérer la commande.";
    detail.className = "error";
  }
});

// --- Afficher les commandes sous forme de cartes ---
async function loadOrders() {
  try {
    const res = await fetch("http://127.0.0.1:5001/orders", {
      headers: { "Authorization": "Bearer " + token }
    });
    const data = await res.json();

    const list = document.getElementById("ordersList");
    list.innerHTML = "";

    if (!res.ok || data.error) {
      list.textContent = data.error || "Impossible de charger les commandes.";
      list.className = "error";
      return;
    }

    data.forEach(order => {
      const card = document.createElement("div");
      card.className = "product-card";
      card.textContent = `Commande #${order.id} - Produit ${order.product_id} - Quantité ${order.quantity} - Statut ${order.status}`;
      list.appendChild(card);
    });
  } catch (err) {
    console.error("Erreur loadOrders:", err);
    const list = document.getElementById("ordersList");
    list.textContent = "Erreur lors du chargement des commandes.";
    list.className = "error";
  }
}

// --- Fonction utilitaire pour afficher un message ---
function showMessage(message, type) {
  const resultDiv = document.getElementById("result");
  resultDiv.textContent = message;
  resultDiv.className = type; // "error" ou "success"
}

// --- Charger les commandes au démarrage ---
loadOrders();