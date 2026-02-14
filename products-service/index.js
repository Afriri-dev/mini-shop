const express = require("express");
const app = express();
app.use(express.json());

// Exemple de route GET
app.get("/products", (req, res) => {
  res.json([{ id: 1, name: "Sample", price: 100 }]);
});

// Route POST manquante
app.post("/products", (req, res) => {
  const { name, price } = req.body;
  // Ici tu insères dans MySQL
  res.json({ message: `Product ${name} added successfully!` });
});

app.listen(3000, () => {
  console.log("Products Service running on port 3000");
});