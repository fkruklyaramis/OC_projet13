Documentation Technique OC-Lettings-Site
========================================

Bienvenue dans la documentation technique complète de **OC-Lettings-Site**.

Table des matières
==================

.. contents:: 
   :local:
   :depth: 2

1. Description du projet
========================

OC-Lettings-Site est une application web de gestion de locations immobilières développée avec Django dans le cadre du projet OpenClassrooms P13. Cette application permet la gestion complète des profils utilisateurs et des annonces de location immobilière avec un système de monitoring avancé.

**Vision du projet :**
Fournir une plateforme moderne et robuste pour la gestion immobilière avec déploiement automatisé et surveillance en temps réel.

**Objectifs techniques :**

* ✅ Refactorisation d'une application monolithique en architecture modulaire
* ✅ Mise en place d'un pipeline CI/CD complet
* ✅ Intégration de monitoring d'erreurs avec Sentry
* ✅ Déploiement cloud automatisé
* ✅ Documentation technique professionnelle

**Fonctionnalités métier :**

* **Gestion des locations** : Création, modification, consultation des biens immobiliers
* **Gestion des profils** : Profils utilisateurs avec villes favorites
* **Interface d'administration** : Interface Django Admin pour la gestion des données
* **Pages d'erreur personnalisées** : Gestion des erreurs 404 et 500
* **Système de logs** : Traçabilité complète des opérations

2. Instructions d'installation
==============================

Prérequis système
-----------------

**Environnement de développement :**

* Python 3.9+ (obligatoire)
* Git 2.0+ (obligatoire)
* Docker 20.0+ (optionnel, recommandé)
* Compte GitHub (pour CI/CD)

**Plateformes supportées :**

* macOS 10.15+
* Ubuntu 18.04+ / Debian 10+
* Windows 10+ avec WSL2

Installation en développement local
-----------------------------------

**Étape 1 : Clonage du repository**

.. code-block:: bash

   git clone https://github.com/fkruklyaramis/OC_projet13.git
   cd OC_projet13

**Étape 2 : Configuration de l'environnement Python**

.. code-block:: bash

   # Créer l'environnement virtuel
   python -m venv venv
   
   # Activer l'environnement
   source venv/bin/activate        # Linux/macOS
   venv\Scripts\activate          # Windows

**Étape 3 : Installation des dépendances**

.. code-block:: bash

   pip install --upgrade pip
   pip install -r requirements.txt

**Étape 4 : Configuration de l'application**

.. code-block:: bash

   # Copier le fichier de configuration
   cp .env.example .env
   
   # Éditer .env avec vos paramètres
   # SECRET_KEY=your-secret-key
   # DEBUG=True
   # SENTRY_DSN=your-sentry-dsn (optionnel)

**Étape 5 : Initialisation de la base de données**

.. code-block:: bash

   # Appliquer les migrations
   python manage.py migrate
   
   # Créer un superutilisateur
   python manage.py createsuperuser
   
   # Charger les données de démonstration
   python manage.py setup_production

**Étape 6 : Lancement du serveur**

.. code-block:: bash

   python manage.py runserver
   
   # Application accessible sur : http://localhost:8000
   # Interface admin : http://localhost:8000/admin

Installation avec Docker
-------------------------

**Option 1 : Image Docker Hub (recommandée)**

.. code-block:: bash

   # Pull et run direct
   docker run -p 8000:8000 --env-file .env francoiskrukly/oc-lettings-site:latest

**Option 2 : Build local**

.. code-block:: bash

   # Build de l'image
   docker build -t oc-lettings-site .
   
   # Run avec configuration
   docker run -p 8000:8000 --env-file .env oc-lettings-site

3. Guide de démarrage rapide
============================

**🚀 Démarrage en 3 minutes**

.. code-block:: bash

   # 1. Installation rapide
   git clone https://github.com/fkruklyaramis/OC_projet13.git
   cd OC_projet13
   python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   
   # 2. Configuration minimale
   python manage.py migrate
   python manage.py setup_production
   
   # 3. Lancement
   python manage.py runserver

**🎯 Vérification de l'installation**

* ✅ Page d'accueil : http://localhost:8000
* ✅ Lettings : http://localhost:8000/lettings/
* ✅ Profiles : http://localhost:8000/profiles/
* ✅ Admin : http://localhost:8000/admin (si superuser créé)

**🔍 Tests et qualité**

.. code-block:: bash

   # Lancer les tests
   python -m pytest --cov=. --cov-report=html
   
   # Vérifier le linting
   flake8 .
   
   # Voir la couverture
   open htmlcov/index.html

4. Technologies et langages de programmation
=============================================

Stack technique complète
-------------------------

**Backend - Framework et langage**

* **Python 3.9+** : Langage principal, syntaxe moderne
* **Django 3.0.2** : Framework web robuste et sécurisé
* **SQLite** : Base de données (développement)
* **PostgreSQL** : Base de données (production sur Render)

**Frontend - Interface utilisateur**

* **HTML5** : Structure sémantique des pages
* **CSS3** : Styles modernes avec Flexbox/Grid
* **Bootstrap 4** : Framework CSS responsive
* **JavaScript ES6+** : Interactions côté client

**DevOps - Déploiement et CI/CD**

* **Docker** : Conteneurisation multi-architecture
* **GitHub Actions** : Pipeline CI/CD automatisé
* **Render** : Plateforme de déploiement cloud
* **Git** : Contrôle de version distribué

**Monitoring et qualité**

* **Sentry** : Monitoring d'erreurs en temps réel  
* **pytest** : Framework de tests unitaires/intégration
* **coverage.py** : Mesure de couverture de code (88.83%)
* **flake8** : Linter Python (PEP8 compliance)

**Serveur et production**

* **Gunicorn** : Serveur WSGI hautes performances
* **WhiteNoise** : Serveur de fichiers statiques
* **SSL/TLS** : Chiffrement HTTPS automatique

5. Structure de la base de données et modèles de données
========================================================

Architecture de la base de données
-----------------------------------

**Diagramme Entity-Relationship**

::

   ┌─────────────────┐    1:1     ┌─────────────────┐
   │      User       │◄───────────┤     Profile     │
   │  (Django Auth)  │            │                 │
   └─────────────────┘            └─────────────────┘
                                  │ - favorite_city │
                                  └─────────────────┘
   
   ┌─────────────────┐    1:1     ┌─────────────────┐
   │     Address     │◄───────────┤     Letting     │
   │                 │            │                 │
   └─────────────────┘            └─────────────────┘
   │ - number        │            │ - title         │
   │ - street        │            └─────────────────┘
   │ - city          │
   │ - state         │
   │ - zip_code      │
   │ - country_iso   │
   └─────────────────┘

**Modèles de données détaillés**

*Modèle User (Django intégré)*

.. code-block:: python

   # Modèle Django standard avec :
   username        : CharField(150, unique=True)
   email           : EmailField(254)
   first_name      : CharField(150)
   last_name       : CharField(150)
   is_staff        : BooleanField()
   is_active       : BooleanField()
   date_joined     : DateTimeField()

*Modèle Profile (profiles/models.py)*

.. code-block:: python

   class Profile(models.Model):
       user            : OneToOneField(User, CASCADE)
       favorite_city   : CharField(64, blank=True)
       
       def __str__(self):
           return self.user.username

*Modèle Address (lettings/models.py)*

.. code-block:: python

   class Address(models.Model):
       number          : PositiveIntegerField()
       street          : CharField(64)
       city            : CharField(64)
       state           : CharField(2)
       zip_code        : PositiveIntegerField()
       country_iso_code: CharField(3)
       
       class Meta:
           verbose_name_plural = "Addresses"

*Modèle Letting (lettings/models.py)*

.. code-block:: python

   class Letting(models.Model):
       title   : CharField(256)
       address : OneToOneField(Address, CASCADE)
       
       def __str__(self):
           return self.title

**Relations et contraintes**

* **User ↔ Profile** : Relation OneToOne obligatoire
* **Address ↔ Letting** : Relation OneToOne obligatoire  
* **Signaux Django** : Logging automatique des opérations CRUD
* **Migrations** : Système de migration automatique pour évolution du schéma

**Exemples de données**

.. code-block:: sql

   -- Exemples d'adresses
   INSERT INTO Address VALUES (
       123, 'Main Street', 'New York', 'NY', 10001, 'USA'
   );
   
   -- Exemple de letting
   INSERT INTO Letting VALUES (
       'Cozy Downtown Apartment', <address_id>
   );
   
   -- Exemple de profil
   INSERT INTO Profile VALUES (
       <user_id>, 'Paris'
   );

6. Description des interfaces de programmation
==============================================

Architecture modulaire Django
------------------------------

**Applications Django**

L'application suit le pattern MVT (Model-View-Template) de Django avec une architecture modulaire :

*Application lettings/*

.. code-block:: python

   # lettings/models.py - Modèles de données
   class Address(models.Model): ...
   class Letting(models.Model): ...
   
   # lettings/views.py - Logique métier
   def index(request): ...          # Liste des lettings
   def letting(request, id): ...    # Détail d'un letting
   
   # lettings/urls.py - Configuration des routes
   urlpatterns = [
       path('', views.index, name='index'),
       path('<int:letting_id>/', views.letting, name='letting'),
   ]

*Application profiles/*

.. code-block:: python

   # profiles/models.py
   class Profile(models.Model): ...
   
   # profiles/views.py  
   def index(request): ...              # Liste des profils
   def profile(request, username): ...  # Détail d'un profil
   
   # profiles/urls.py
   urlpatterns = [
       path('', views.index, name='index'),
       path('<str:username>/', views.profile, name='profile'),
   ]

**API REST implicite**

Bien que l'application n'expose pas d'API REST explicite, elle suit les bonnes pratiques RESTful :

.. code-block:: python

   # URLs RESTful
   GET  /lettings/              # Liste des ressources
   GET  /lettings/<id>/         # Ressource spécifique
   GET  /profiles/              # Liste des profils  
   GET  /profiles/<username>/   # Profil spécifique

**Interfaces d'administration**

.. code-block:: python

   # Django Admin Interface
   GET  /admin/                 # Interface d'administration
   GET  /admin/lettings/        # Gestion des lettings
   GET  /admin/profiles/        # Gestion des profils
   POST /admin/lettings/add/    # Création de lettings

**Gestion d'erreurs standardisée**

.. code-block:: python

   # Handlers d'erreurs personnalisés (oc_lettings_site/views.py)
   def handler404(request, exception): ...  # Erreur 404 personnalisée
   def handler500(request): ...             # Erreur 500 personnalisée
   
   # Templates d'erreur
   templates/404.html                       # Page 404 personnalisée
   templates/500.html                       # Page 500 personnalisée

**Services transversaux**

.. code-block:: python

   # service/sentry_service.py - Monitoring
   def configure_sentry(): ...              # Configuration Sentry
   
   # Middleware Django
   - SecurityMiddleware                     # Sécurité HTTPS
   - WhiteNoiseMiddleware                   # Fichiers statiques
   - SessionMiddleware                      # Gestion des sessions
   - AuthenticationMiddleware               # Authentification

7. Guide d'utilisation
======================

Interface utilisateur
----------------------

**Page d'accueil (Homepage)**

* **URL** : `/`
* **Fonctionnalité** : Point d'entrée principal avec navigation
* **Éléments** : Logo, liens vers Lettings et Profiles

**Section Lettings**

* **URL** : `/lettings/`
* **Fonctionnalité** : Consultation des biens immobiliers
* **Actions utilisateur** :
  
  1. Voir la liste des lettings disponibles
  2. Cliquer sur un letting pour voir les détails
  3. Consulter l'adresse complète du bien

* **URL détail** : `/lettings/<id>/`
* **Informations affichées** :
  
  - Titre du bien
  - Adresse complète (numéro, rue, ville, état, code postal, pays)
  - Navigation retour vers la liste

**Section Profiles**

* **URL** : `/profiles/`
* **Fonctionnalité** : Consultation des profils utilisateurs  
* **Actions utilisateur** :
  
  1. Voir la liste des utilisateurs inscrits
  2. Cliquer sur un profil pour voir les détails
  3. Consulter la ville favorite de l'utilisateur

* **URL détail** : `/profiles/<username>/`
* **Informations affichées** :
  
  - Nom d'utilisateur
  - Email de contact
  - Ville favorite (si renseignée)

**Cas d'utilisation concrets**

*Cas 1 : Consultation d'un bien immobilier*

.. code-block:: none

   Utilisateur → Page d'accueil → Clic "Lettings" 
   → Liste des biens → Clic sur "Cozy Downtown Apartment"
   → Détail avec adresse "123 Main St, New York, NY 10001, USA"

*Cas 2 : Recherche d'information sur un utilisateur*

.. code-block:: none

   Utilisateur → Page d'accueil → Clic "Profiles"
   → Liste des profils → Clic sur "john_doe"  
   → Profil avec email et ville favorite "Paris"

*Cas 3 : Navigation administrative*

.. code-block:: none

   Admin → /admin → Login → Dashboard Django Admin
   → Lettings → Ajouter/Modifier/Supprimer des biens
   → Profiles → Gérer les profils utilisateurs

**Interface d'administration**

* **URL** : `/admin/`
* **Authentification** : Superutilisateur requis
* **Fonctionnalités** :
  
  - Gestion CRUD complète des Address, Letting, Profile
  - Interface Django Admin native
  - Filtres et recherche avancée
  - Export/Import de données

Guide d'utilisation
===================

Interface utilisateur
----------------------

**Page d'accueil :** http://localhost:8000

Liste des sections disponibles (Profiles, Lettings)

**Profiles :** http://localhost:8000/profiles/

Liste des profils utilisateurs avec liens de détail

**Lettings :** http://localhost:8000/lettings/

Liste des annonces de location avec détails d'adresse

Interface d'administration
--------------------------

**Accès :** http://localhost:8000/admin/

**Compte par défaut :**

* Username: admin
* Password: admin

**Fonctionnalités :**

* Gestion complète des modèles
* Interface CRUD intuitive
* Filtres et recherche
* Actions en lot

Déploiement
===========

Architecture de déploiement
----------------------------

**Environnements :**

* **Développement :** Local avec SQLite
* **Production :** Render avec PostgreSQL

**Pipeline CI/CD :**

1. Push sur GitHub
2. Tests automatiques (GitHub Actions)
3. Build Docker
4. Déploiement Render automatique

Configuration Docker
--------------------

**Variables d'environnement production :**

.. code-block:: bash

   DEBUG=False
   SECRET_KEY=<clé-secrète>
   DATABASE_URL=<url-postgresql>
   SENTRY_DSN=<dsn-sentry>

GitHub Actions
--------------

**Workflow automatisé :**

1. **Tests :** pytest, flake8, coverage
2. **Build :** Construction image Docker
3. **Deploy :** Push sur Render (branche main)

**Déclencheurs :**

* Push sur toute branche (tests)
* Push sur main (tests + déploiement)

Render
------

**Configuration :**

* Service Web Docker
* Auto-deploy depuis GitHub
* Variables d'environnement sécurisées
* SSL automatique
* Logs centralisés

8. Procédures de déploiement et gestion de l'application
=========================================================

Pipeline CI/CD complet
-----------------------

**Architecture de déploiement automatisé**

::

   Développeur → Git Push → GitHub → GitHub Actions → Docker Hub → Render
        ↓           ↓          ↓            ↓            ↓         ↓
   Code local → Repository → Triggers → Build/Test → Registry → Production

**Workflow détaillé (.github/workflows/deploy.yml)**

*Étape 1 : Tests et validation*

.. code-block:: yaml

   # Déclenchement automatique
   on:
     push:
       branches: [ "main", "develop" ]
     pull_request:
       branches: [ "main" ]

   # Job de tests
   test:
     - Linting flake8 (PEP8 compliance)
     - Tests pytest (32 tests, 88.83% coverage)
     - Vérification configuration Django
     - Collecte fichiers statiques

*Étape 2 : Build Docker multi-architecture*

.. code-block:: yaml

   build:
     - Build image Docker (linux/amd64, linux/arm64)
     - Push vers Docker Hub
     - Tag automatique avec SHA Git
     - Optimisation des layers

*Étape 3 : Déploiement production*

.. code-block:: yaml

   deploy:
     - Déclenchement auto sur branche main
     - Déploiement Render via webhook
     - Variables d'environnement sécurisées
     - Vérification santé application

Déploiement en développement
----------------------------

**Déploiement local rapide**

.. code-block:: bash

   # 1. Tests en local
   python -m pytest --cov=.
   flake8 .
   
   # 2. Build Docker local
   docker build -t oc-lettings-site-dev .
   
   # 3. Test conteneur
   docker run -p 8000:8000 --env-file .env oc-lettings-site-dev

**Environnement de staging**

.. code-block:: bash

   # Branche develop → auto-deploy staging
   git checkout develop
   git push origin develop
   # → Tests auto + Deploy staging

Déploiement en production
-------------------------

**Processus de mise en production**

.. code-block:: bash

   # 1. Merge vers main (via Pull Request)
   git checkout main
   git merge develop
   git push origin main
   
   # 2. Déclenchement automatique :
   #    - Tests complets (pytest, flake8, security)
   #    - Build Docker multi-arch
   #    - Push Docker Hub
   #    - Deploy Render production

**Configuration des variables d'environnement**

*Développement (.env)*

.. code-block:: bash

   DEBUG=True
   SECRET_KEY=dev-key-not-for-production
   ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
   SENTRY_DSN=https://your-dev-dsn@sentry.io/project

*Production (Render Dashboard)*

.. code-block:: bash

   DEBUG=False
   SECRET_KEY=<clé-production-sécurisée-32-chars>
   ALLOWED_HOSTS=your-app.onrender.com,your-domain.com
   DATABASE_URL=postgresql://user:pass@host:port/db
   SENTRY_DSN=https://your-prod-dsn@sentry.io/project
   SENTRY_ENVIRONMENT=production

Gestion des déploiements
-------------------------

**Rollback en cas de problème**

.. code-block:: bash

   # 1. Via Render Dashboard
   #    → Deploy History → Previous Version → Redeploy
   
   # 2. Via Git (rollback code)
   git revert <commit-hash>
   git push origin main
   # → Auto-redeploy vers version stable

**Monitoring post-déploiement**

.. code-block:: bash

   # Vérifications automatiques
   1. Health check Render (30s après deploy)
   2. Tests de fumée (pages principales)
   3. Monitoring Sentry (erreurs temps réel)
   4. Logs applicatifs centralisés

**Procédures de maintenance**

*Mise à jour des dépendances*

.. code-block:: bash

   # 1. Local
   pip-review --local --auto
   pip freeze > requirements.txt
   
   # 2. Test
   python -m pytest --cov=.
   
   # 3. Deploy
   git commit -m "Update dependencies"
   git push origin main

*Migrations de base de données*

.. code-block:: bash

   # Auto-gérées par Django/Render
   python manage.py makemigrations
   python manage.py migrate  # Auto-exécuté au deploy

Surveillance et monitoring
==========================

**Sentry - Monitoring d'erreurs**

.. code-block:: python

   # Configuration production
   SENTRY_DSN = os.getenv('SENTRY_DSN')
   SENTRY_ENVIRONMENT = os.getenv('SENTRY_ENVIRONMENT', 'production')
   SENTRY_TRACES_SAMPLE_RATE = 0.05
   
   # Capture automatique :
   - Exceptions non gérées
   - Erreurs 404/500 personnalisées  
   - Performance monitoring
   - Alertes temps réel

**Logs applicatifs**

.. code-block:: python

   # logs/oc_lettings.log
   INFO  - Page d'accueil visitée par 192.168.1.1
   INFO  - Nouveau letting créé: Modern Loft Downtown
   INFO  - Profil mis à jour: john_doe
   ERROR - Letting introuvable: ID 999

**Métriques de santé**

- **Uptime** : >99.9% (Render monitoring)
- **Temps de réponse** : <200ms moyenne
- **Couverture tests** : 88.83% maintenue
- **Sécurité** : SSL/TLS automatique, HTTPS forcé

**Alertes et notifications**

.. code-block:: yaml

   # Configuration alertes
   Sentry:
     - Erreur critique → Email immédiat
     - Pic d'erreurs → Slack notification
   
   Render:
     - Deploy failed → Email + Dashboard
     - Service down → SMS + Email
   
   GitHub Actions:
     - Build failed → Email + PR status

===================================
Conclusion
===================================

Cette documentation couvre tous les aspects techniques de l'application OC-Lettings-Site, depuis l'installation jusqu'au déploiement en production. L'architecture modulaire Django, le pipeline CI/CD automatisé et le monitoring Sentry garantissent une application robuste et maintenable.

**Contacts et ressources**

* **Repository** : https://github.com/fkruklyaramis/OC_projet13
* **Documentation** : https://oc-lettings-site.readthedocs.io/
* **Issues** : GitHub Issues pour le support technique

