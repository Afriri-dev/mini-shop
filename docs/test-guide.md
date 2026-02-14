# ✅ Guide de Test Rapide – Mini‑Shop

Ce guide explique comment vérifier que l’environnement est correctement configuré après le premier lancement avec Docker Compose.

---

## 🔹 Étape 1 : Vérifier les conteneurs

```bash
docker ps

👉 Tu dois voir :
- mysql-db
- auth-service
- orders-service
- products-service


🔹 Étape 2 : Vérifier la base MySQL
Connexion au conteneur MySQL :

Bash :
docker exec -it mysql-db mysql -u root -p

Mot de passe : rootpassword
Puis vérifier les tables

SQL :

USE shopdb;
SHOW TABLES;
SELECT * FROM users;
SELECT * FROM products;
SELECT * FROM orders;

👉 Tu dois voir les données de test insérées par init.sql.

🔹 Étape 3 : Tester Auth Service
Bash :
curl http://localhost:5000/login -X POST -d '{"username":"admin","password":"admin"}' -H "Content-Type: application/json"

👉 Tu dois recevoir un token JWT si l’auth fonctionne.

🔹 Étape 4 : Tester Products Service
Bash :
curl http://localhost:3000/products

👉 Tu dois voir la liste des produits (Produit A, Produit B, etc.).

🔹 Étape 5 : Tester Orders Service
curl http://localhost:5001/orders -X POST -d '{"user_id":1,"product_id":1,"quantity":2}' -H "Content-Type: application/json"


👉 Tu dois voir une commande créée avec statut pending.

🔹 Étape 6 : Vérifier CI/CD
- Pousser une modification sur une branche feature/....
- Vérifier que GitHub Actions :
- Installe les dépendances
- Lance les tests
- Fait l’audit sécurité
- Construit et pousse l’image sur Docker Hub

🔹 Résultat attendu
- Les services démarrent sans erreur.
- La base contient les données de test.
- Les endpoints Auth, Products et Orders répondent correctement.
- Les pipelines CI/CD publient les images sur Docker Hub.

---

## 📌 Quand les développeurs peuvent commencer

👉 Les développeurs peuvent commencer **dès que** :
1. La structure du projet est créée et poussée sur GitHub (`main` propre).
2. Les fichiers essentiels (`docker-compose.yml`, `init.sql`, `.env.example`, workflows CI/CD) sont en place.
3. Le premier test avec `docker-compose up` est **réussi** (conteneurs démarrés, base initialisée, endpoints accessibles).

⚡ À ce moment-là, chaque développeur peut prendre sa branche (`feature/auth-service`, `feature/orders-service`, `feature/products-service`) et commencer à coder son microservice en suivant son README dédié.

---


```
