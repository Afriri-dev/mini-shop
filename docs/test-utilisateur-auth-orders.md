# Scénario de test utilisateur pour Auth et Orders

Ce guide QA décrit pas-à-pas les actions qu’un testeur doit réaliser pour valider l’application graphique.

---

## Étape 1 : Inscription
1. Ouvrir l’application graphique.  
2. Aller sur l’écran **Inscription**.  
3. Créer un utilisateur avec :  
   - Username : `user1`  
   - Password : `password123`  
   - Role : `user`  
4. Vérifier que le message de confirmation s’affiche.  
5. Répéter avec un autre utilisateur :  
   - Username : `admin1`  
   - Password : `adminpass`  
   - Role : `admin`  
6. Vérifier que les deux utilisateurs sont bien enregistrés en base avec leur rôle respectif.

---

## Étape 2 : Connexion
1. Aller sur l’écran **Connexion**.  
2. Se connecter avec `user1`.  
3. Vérifier que l’UI affiche un état connecté (par ex. bouton “Déconnexion”).  
4. Vérifier que les menus affichés correspondent au rôle `user` (accès limité).  
5. Se déconnecter.  
6. Se connecter avec `admin1`.  
7. Vérifier que l’UI affiche les menus avancés (gestion des utilisateurs et commandes).

---

## Étape 3 : Création de commande
1. Connecté en tant que `user1`, aller sur l’écran **Nouvelle commande**.  
2. Sélectionner un produit fictif (ex. `product_id = 101`).  
3. Saisir une quantité (ex. `2`).  
4. Valider et vérifier que le message “Commande créée avec succès” s’affiche.  
5. Vérifier que la commande est bien associée à `user1`.

---

## Étape 4 : Liste des commandes
1. Connecté en tant que `user1`, aller sur l’écran **Mes commandes**.  
2. Vérifier que seules les commandes de `user1` apparaissent.  
3. Se déconnecter.  
4. Se connecter avec `admin1`.  
5. Aller sur l’écran **Toutes les commandes**.  
6. Vérifier que l’admin voit toutes les commandes, y compris celles de `user1`.

---

## Étape 5 : Vérification des rôles et permissions
- Tenter d’accéder à une page réservée aux admins avec `user1`.  
- Vérifier que l’UI affiche un message “Accès refusé”.  
- Vérifier que l’admin peut accéder à toutes les pages.

---

## Étape 6 : Santé des services
- Vérifier que l’UI affiche l’état des services :  
  - Auth : ✅ OK  
  - Orders : ✅ OK  
- Simuler une panne (arrêter un service) et vérifier que l’UI affiche “Service indisponible”.

---

## Résultat attendu
- Les rôles `admin` et `user` sont respectés.  
- Les commandes sont correctement créées et filtrées.  
- L’UI reflète fidèlement les permissions et l’état des services.  
- Les erreurs sont affichées clairement et l’application reste cohérente.