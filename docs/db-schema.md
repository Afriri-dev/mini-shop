# 🗄️ Schéma de Base de Données – Mini‑Shop

La base de données **MySQL** utilisée par Mini‑Shop s’appelle `shopdb`.  
Elle contient trois tables principales : `users`, `products`, `orders`.

---

## 🔹 Tables

### 1. `users`
- `id` (INT, PK, AUTO_INCREMENT) → identifiant unique
- `username` (VARCHAR(50), UNIQUE) → nom d’utilisateur
- `password` (VARCHAR(255)) → mot de passe haché
- `role` (ENUM: 'user', 'admin') → rôle de l’utilisateur

### 2. `products`
- `id` (INT, PK, AUTO_INCREMENT) → identifiant unique
- `name` (VARCHAR(100)) → nom du produit
- `price` (DECIMAL(10,2)) → prix du produit
- `stock` (INT) → quantité disponible

### 3. `orders`
- `id` (INT, PK, AUTO_INCREMENT) → identifiant unique
- `user_id` (INT, FK → users.id) → utilisateur ayant passé la commande
- `product_id` (INT, FK → products.id) → produit commandé
- `quantity` (INT) → nombre d’unités commandées
- `status` (ENUM: 'pending', 'confirmed', 'shipped') → état de la commande

---

## 🔹 Relations

- **Un utilisateur** peut passer **plusieurs commandes** → relation 1‑N entre `users` et `orders`.
- **Un produit** peut apparaître dans **plusieurs commandes** → relation 1‑N entre `products` et `orders`.
- La table `orders` fait le lien entre `users` et `products`.

---

## 🔹 Schéma ASCII

+---------+        +-----------+        +-----------+ |  users  |        |  orders   |        | products  | +---------+        +-----------+        +-----------+ | id (PK) |<----+  | id (PK)   |  +---> | id (PK)   | | username|      |  | user_id FK|       | name       | | password|      |  | product_id FK|    | price      | | role    |      |  | quantity  |       | stock      | +---------+      |  | status    |       +-----------+ +-----------+


---

## 🔹 Notes

- Les mots de passe doivent être **hachés** (bcrypt ou SHA‑256).  
- Les rôles permettent de limiter les droits (`admin` vs `user`).  
- Les commandes passent par un cycle : `pending` → `confirmed` → `shipped`.  
- Le script `shared/init.sql` initialise la base avec des données de test.  

---

## 🔹 Documentation complémentaire

- Voir `architecture-diagram.md` pour la communication entre services.  
- Voir `SECURITY.md` pour les bonnes pratiques de sécurité.  
- Voir `DEVELOPER_GUIDE.md` pour le workflow collaboratif.