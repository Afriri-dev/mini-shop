function loadProducts() {
  const productsDiv = document.getElementById("products");

  const mockProducts = [
    { id: 1, name: "Chaussures", price: 50 },
    { id: 2, name: "T-shirt", price: 20 },
    { id: 3, name: "Casquette", price: 15 }
  ];

  productsDiv.innerHTML = mockProducts.map(p =>
    `<div>
       <h3>${p.name}</h3>
       <p>Prix: ${p.price} €</p>
       <button onclick="alert('🛒 Produit ${p.id} ajouté au panier')">Ajouter au panier</button>
     </div>`
  ).join("");
}

loadProducts();