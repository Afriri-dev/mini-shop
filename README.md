# 🛒 Mini‑Shop – Microservices E‑Commerce

Mini‑Shop est une application e‑commerce basée sur une architecture **microservices**.  
Elle inclut trois services principaux :

- **Auth Service** (Python/Flask) → gestion des utilisateurs et authentification
- **Orders Service** (Python/Flask) → gestion des commandes
- **Products Service** (Node.js/Express) → gestion des produits

Une base de données **MySQL** est utilisée pour stocker les données.

---

## 🚀 Démarrage rapide

### 1. Cloner le projet

```bash
git clone https://github.com/ton-compte/mini-shop.git
cd mini-shop
2. Créer le fichier .env
Copier le modèle :
cp shared/.env.example .env

Puis adapter les valeurs (mot de passe DB, secret JWT, etc.).

Lancer avec Docker Compose

Mode développement (par défaut):

docker-compose up --build

👉 Ce mode utilise docker-compose.yml + docker-compose.override.yml :
- Les volumes montent le code local → pas besoin de rebuild à chaque modification.
- Les services tournent en mode dev (FLASK_ENV=development, NODE_ENV=development).
- Les changements dans le code sont rechargés automatiquement.

Mode production

docker-compose -f docker-compose.yml up --build -d

👉 Ce mode utilise uniquement docker-compose.yml :
- Les images sont construites et figées.
- Pas de volumes montés.
- Les services tournent en mode stable.

📂 Structure du proje

mini-shop/
├── auth-service/          # Microservice Auth (Python/Flask)
├── orders-service/        # Microservice Orders (Python/Flask)
├── products-service/      # Microservice Products (Node.js/Express)
├── shared/                # Ressources communes (init.sql, .env.example, guides)
├── docs/                  # Documentation (schémas, diagrammes)
├── .github/workflows/     # Pipelines CI/CD
├── docker-compose.yml     # Orchestration globale (prod)
├── docker-compose.override.yml # Config dev
└── README.md              # Documentation principale

🔐 Sécurité et CI/CD
• 	Les pipelines CI/CD exécutent :
• 	Tests unitaires (pytest,nmp test )
• 	Audit des dépendances (pip audit,nmp audit )
• 	Build et push des images Docker sur Docker Hub
• 	La branche (main) est protégée → uniquement mise à jour via Pull Request validée.

👥 Contribution
Voir :
• shared/CONTRIBUTING.md	 → guide de contribution
• shared/STYLE_GUIDE	 → conventions de code
• shared/AGILE_GUIDE	 → organisation Agile
• shared/SECURITY	 → bonnes pratiques DevSecOps


---

⚡ En résumé :
- Le **README principal** explique comment cloner, configurer `.env`, lancer en mode dev ou prod.
- Il documente la structure du projet et rappelle les règles CI/CD et sécurité.
- Tes développeurs auront un guide clair dès qu’ils ouvrent le repo.

👉 Veux-tu que je prépare aussi un **README spécifique pour chaque microservice** (Auth, Orders, Products), afin que chaque développeur ait son guide dédié dans son dossier ?
```
