# oc_lettings_site/Dockerfile
# Utilise l'image officielle Python 3.9 basée sur Alpine Linux (légère)
FROM python:3.9-slim

# Variables d'environnement pour Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de requirements et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source de l'application
COPY . .

# Créer les répertoires nécessaires
RUN mkdir -p static staticfiles logs

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# Créer un utilisateur non-root pour la sécurité
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Exposer le port de l'application
EXPOSE 8000

# Commande par défaut pour lancer l'application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "oc_lettings_site.wsgi:application"]