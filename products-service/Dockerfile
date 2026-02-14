# Utiliser une image Node.js légère
FROM node:18-alpine

# Créer le dossier de travail
WORKDIR /app

# Copier les fichiers de configuration
COPY package.json package-lock.json ./

# Installer uniquement les dépendances de production
RUN npm install --production

# Copier le code source
COPY . .

# Exposer le port
EXPOSE 3000

# Lancer l’application
CMD ["npm", "start"]