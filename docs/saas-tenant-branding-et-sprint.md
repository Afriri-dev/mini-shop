# SaaS multi-boutiques — Schéma minimal & ordre des stories (sprint)

Contexte rappelé : plusieurs boutiques, essai gratuit 2 mois puis coupure sans paiement, personnalisation d’interface par boutique.

---

## 1. Schéma SQL minimal (`tenants` + branding)

```sql
-- Extension possible de votre base actuelle (ex. shopdb)
-- Une ligne par boutique (tenant).

CREATE TABLE IF NOT EXISTS tenants (
    id              CHAR(36) NOT NULL PRIMARY KEY,  -- UUID recommandé
    slug            VARCHAR(64) NOT NULL UNIQUE,   -- ex. chez-moi (URL / sous-domaine)
    name            VARCHAR(255) NOT NULL,         -- nom légal ou commercial
    status          ENUM('trial', 'active', 'past_due', 'suspended', 'closed')
                    NOT NULL DEFAULT 'trial',
    trial_started_at DATETIME(3) NOT NULL,
    trial_ends_at    DATETIME(3) NOT NULL,          -- ex. trial_started_at + 60 jours
    created_at       DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    updated_at       DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    INDEX idx_tenants_status (status),
    INDEX idx_tenants_trial_ends (trial_ends_at)
);

-- Personnalisation visuelle (1–1 avec tenant, ou colonnes directement sur tenants si vous préférez une seule table au MVP)

CREATE TABLE IF NOT EXISTS tenant_branding (
    tenant_id       CHAR(36) NOT NULL PRIMARY KEY,
    display_name    VARCHAR(255) NULL,              -- nom affiché dans l’UI (si différent de tenants.name)
    logo_url        VARCHAR(2048) NULL,             -- URL stockage objet (S3, etc.)
    primary_color   VARCHAR(7) NULL,                -- ex. #1a2b3c
    secondary_color VARCHAR(7) NULL,
    accent_color    VARCHAR(7) NULL,
    updated_at      DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
    CONSTRAINT fk_branding_tenant FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
);
```

**Lien avec les utilisateurs existants** : ajouter `tenant_id` (FK vers `tenants.id`) sur la table `users` (ou table `memberships` si un utilisateur peut appartenir à plusieurs boutiques plus tard).

**État d’accès** (règle métier) :

| `status`     | Accès plateforme (à définir en produit)        |
|-------------|------------------------------------------------|
| `trial`     | Oui si `NOW() < trial_ends_at`               |
| `active`    | Oui (payant à jour)                           |
| `past_due`  | Souvent grâce / lecture seule / bientôt coupé |
| `suspended` | Non (essai terminé sans paiement, etc.)       |
| `closed`    | Non                                           |

Un **job planifié** (cron / worker) peut passer `trial` → `suspended` quand `trial_ends_at` est dépassé et aucun paiement enregistré.

---

## 2. API minimale (pour le front)

| Méthode | Route | Rôle |
|--------|--------|------|
| `GET`  | `/tenants/me/branding` | Branding du tenant courant (JWT contient `tenant_id`) |
| `PATCH`| `/tenants/me/branding` | Mise à jour (admin boutique) — couleurs, `display_name` |
| `POST` | `/tenants/me/branding/logo` | Upload logo → retourne `logo_url` (ou URL signée) |

Réponses d’erreur si abonnement expiré : code métier dédié (ex. `SUBSCRIPTION_EXPIRED`) pour afficher l’écran de paiement.

---

## 3. Front — application du thème

1. Après login, appeler `GET /tenants/me/branding`.
2. Injecter en `:root` des **variables CSS** : `--color-primary`, `--color-secondary`, etc.
3. Afficher `display_name` + logo dans le header / layout.

Exemple (conceptuel) :

```css
:root {
  --color-primary: var(--tenant-primary, #1976d2);
}
```

---

## 4. Ordre des stories — **prochain sprint** (suggestion)

Priorité : poser **tenant + essai + branding** avant d’enrichir le catalogue.

| # | Story | Critères d’acceptation (résumé) |
|---|--------|----------------------------------|
| 1 | Créer compte **boutique** (tenant) + premier admin | `tenants` + `users.tenant_id` ; `trial_*` renseignés (+60 j) ; slug unique. |
| 2 | **Bloquer l’accès** si essai terminé et non payé | Middleware / gateway : 403 + code `SUBSCRIPTION_EXPIRED` ; statut `suspended`. |
| 3 | **GET branding** pour le tenant connecté | JSON avec couleurs + `display_name` + `logo_url` (nullable). |
| 4 | **PATCH branding** (rôle admin boutique uniquement) | Mise à jour `tenant_branding` ; validation couleur hex ; pas de HTML arbitraire. |
| 5 | **Front** : appliquer variables CSS depuis l’API | Écran paramètres “Apparence” + preview. |
| 6 | (Si temps) **Upload logo** | Presigned URL ou multipart → `logo_url` ; limite taille + type MIME. |

**Definition of Done** commune : tests sur règles d’accès + pas de fuite de données entre `tenant_id`.

---

## 5. Suite (sprint suivant)

- Webhooks paiement (Stripe, etc.) → `status = active`.
- Emails J-7 / J-1 fin d’essai.
- Export données si compte suspendu (selon CGU).

---

*Document généré pour cadrage produit / technique — à ajuster selon votre PSP et votre politique exacte après essai.*
