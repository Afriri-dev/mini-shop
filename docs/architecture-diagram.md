# 🏗️ Diagramme d’Architecture – Mini‑Shop

Ce diagramme illustre la communication entre les différents microservices et la base de données MySQL.

---

## 🔹 Description

- **Auth Service (Python/Flask)**  
  - Gère l’authentification et les rôles des utilisateurs.  
  - Communique avec la base MySQL pour stocker et vérifier les identifiants.  

- **Orders Service (Python/Flask)**  
  - Gère la création et le suivi des commandes.  
  - Communique avec Auth Service pour vérifier l’identité de l’utilisateur.  
  - Communique avec Products Service pour vérifier la disponibilité des produits.  
  - Stocke les commandes dans MySQL.  

- **Products Service (Node.js/Express)**  
  - Gère le catalogue des produits.  
  - Communique avec MySQL pour stocker et mettre à jour les produits.  
  - Fournit les informations produits à Orders Service.  

- **MySQL Database**  
  - Base centrale `shopdb`.  
  - Contient les tables `users`, `products`, `orders`.  
  - Initialisée via `shared/init.sql`.  

---

## 🔹 Schéma ASCII (vue simplifiée)
      +-------------------+
      |   Auth Service    |
      |   (Python/Flask)  |
      +---------+---------+
                |
                | Vérifie utilisateurs
                v
      +-------------------+
      |  Orders Service   |
      |   (Python/Flask)  |
      +---------+---------+
                |
    +-----------+-----------+
    |                       |
    v                       v
    +-------------------+   +-------------------+ | Products Service  |   |   MySQL Database  | | (Node.js/Express) |   |      shopdb       | +-------------------+   +-------------------+


---

## 🔹 Notes

- Les services sont orchestrés via **Docker Compose**.  
- Les images sont construites et poussées sur **Docker Hub** via CI/CD.  
- Les variables d’environnement sont centralisées dans `.env`.  
- La base MySQL est initialisée automatiquement avec `init.sql`.  

---

## 🔹 Documentation complémentaire

- Voir `DEVELOPER_GUIDE.md` pour le workflow collaboratif.  
- Voir `SECURITY.md` pour les bonnes pratiques DevSecOps.  
- Voir `STYLE_GUIDE.md` pour les conventions de code.  