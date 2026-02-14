# 👩‍💻 Guide Développeur – Mini‑Shop

Ce document explique comment collaborer efficacement sur le projet Mini‑Shop, basé sur une architecture **microservices** et un workflow **DevSecOps**.

---

## 🔹 Organisation des branches GitHub

- **main** : branche protégée, toujours stable et validée.
- **feature/orders-service** : développement du microservice Orders (Python).
- **feature/products-service** : développement du microservice Products (Node.js).
- **feature/auth-service** : développement du microservice Auth (Python).

👉 Règles :
- Aucun push direct sur `main`.
- Toute modification passe par une **Pull Request**.
- Les tests et audits doivent être validés avant merge.

---

## 🔹 Workflow CI/CD

Chaque push ou PR déclenche un pipeline GitHub Actions :

1. **Checkout du code**
2. **Installation des dépendances**
   - Python : `pip install -r requirements.txt`
   - Node.js : `npm install`
3. **Exécution des tests**
   - Python : `pytest`
   - Node.js : `npm test`
4. **Audit sécurité**
   - Python : `pip-audit`
   - Node.js : `npm audit`
5. **Build & Push Docker**
   - Les images sont construites et poussées sur Docker Hub :
     - `DOCKERHUB_USERNAME/auth-service:latest`
     - `DOCKERHUB_USERNAME/orders-service:latest`
     - `DOCKERHUB_USERNAME/products-service:latest`

---

## 🔹 Collaboration en équipe

- **Communication** : Slack/Teams pour les échanges quotidiens.
- **Documentation vivante** : Notion/ClickUp pour centraliser les guides et checklists.
- **Agile** :
  - Sprints de 2 semaines.
  - Daily stand‑up (15 min).
  - Sprint review + retrospective.

---

## 🔹 Bonnes pratiques

- Respecter les conventions de code (`STYLE_GUIDE.md`).
- Ne jamais stocker de secrets en dur → utiliser `.env`.
- Toujours écrire des tests unitaires pour chaque nouvelle fonctionnalité.
- Documenter chaque PR avec :
  - Description claire
  - Screenshots ou logs si nécessaire
  - Checklist des tests effectués

---

## 🔹 Lancer le projet en local

### Mode développement
```bash
docker-compose up --build