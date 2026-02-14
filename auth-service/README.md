# 🔑 Auth Service – Mini‑Shop

Microservice d’authentification basé sur **Python/Flask**.  
Il gère la création de comptes, la connexion et la gestion des rôles (`user`, `admin`).

---

## 🚀 Démarrage

### 1. Installer les dépendances
```bash
pip install -r requirements.txt

2. Lancer en local
python src/app.py

Le service démarre sur http://localhost:5000

🧪 Tests
pytest



🐳 Docker
Construire l’image
docker build -t auth-service .


Lancer avec Docker Compose
docker-compose up auth-service



📖 Documentation
- Variables d’environnement : voir shared/.env.example
- Base de données : shopdb (MySQL)

