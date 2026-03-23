Mini-checklist Test en Local

Cette checklist rapide est destinée à l’équipe Mini-Shop pour valider le pipeline CI/CD avant chaque push.

1. Préparation

[ ] Vérifier que Docker est installé et fonctionne (docker info).

[ ] Installer les dépendances (pip install -r requirements.txt, npm install).

[ ] Vérifier que les secrets (DockerHub, etc.) sont configurés.

2. Tests locaux

[ ] Unitaires & intégration : pytest (Auth/Orders), npm test (Products).

[ ] Fonctionnels : pytest -m functional, npx cypress run (Frontend).

[ ] Performance : locust ou artillery.

[ ] Régression : pytest --lf, npm test -- --onlyChanged.

3. Build Docker

[ ] docker build -t local/auth-service ./auth-service

[ ] docker build -t local/orders-service ./orders-service

[ ] docker build -t local/products-service ./products-service

[ ] docker build -t local/frontend ./frontend

4. Smoke tests

[ ] Démarrer les conteneurs : docker-compose up.

[ ] Vérifier les endpoints :

curl -f http://localhost:5000/auth/health

curl -f http://localhost:5001/orders/health

curl -f http://localhost:5002/products/health

curl -f http://localhost:3000/frontend/health

5. Validation finale

[ ] Tous les tests passent.

[ ] Les images Docker démarrent correctement.

[ ] Les endpoints répondent.

✅ Objectif

Cette mini-checklist garantit que le pipeline est fiable en local avant d’être poussé sur GitHub Actions.