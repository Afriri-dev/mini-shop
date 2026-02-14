
---

## 📂 `orders-service/README.md`

```markdown
# 📦 Orders Service – Mini‑Shop

Microservice de gestion des commandes basé sur **Python/Flask**.  
Il gère la création, la mise à jour et le suivi des commandes.

---

## 🚀 Démarrage

### 1. Installer les dépendances
```bash
pip install -r requirements.txt

2. Lancer en local
bash :
python src/app.py

🧪 Test
Bash :
pytest

🐳 Docker
Construire l’image

Bash :
docker build -t orders-service .

Lancer avec Docker Compose :
Bash :
docker-compose up orders-service

📖 Documentation
• 	Variables d’environnement : voir shared/env.example
• 	Base de données : shopdb (MySQL)