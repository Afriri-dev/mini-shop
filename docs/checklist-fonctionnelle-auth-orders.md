# Checklist fonctionnelle pour Auth et Orders

## Auth Service

### Inscription
- Saisir un nouvel utilisateur avec `username`, `password` et `role` (admin ou user).
- Vérifier que l’utilisateur est créé en base avec le bon rôle.
- Cas de test : créer un utilisateur `admin` et un utilisateur `user`.

### Connexion
- Se connecter avec un utilisateur existant.
- Vérifier que le JWT généré contient le rôle.
- Vérifier que l’UI affiche un état connecté.
- Vérifier que les options affichées dépendent du rôle :
  - **Admin** : accès à la gestion des utilisateurs et commandes.
  - **User** : accès limité à ses propres commandes.

### Santé
- Vérifier que l’UI peut afficher l’état du service Auth.

---

## Orders Service

### Création de commande
- Créer une commande avec `user_id`, `product_id`, `quantity`.
- Vérifier que la commande est insérée en base.
- Vérifier que le rôle `user` peut créer une commande.
- Vérifier que le rôle `admin` peut créer une commande (si prévu).

### Liste des commandes
- **Admin** : voir toutes les commandes.
- **User** : voir uniquement ses propres commandes.
- Vérifier que l’UI filtre correctement selon le rôle.

### Santé
- Vérifier que l’UI peut afficher l’état du service Orders.

---

## Intégration Auth ↔ Orders

### Workflow complet
1. Créer un utilisateur avec rôle `user`.
2. Se connecter → créer une commande → vérifier qu’il ne voit que ses commandes.
3. Créer un utilisateur avec rôle `admin`.
4. Se connecter → vérifier qu’il voit toutes les commandes.

---

## Frontend (UI globale)
- Vérifier que les appels API sont routés vers les bons services.
- Vérifier que les erreurs sont affichées clairement (ex. mauvais mot de passe, accès refusé).
- Vérifier que l’UI reste cohérente même si un service est indisponible.

---

## Résultat attendu
- Auth gère correctement l’inscription, la connexion et les rôles.
- Orders gère la création et la récupération des commandes.
- Les rôles `admin` et `user` sont respectés dans l’UI.
- L’UI reflète fidèlement les permissions et l’état des services.