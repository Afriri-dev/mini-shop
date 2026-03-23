FROM nginx:alpine

# Supprimer la config par défaut
RUN rm /etc/nginx/conf.d/default.conf

# Copier ta config personnalisée
COPY nginx.conf /etc/nginx/conf.d

# Copier les fichiers frontend (HTML, CSS, JS)
COPY . /usr/share/nginx/html

EXPOSE 80