# Modèles d'issues GitHub — Sprints 1, 2, 3, 4

**Instructions :** Copiez chaque bloc ci-dessous dans une nouvelle issue GitHub (onglet Issues → New issue).  
Assurez-vous de créer les labels `sprint-1`, `sprint-2`, `sprint-3` et les milestones correspondants si nécessaire.

---

## SPRINT 1 — Fondation SaaS

---

### Issue 1.1 : [Sprint 1] Modèle tenant + lien users

**Labels :** `sprint-1`  
**Milestone :** Sprint 1 - Fondation SaaS

#### Description

Créer le modèle multi-tenant à la base du SaaS :

- Table `tenants` avec : `id` (UUID), `slug` (unique), `name`, `status`, `trial_started_at`, `trial_ends_at`, `created_at`, `updated_at`
- Ajouter `tenant_id` (FK vers `tenants.id`) sur la table `users`
- Migration SQL ou mise à jour de `init.sql`

#### Critères d'acceptation

- [ ] Table `tenants` créée avec les champs requis
- [ ] `users.tenant_id` NOT NULL pour les nouveaux utilisateurs (ou contrainte adaptée)
- [ ] Index sur `tenants.status` et `tenants.trial_ends_at`
- [ ] Migration réversible ou documentée

---

### Issue 1.2 : [Sprint 1] Inscription "créer ma boutique"

**Labels :** `sprint-1`  
**Milestone :** Sprint 1 - Fondation SaaS

#### Description

Nouveau parcours d'inscription : l'utilisateur crée **sa boutique** (tenant) et devient admin.

- Création du tenant avec `trial_started_at = NOW()`, `trial_ends_at = NOW() + 60 jours`, `status = 'trial'`
- Slug unique (généré ou saisi, validation)
- Création du premier user (admin) lié à ce tenant
- Route API : `POST /auth/signup-boutique` ou équivalent

#### Critères d'acceptation

- [ ] Un tenant + un user admin sont créés en une transaction
- [ ] Slug unique et validé (format, unicité)
- [ ] Essai 60 jours correctement renseigné
- [ ] Tests unitaires ou d'intégration passent

---

### Issue 1.3 : [Sprint 1] Login avec JWT incluant tenant_id

**Labels :** `sprint-1`  
**Milestone :** Sprint 1 - Fondation SaaS

#### Description

Adapter le login pour inclure `tenant_id` dans le JWT (claims).

- Lors du login, charger le `tenant_id` du user
- Inclure `tenant_id` dans le payload JWT
- Les autres services (orders, products) pourront filtrer par tenant à partir du token

#### Critères d'acceptation

- [ ] JWT contient `user_id` et `tenant_id`
- [ ] Route `/auth/login` retourne un token valide avec ces claims
- [ ] Tests vérifient la présence de `tenant_id` dans le token décodé

---

### Issue 1.4 : [Sprint 1] Garde d'accès — bloquer si essai terminé / suspendu

**Labels :** `sprint-1`  
**Milestone :** Sprint 1 - Fondation SaaS

#### Description

Middleware ou décorateur qui vérifie que le tenant a le droit d'accéder à la plateforme.

- Si `status = 'suspended'` ou `status = 'closed'` → **403** avec code métier `SUBSCRIPTION_EXPIRED`
- Si `status = 'trial'` et `NOW() > trial_ends_at` → passer en `suspended` (ou refuser l'accès) et retourner 403
- Appliquer sur les routes protégées (auth, orders, products, etc.)

#### Critères d'acceptation

- [ ] Requête avec tenant suspendu → 403 + `SUBSCRIPTION_EXPIRED`
- [ ] Requête avec essai expiré → 403
- [ ] Requête avec tenant en trial valide → accès autorisé
- [ ] Tests automatisés couvrent ces cas

---

### Issue 1.5 : [Sprint 1] Job / tâche — passage trial → suspended

**Labels :** `sprint-1`  
**Milestone :** Sprint 1 - Fondation SaaS

#### Description

Tâche planifiée (cron, worker, ou exécution périodique) qui met à jour les tenants dont l'essai est terminé.

- Trouver les tenants avec `status = 'trial'` et `trial_ends_at < NOW()`
- Les passer à `status = 'suspended'`
- Optionnel : ne pas toucher ceux qui ont déjà un paiement enregistré (pour plus tard)

#### Critères d'acceptation

- [ ] Les tenants dont l'essai est dépassé passent à `suspended`
- [ ] Exécution documentée (cron, manuelle, ou au login)
- [ ] Tests ou script de vérification fourni

---

### Issue 1.6 : [Sprint 1] Tests + CI pour fondation tenant

**Labels :** `sprint-1`  
**Milestone :** Sprint 1 - Fondation SaaS

#### Description

- Tests unitaires ou d'intégration pour : création tenant, login, blocage accès suspendu
- CI : s'assurer que les tests passent sur les services modifiés
- Pas de régression sur les tests existants

#### Critères d'acceptation

- [ ] Tests passent localement et en CI
- [ ] Couverture des scénarios critiques (création tenant, accès refusé)

---

## SPRINT 2 — Domaine métier (catalogue + stock)

---

### Issue 2.1 : [Sprint 2] Produits CRUD avec tenant_id

**Labels :** `sprint-2`  
**Milestone :** Sprint 2 - Catalogue & Stock

#### Description

Adapter le service produits pour le multi-tenant :

- Ajouter `tenant_id` sur la table `products`
- Toutes les requêtes (GET, POST, PUT, DELETE) filtrent par `tenant_id` issu du JWT
- Un tenant ne peut jamais voir ou modifier les produits d'un autre tenant

#### Critères d'acceptation

- [ ] `products.tenant_id` NOT NULL
- [ ] GET /products ne retourne que les produits du tenant connecté
- [ ] POST /products assigne automatiquement le tenant_id
- [ ] Tentative d'accès à un produit d'un autre tenant → 404
- [ ] Tests d'isolation entre tenants

---

### Issue 2.2 : [Sprint 2] Stock avec tenant_id

**Labels :** `sprint-2`  
**Milestone :** Sprint 2 - Catalogue & Stock

#### Description

Gestion du stock par tenant :

- Table ou champs de stock liés aux produits (déjà ou à créer)
- Toutes les opérations stock (entrée, sortie, ajustement) scoped par `tenant_id`
- Vérifier que le produit appartient au tenant avant toute opération

#### Critères d'acceptation

- [ ] Stock isolé par tenant
- [ ] Opérations CRUD ou mouvements validés (produit ∈ tenant)
- [ ] Tests vérifiant l'isolation

---

### Issue 2.3 : [Sprint 2] Commandes avec tenant_id

**Labels :** `sprint-2`  
**Milestone :** Sprint 2 - Catalogue & Stock

#### Description

Adapter le service commandes pour le multi-tenant :

- `orders.tenant_id` (ou déduction via user → tenant)
- Les commandes ne concernent que les produits du tenant
- Isolation stricte : un tenant ne voit jamais les commandes d'un autre

#### Critères d'acceptation

- [ ] Orders filtrés par tenant
- [ ] Création de commande valide le produit (même tenant)
- [ ] Tests d'isolation

---

### Issue 2.4 : [Sprint 2] Tests d'isolation multi-tenant

**Labels :** `sprint-2`  
**Milestone :** Sprint 2 - Catalogue & Stock

#### Description

Tests qui prouvent qu'il n'y a pas de fuite de données entre tenants.

- Créer deux tenants (A et B)
- Créer des produits pour A
- Avec un token tenant B : aucun produit de A ne doit être visible
- Idem pour les commandes

#### Critères d'acceptation

- [ ] Tests automatisés passent
- [ ] Aucune requête ne retourne de données d'un autre tenant

---

## SPRINT 3 — Branding + Durcissement

---

### Issue 3.1 : [Sprint 3] Table tenant_branding + API GET branding

**Labels :** `sprint-3`  
**Milestone :** Sprint 3 - Branding & Expérience

#### Description

- Créer table `tenant_branding` (tenant_id, display_name, primary_color, secondary_color, accent_color, logo_url)
- Route `GET /tenants/me/branding` : retourne le branding du tenant connecté (ou valeurs par défaut)
- JWT utilisé pour identifier le tenant

#### Critères d'acceptation

- [ ] Table créée avec FK vers tenants
- [ ] GET retourne JSON (couleurs, display_name, logo_url nullable)
- [ ] Si pas de branding : valeurs par défaut ou null
- [ ] Route protégée (authentification requise)

---

### Issue 3.2 : [Sprint 3] API PATCH branding (admin uniquement)

**Labels :** `sprint-3`  
**Milestone :** Sprint 3 - Branding & Expérience

#### Description

- Route `PATCH /tenants/me/branding` : mise à jour des champs (display_name, couleurs)
- Réservé aux admins du tenant (rôle ou propriétaire)
- Validation : couleurs au format hex (#RRGGBB), pas de HTML arbitraire dans display_name

#### Critères d'acceptation

- [ ] PATCH met à jour tenant_branding
- [ ] Validation des couleurs (regex ou lib)
- [ ] Sanitisation display_name (éviter XSS)
- [ ] Non-admin → 403

---

### Issue 3.3 : [Sprint 3] Front — appliquer thème depuis l'API

**Labels :** `sprint-3`  
**Milestone :** Sprint 3 - Branding & Expérience

#### Description

- Après login, appeler `GET /tenants/me/branding`
- Injecter les couleurs en variables CSS (`:root { --color-primary: ... }`)
- Afficher `display_name` et logo dans le header / layout

#### Critères d'acceptation

- [ ] Thème appliqué dynamiquement
- [ ] Nom de la boutique visible
- [ ] Logo affiché si présent (sinon placeholder ou vide)
- [ ] Fallback si l'API échoue (couleurs par défaut)

---

### Issue 3.4 : [Sprint 3] Page paramètres "Apparence de ma boutique"

**Labels :** `sprint-3`  
**Milestone :** Sprint 3 - Branding & Expérience

#### Description

- Écran de paramètres où l'admin peut modifier display_name, couleurs
- Aperçu en direct ou rafraîchi après sauvegarde
- Appel PATCH à l'API pour persister

#### Critères d'acceptation

- [ ] Formulaire avec champs : nom affiché, couleur primaire, secondaire
- [ ] Bouton Sauvegarder → PATCH API
- [ ] Feedback succès / erreur
- [ ] Accès restreint aux admins du tenant

---

### Issue 3.5 : [Sprint 3] Doc / runbook essai + suspension

**Labels :** `sprint-3`  
**Milestone :** Sprint 3 - Branding & Expérience

#### Description

Documenter le comportement essai gratuit et suspension pour l'équipe (et éventuellement le support).

- Règles : 60 jours à partir de quand ? Que se passe-t-il à J+60 ?
- Où sont les jobs qui passent trial → suspended ?
- Comment simuler un essai expiré en dev/test ?
- Où sont stockés les secrets (DB, JWT, etc.) ?

#### Critères d'acceptation

- [ ] Doc à jour dans `docs/` ou wiki
- [ ] Runbook exploitable par un dev ou ops

---

## Récapitulatif des labels à créer

Dans GitHub : **Issues → Labels → New label**

- `sprint-1` (ex. bleu)
- `sprint-2` (ex. vert)
- `sprint-3` (ex. violet)

## Récapitulatif des milestones à créer

Dans GitHub : **Issues → Milestones → New milestone**

- **Sprint 1 - Fondation SaaS**
- **Sprint 2 - Catalogue & Stock**
- **Sprint 3 - Branding & Expérience**

---

*Ce fichier peut être versionné et mis à jour au fil des sprints.*

---

## SPRINT 4 — Facturation & Offline Sync (web-first)

---

### Issue 4.1 : [Sprint 4] Modèle facture (tenant) + statuts draft/issued

**Labels :** `sprint-4`  
**Milestone :** Sprint 4 - Facturation & Offline

#### Description

Créer le modèle de données de factures multi-boutiques :

- Table `invoices` (ou équivalent) scannée par `tenant_id`
- Champs recommandés :
  - `id` (UUID ou INT)
  - `tenant_id`
  - `invoice_number` (numéro final, format recommandé `TENANT-000123`)
  - `status` (ex. `draft_local`, `pending_sync`, `issued`, `cancelled`, `sync_error`)
  - `currency`, `issued_at`
  - `customer_name`, `customer_email` (si nécessaire)
  - `totals` (ou via une table de lignes + calcul côté serveur)
  - `offline_event_id` (idempotency key côté client)
  - `created_at`, `updated_at`
- Table `invoice_items` (lignes) également scoped par `tenant_id` et liées à la facture

#### Critères d'acceptation

- [ ] `invoices.tenant_id` est obligatoire (pas de fuite inter-tenant)
- [ ] `offline_event_id` est stocké et sert de clé d'idempotence
- [ ] Statuts supportés : au minimum `draft_local`, `pending_sync`, `issued`
- [ ] Tests (ou scripts) pour valider l'isolation tenant_id
- [ ] `invoice_number` respecte strictement le format `TENANT-000123` (où `TENANT` = `tenant_code` normalisé en majuscules, sans caractères spéciaux)

---

### Issue 4.2 : [Sprint 4] Stratégie offline des numéros (recommandée: plages allouées)

**Labels :** `sprint-4`  
**Milestone :** Sprint 4 - Facturation & Offline

#### Description

Définir la stratégie permettant la génération de numéros en mode offline :

Option MVP (recommandée):
- Le serveur alloue des **plages de numéros** à la boutique (ex. 1001..1200) à l'avance.
- En offline, la boutique utilise les numéros de la plage courante pour produire le “brouillon imprimable”.
- À la reconnexion, le serveur valide/commit et rend le PDF final avec le même numéro.

Actions à fournir :
- Table `invoice_number_ranges` :
  - `tenant_id`, `range_start`, `range_end`, `next_number`, `allocated_at`, `consumed_at`
  - verrouillage atomique lors du “consuming” du prochain numéro (à faire côté serveur au sync)

#### Critères d'acceptation

- [ ] Le numéro d'une facture offline reste cohérent après synchronisation
- [ ] En cas de double envoi (même `offline_event_id`), pas de double consommation
- [ ] Test pour deux factures offline envoyées ensuite : numéros uniques et cohérents
- [ ] Le mapping final génère `invoice_number = <TENANT>-<SEQ_PADDED_6>` (ex. `TENANT-000123`), où `<TENANT>` provient de `tenants.tenant_code`

---

### Issue 4.3 : [Sprint 4] Idempotence et file d'événements offline côté client + backend

**Labels :** `sprint-4`  
**Milestone :** Sprint 4 - Facturation & Offline

#### Description

Mise en place d'une synchronisation robuste :

- Le client enregistre une action offline avec un `offline_event_id` unique (UUID v4 généré localement).
- Le backend expose un endpoint de sync :
  - `POST /sync/invoices` (ou `POST /sync/events`)
  - Le payload contient : `tenant_id` (déduit du JWT) + `offline_event_id` + contenu facture (items, totaux, etc.)
- Le backend :
  - valide le tenant + son statut (trial/expired)
  - traite l'événement **idempotemment** :
    - si `offline_event_id` déjà connu → retourner le mapping vers `invoice_id` / status sans réappliquer
  - renvoie un mapping : `offline_event_id -> invoice_id, final invoice_number, status`

#### Critères d'acceptation

- [ ] Envoi 2 fois du même `offline_event_id` ne crée pas 2 factures
- [ ] Le backend retourne un mapping cohérent même après réessai
- [ ] Les erreurs de validation renvoient un message exploitable côté client

---

### Issue 4.4 : [Sprint 4] Rendu brouillon offline + PDF final identique (signature serveur)

**Labels :** `sprint-4`  
**Milestone :** Sprint 4 - Facturation & Offline

#### Description

Définir le rendu en deux étapes :

1) **Offline** :
   - Générer un rendu brouillon (HTML/CSS) imprimable immédiatement
   - Marquer clairement : `BROUILLON - NON FINAL`
   - Ne pas exiger de signature hors ligne

2) **Au retour en ligne** :
   - Le serveur génère le PDF final à partir d'une source “canonique” (invoice + items)
   - Le PDF final est “identique” au brouillon dans la mesure du possible
   - Signature serveur (si vous avez l'exigence de signature) dans la phase finale

Support :
- Route serveur : `GET /invoices/{id}/pdf` retourne le PDF final

#### Critères d'acceptation

- [ ] Offline : page brouillon accessible et imprimable
- [ ] Après sync : statut passe à `issued` et PDF final disponible
- [ ] Le brouillon et le final partagent la même structure/template
- [ ] Les divergences éventuelles sont documentées (font rendering, etc.)

---

### Issue 4.5 : [Sprint 4] Gestion des conflits (offline vs online) : politique MVP

**Labels :** `sprint-4`  
**Milestone :** Sprint 4 - Facturation & Offline

#### Description

Définir la politique de conflit pour MVP :

- Option MVP simple :
  - Une facture avec `status != draft_local` n'est plus modifiable (après `issued`)
  - Si un événement offline arrive pour une facture déjà `issued` → refuser avec une erreur métier
- Documenter la politique et l'implémenter côté backend

#### Critères d'acceptation

- [ ] Deux syncs offline pour la même facture logique → résultat déterministe
- [ ] Une tentative de modification après `issued` renvoie 409/validation error
- [ ] Tests couvrent au moins 1 cas de conflit

---

### Issue 4.6 : [Sprint 4] PWA web offline (cache + stockage local des brouillons)

**Labels :** `sprint-4`  
**Milestone :** Sprint 4 - Facturation & Offline

#### Description

Rendre l'app web utilisable en offline :

- Transformer le front en PWA minimal (service worker)
- Stocker les brouillons factures en local (IndexedDB)
- Lancer la sync dès que connexion détectée

#### Critères d'acceptation

- [ ] Déconnexion internet : écran facture + brouillon fonctionnent
- [ ] Les brouillons sont persistés et synchronisés au retour en ligne
- [ ] UI indique clairement `pending_sync` et `issued`

---

### Issue 4.7 : [Sprint 4] Tests & CI pour synchronisation offline

**Labels :** `sprint-4`  
**Milestone :** Sprint 4 - Facturation & Offline

#### Description

Mettre en place des tests backend :

- Tests d'idempotence `offline_event_id`
- Tests de validation tenant_id + statut (trial/suspended)
- Tests des statuts : `draft_local` -> `pending_sync` -> `issued`

#### Critères d'acceptation

- [ ] Tous les tests passent en CI sans nécessiter d'UI navigateur
- [ ] Au moins un test couvre la ré-exécution d'un événement offline

---

## Récapitulatif des labels/milestones à créer

- Label : `sprint-4`
- Milestone : `Sprint 4 - Facturation & Offline`
