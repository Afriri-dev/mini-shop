# 🔐 Bonnes pratiques de sécurité

- Toujours hacher les mots de passe avec SHA‑256 ou bcrypt.
- Ne jamais stocker les secrets en dur dans le code.
- Utiliser `.env` pour les variables sensibles.
- Vérifier les dépendances avec `npm audit` et `pip audit`.
- Intégrer Snyk dans le pipeline CI/CD.
- Limiter les droits CRUD aux utilisateurs avec rôle `admin`.