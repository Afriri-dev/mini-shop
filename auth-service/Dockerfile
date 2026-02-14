# Image de base Python
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY src/ ./src
COPY tests/ ./tests

# Exposer le port
EXPOSE 5000

# Commande de démarrage
CMD ["python", "src/app.py"]