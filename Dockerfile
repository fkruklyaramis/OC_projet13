# oc_lettings_site/Dockerfile - Image Docker multi-architecture pour OC-Lettings-Site
# FROM python:3.9-slim utilise l'image officielle Python sur Debian Bullseye (pas Alpine)
# "slim" = version allégée sans outils dev (gcc, make) mais avec glibc pour compatibilité
# Taille ~45MB vs ~120MB pour python:3.9 standard, compatible linux/amd64 + linux/arm64
FROM python:3.9-slim

# PYTHONDONTWRITEBYTECODE=1 désactive la création des fichiers .pyc (bytecode Python)
# Économise de l'espace disque et évite les problèmes de permissions dans les conteneurs
# PYTHONUNBUFFERED=1 force la sortie Python en temps réel (pas de buffer)
# Essentiel pour voir les logs Django instantanément dans docker logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# WORKDIR /app crée le dossier /app et définit comme répertoire de travail
# Tous les COPY, RUN, CMD suivants s'exécuteront depuis /app
# Équivaut à : mkdir -p /app && cd /app
WORKDIR /app

# COPY requirements.txt . copie seulement le fichier requirements.txt vers /app/
# Stratégie "layer caching" : si requirements.txt n'a pas changé, Docker réutilise le layer
# Évite de refaire pip install à chaque build si seul le code applicatif change
COPY requirements.txt .

# --no-cache-dir évite de stocker le cache pip dans l'image (économise ~100MB)
# --upgrade pip met à jour pip vers la dernière version pour éviter les warnings
# Se fait en 2 RUN séparés pour optimiser les layers Docker (rebuild plus rapide)
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# COPY . . copie TOUT le code source du repo vers /app/ (sauf .dockerignore)
# Inclut : oc_lettings_site/, lettings/, profiles/, manage.py, templates/, static/
# Fait APRÈS pip install pour optimiser le cache Docker (code change plus souvent que requirements)
COPY . .

# mkdir -p crée les dossiers avec parents si nécessaires (-p = no error if exists)
# static/ = fichiers CSS/JS/images du développement
# staticfiles/ = dossier où Django collecte TOUS les fichiers statiques (app + admin)
# logs/ = stockage des logs applicatifs (oc_lettings.log)
RUN mkdir -p static staticfiles logs

# python manage.py migrate applique toutes les migrations Django sur la DB SQLite
# --noinput évite les questions interactives (mode automatique)
# Crée les tables lettings_address, lettings_letting, profiles_profile, auth_user, etc.
# ATTENTION : en production réelle, les migrations se font généralement au démarrage, pas au build
RUN python manage.py migrate --noinput

# setup_production est une commande Django custom (oc_lettings_site/management/commands/)
# Crée automatiquement : 1 superuser admin, 4 utilisateurs, 4 profils, 4 adresses, 4 lettings
# Permet d'avoir des données de démonstration immédiatement après déploiement
# Idempotente : ne recrée pas les données si elles existent déjà
RUN python manage.py setup_production

# collectstatic rassemble tous les fichiers statiques dans staticfiles/
# Combine : static/ de l'app + static/ de Django admin + static/ des packages tiers
# --noinput mode automatique, écrase les fichiers existants sans demander
# Résultat : staticfiles/ contient tout pour servir les CSS/JS/images en production
RUN python manage.py collectstatic --noinput

# SÉCURITÉ : Création d'un utilisateur non-root pour éviter les failles de sécurité
# adduser --disabled-password crée utilisateur sans mot de passe (connexion SSH impossible)
# --gecos '' évite les questions interactives sur nom complet, téléphone, etc.
# Par defaut, Docker exécute en root (UID 0) = dangereux si container compromis
RUN adduser --disabled-password --gecos '' appuser

# chown -R change récursivement le propriétaire de /app/ vers appuser:appuser
# Nécessaire car tous les fichiers copiés appartiennent à root par défaut
# appuser aura maintenant les permissions lecture/écriture sur logs/, static/, etc.
RUN chown -R appuser:appuser /app

# USER appuser bascule vers l'utilisateur non-root pour toutes les commandes suivantes
# Gunicorn s'exécutera avec UID > 0, limitant les dégâts en cas de faille
USER appuser

# EXPOSE 8000 documente que le conteneur écoute sur le port 8000
# N'ouvre PAS le port (il faut docker run -p 8000:8000)
# Juste une indication pour les développeurs et outils d'orchestration
EXPOSE 8000

# CMD définit la commande par défaut exécutée au démarrage du conteneur
# gunicorn = serveur WSGI Python haute performance (production-ready)
# --bind 0.0.0.0:8000 écoute sur toutes les interfaces (pas seulement localhost)
# --workers 3 lance 3 processus worker pour gérer les requêtes en parallèle
# oc_lettings_site.wsgi:application pointe vers l'objet WSGI Django
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "oc_lettings_site.wsgi:application"]