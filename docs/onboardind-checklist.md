# 📝 Checklist Onboarding Développeur – Mini‑Shop

Ce guide permet à chaque nouveau membre de l’équipe de démarrer rapidement et efficacement sur le projet Mini‑Shop.

---

## 🔹 Étape 1 : Préparer l’environnement
- [ ] Installer Docker et Docker Compose
- [ ] Installer Git et configurer SSH avec GitHub
- [ ] Installer Python 3.10 et Node.js 18 (si besoin pour tests locaux)
- [ ] Cloner le dépôt GitHub : `git clone https://github.com/ton-compte/mini-shop.git`

---

## 🔹 Étape 2 : Configurer le projet
- [ ] Copier le fichier `.env.example` en `.env` crée à la racine du projet
- [ ] Adapter les variables (mot de passe DB, JWT secret, etc.)( Cad “Adapter les variables d’environnement pour que tout soit cohérent” signifie aligner les valeurs du .env avec celles du docker-compose.yml, du init.sql et des services, afin que tout communique correctement.
)
- [ ] Vérifier la structure des dossiers (`auth-service`, `orders-service`, `products-service`, `shared`, `.github/workflows`)

---

## 🔹 Étape 3 : Lancer en local
- [ ] Exécuter `docker-compose up --build`
- [ ] Vérifier que les conteneurs démarrent (`docker ps`)
- [ ] Tester les endpoints :
  - Auth → `http://localhost:5000`
  - Orders → `http://localhost:5001`
  - Products → `http://localhost:3000`

---

## 🔹 Étape 4 : Vérifier la base de données
- [ ] Se connecter à MySQL : `docker exec -it mysql-db mysql -u root -p`
- [ ] Vérifier les tables (`users`, `products`, `orders`)
- [ ] Vérifier les données de test insérées par `init.sql`

---

## 🔹 Étape 5 : Tests et CI/CD
- [ ] Lancer les tests unitaires (`pytest` ou `npm test`)
- [ ] Vérifier que les pipelines GitHub Actions passent
- [ ] Vérifier que les images Docker sont poussées sur Docker Hub

---

## 🔹 Étape 6 : Workflow Git
- [ ] Créer une branche `feature/...` pour chaque nouvelle fonctionnalité
- [ ] Respecter les conventions de commit
- [ ] Ouvrir une Pull Request vers `main`
- [ ] Attendre validation CI/CD avant merge

---

## 🔹 Étape 7 : Documentation
- [ ] Lire `README.md` (racine)
- [ ] Lire le README du microservice assigné
- [ ] Lire `DEVELOPER_GUIDE.md` et `architecture-diagram.md`
- [ ] Lire `db-schema.md` pour comprendre la base
- [ ] Lire `SECURITY.md`, `STYLE_GUIDE.md`, `CONTRIBUTING.md`

---

## ✅ Résultat attendu
À la fin de cette checklist, le développeur :
- A un environnement fonctionnel
- Peut lancer et tester les services
- Comprend la structure et les règles du projet
- Est prêt à contribuer efficacement