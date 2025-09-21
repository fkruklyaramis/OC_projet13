Documentation OC-Lettings-Site
================================

Bienvenue dans la documentation de **OC-Lettings-Site**, une application Django 3.0 pour la gestion de locations immobilières.

Description du projet
======================

OC-Lettings-Site est une application web moderne développée dans le cadre du projet OpenClassrooms P13. Elle permet de gérer des profils utilisateurs et des annonces de location immobilière.

**Fonctionnalités principales :**

* Gestion des profils utilisateurs
* Gestion des adresses et locations
* Interface d'administration Django
* API REST pour l'accès aux données
* Système de logging automatique
* Déploiement automatisé avec CI/CD

Technologies utilisées
======================

**Backend :**

* Django 3.0.2
* Python 3.9+
* SQLite (développement) / PostgreSQL (production)
* Gunicorn (serveur WSGI)
* WhiteNoise (fichiers statiques)

**Frontend :**

* HTML5/CSS3
* Bootstrap 4
* JavaScript vanilla

**DevOps :**

* Docker et Docker Compose
* GitHub Actions (CI/CD)
* Render (déploiement)
* Sentry (monitoring d'erreurs)

Installation et démarrage
=========================

Prérequis
---------

* Python 3.9+
* Git
* Docker (optionnel)

Installation locale
-------------------

1. **Cloner le repository :**

.. code-block:: bash

   git clone https://github.com/fkruklyaramis/OC_projet13.git
   cd OC_projet13

2. **Créer un environnement virtuel :**

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate  # Linux/macOS

3. **Installer les dépendances :**

.. code-block:: bash

   pip install -r requirements.txt

4. **Appliquer les migrations :**

.. code-block:: bash

   python manage.py migrate

5. **Créer des données de démonstration :**

.. code-block:: bash

   python manage.py setup_production

6. **Lancer le serveur :**

.. code-block:: bash

   python manage.py runserver

L'application est accessible sur http://localhost:8000

Installation Docker
-------------------

.. code-block:: bash

   docker build -t oc-lettings-site .
   docker run -p 8000:8000 oc-lettings-site

Architecture de l'application
=============================

Structure du projet
--------------------

::

   oc_lettings_site/
   ├── lettings/           # Application lettings
   │   ├── models.py       # Modèles Address et Letting
   │   ├── views.py        # Vues de l'application
   │   └── urls.py         # URLs lettings
   ├── profiles/           # Application profiles
   │   ├── models.py       # Modèle Profile
   │   ├── views.py        # Vues profiles
   │   └── urls.py         # URLs profiles
   ├── oc_lettings_site/   # Configuration principale
   │   ├── settings.py     # Configuration Django
   │   ├── urls.py         # URLs principales
   │   └── wsgi.py         # Configuration WSGI
   ├── service/            # Services transversaux
   │   └── sentry_service.py # Configuration Sentry
   ├── templates/          # Templates HTML
   ├── static/            # Fichiers statiques
   └── manage.py          # Point d'entrée Django

Base de données
---------------

**Modèle de données :**

* **User** (Django) : Utilisateurs système
* **Profile** : Profils utilisateurs étendus
* **Address** : Adresses géographiques
* **Letting** : Annonces de location (liées 1:1 aux adresses)

**Relations :**

* User 1:1 Profile
* Address 1:1 Letting

**Signaux Django :**

Logging automatique des opérations CRUD sur tous les modèles.

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
* Password: Abc1234!

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

Surveillance et monitoring
==========================

Sentry
------

**Configuration :**

* Capture automatique des erreurs
* Monitoring des performances
* Alertes en temps réel

Logs applicatifs
----------------

**Configuration :** logs/oc_lettings.log

**Événements loggés :**

* Opérations CRUD sur les modèles
* Erreurs d'application
* Actions d'administration

