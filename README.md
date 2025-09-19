# Orange County Lettings

## Description

Site web d'Orange County Lettings - Application Django refactorisée avec surveillance des erreurs et architecture modulaire.

## Fonctionnalités

- **Architecture modulaire** : Applications Django séparées (lettings, profiles)
- **Surveillance des erreurs** : Intégration Sentry complète avec logging avancé
- **Gestion des profils** : Système de profils utilisateurs avec favoris
- **Gestion des locations** : Système de gestion des biens immobiliers
- **Interface d'administration** : Panel d'administration Django complet
- **Logging complet** : Système de logs multi-niveaux (console, fichier, Sentry)

## Architecture du projet

```
oc-lettings-site/
├── lettings/              # Application gestion des locations
├── profiles/              # Application gestion des profils
├── oc_lettings_site/      # Configuration principale Django
├── service/               # Services externes (Sentry, etc.)
├── templates/             # Templates HTML globaux
├── static/                # Fichiers statiques (CSS, JS, images)
├── logs/                  # Fichiers de logs
└── requirements.txt       # Dépendances Python
```

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/fkruklyaramis/OC_projet13.git`

#### Créer l'environnement virtuel

- `cd /path/to/OC_projet13`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Configuration des variables d'environnement (optionnel)

Pour activer Sentry (surveillance des erreurs), créez un fichier `.env` :

```bash
# Configuration Sentry (optionnel)
SENTRY_DSN=https://your-dsn@sentry.io/your-project-id
SENTRY_ENVIRONMENT=development
SENTRY_LOG_LEVEL=INFO
SENTRY_EVENT_LEVEL=ERROR
SENTRY_TRACES_SAMPLE_RATE=0.1
SENTRY_RELEASE=1.0.0
```

#### Exécuter le site

- `cd /path/to/OC_projet13`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/OC_projet13`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/OC_projet13`
- `source venv/bin/activate`
- `pytest`

#### Coverage des tests

Pour mesurer la couverture de code des tests :

```bash
# Exécuter les tests avec coverage
coverage run -m pytest

# Afficher le rapport de couverture dans le terminal
coverage report

# Générer un rapport HTML détaillé
coverage html

# Ouvrir le rapport HTML (optionnel)
open htmlcov/index.html
```

**Commandes utiles pour coverage :**
- `coverage erase` : Effacer les données de couverture précédentes
- `coverage report --show-missing` : Afficher les lignes non couvertes
- `coverage report --skip-covered` : Ne montrer que les fichiers avec couverture incomplète

#### Base de données

- `cd /path/to/OC_projet13`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(profiles_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from profiles_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`

## Architecture technique

### Applications Django

#### 1. Application `lettings`
- **Modèle** : `Letting` (gestion des biens immobiliers)
- **Vues** : Liste des locations et détail d'une location
- **URLs** : `/lettings/` et `/lettings/<id>/`
- **Templates** : `lettings/index.html` et `lettings/letting.html`

#### 2. Application `profiles`
- **Modèle** : `Profile` (profils utilisateurs avec villes favorites)
- **Vues** : Liste des profils et détail d'un profil
- **URLs** : `/profiles/` et `/profiles/<username>/`
- **Templates** : `profiles/index.html` et `profiles/profile.html`

#### 3. Configuration principale `oc_lettings_site`
- **Settings** : Configuration Django avec intégration Sentry
- **URLs principales** : Routage global et page d'accueil
- **Vues** : Page d'accueil du site

### Service Layer

#### Module `service/sentry_service.py`
- Configuration centralisée de Sentry
- Gestion des variables d'environnement
- Intégration Django et logging
- Support pour multiple environnements (dev/staging/prod)

## Surveillance et Logging avec Sentry

### Configuration de Sentry

L'application intègre **Sentry** pour la surveillance des erreurs et le logging avancé avec une architecture de service modulaire.

#### 1. Prérequis Sentry

1. **Créer un compte Sentry** : https://sentry.io/
2. **Créer un nouveau projet Django** dans votre organisation
3. **Récupérer la DSN** (Data Source Name) de votre projet

#### 2. Configuration des variables d'environnement

Créez un fichier `.env` à la racine du projet :

```bash
# Configuration Sentry
SENTRY_DSN=https://your-actual-dsn@sentry.io/your-project-id
SENTRY_LOG_LEVEL=INFO
SENTRY_EVENT_LEVEL=ERROR
SENTRY_TRACES_SAMPLE_RATE=0.1
SENTRY_ENVIRONMENT=development
SENTRY_RELEASE=1.0.0
```

#### 3. Variables d'environnement disponibles

| Variable | Description | Valeurs possibles | Défaut |
|----------|-------------|-------------------|--------|
| `SENTRY_DSN` | URL de connexion Sentry | URL complète Sentry | - |
| `SENTRY_LOG_LEVEL` | Niveau minimum de log | DEBUG, INFO, WARNING, ERROR, CRITICAL | INFO |
| `SENTRY_EVENT_LEVEL` | Niveau pour créer des événements Sentry | WARNING, ERROR, CRITICAL | ERROR |
| `SENTRY_TRACES_SAMPLE_RATE` | Taux d'échantillonnage des traces | 0.0 à 1.0 | 0.1 |
| `SENTRY_ENVIRONMENT` | Environnement de déploiement | development, staging, production | development |
| `SENTRY_RELEASE` | Version de l'application | Numéro de version | unknown |

#### 4. Architecture de logging

L'application utilise une architecture de logging sophistiquée :

**Loggers disponibles :**
- `oc_lettings_site` : Logs de l'application principale
- `lettings` : Logs de l'application lettings  
- `profiles` : Logs de l'application profiles
- `django` : Logs du framework Django

**Handlers de logging :**
- **Console** : Affichage en temps réel (DEBUG et plus)
- **Fichier** : `logs/oc_lettings.log` (INFO et plus)
- **Sentry** : Erreurs uniquement (ERROR et CRITICAL)

**Points de logging automatiques :**
- Accès aux pages avec adresses IP
- Opérations sur les modèles (création/modification/suppression)
- Gestion des erreurs 404 et exceptions
- Requêtes de base de données

#### 5. Fonctionnalités de surveillance

**Surveillance automatique :**
- Capture des exceptions non gérées
- Monitoring des performances avec échantillonnage configurable
- Tracking des requêtes Django avec middleware intégré
- Envoi automatique des erreurs critiques vers Sentry

**Logging intelligent :**
- Logs contextuels avec adresses IP et métadonnées utilisateur  
- Signaux Django pour les opérations de base de données
- Gestion différenciée des niveaux selon l'environnement
- Rotation automatique des fichiers de logs

#### 6. Configuration pour la production

Pour la production, ajustez les variables d'environnement :

```bash
SENTRY_ENVIRONMENT=production
SENTRY_LOG_LEVEL=WARNING
SENTRY_EVENT_LEVEL=ERROR
SENTRY_TRACES_SAMPLE_RATE=0.05
```

**Recommandations production :**
- Réduire le taux d'échantillonnage des traces
- Augmenter le niveau minimum des logs
- Configurer la rotation des fichiers de logs
- Utiliser des variables d'environnement sécurisées

### Consultation des logs

**Sources de logs disponibles :**
- **Console de développement** : Logs en temps réel pendant le développement
- **Fichier local** : `logs/oc_lettings.log` pour analyse historique
- **Dashboard Sentry** : https://sentry.io pour erreurs et monitoring

### Architecture du service Sentry

**Fichier `service/sentry_service.py` :**
```python
def configure_sentry():
    """Configuration centralisée de Sentry avec variables d'environnement"""
    # Configuration automatique selon l'environnement
    # Intégration Django native
    # Support logging avancé
```

**Intégration dans `settings.py` :**
```python
from service.sentry_service import configure_sentry
configure_sentry()  # Activation automatique si DSN configurée
```

## Débogage et maintenance

### Diagnostic des problèmes

1. **Sentry ne capture pas d'erreurs** :
   - Vérifiez la variable `SENTRY_DSN`
   - Contrôlez le niveau `SENTRY_EVENT_LEVEL`
   - Consultez les logs console pour les messages de configuration

2. **Logs manquants** :
   - Vérifiez les permissions du dossier `logs/`
   - Contrôlez la configuration `SENTRY_LOG_LEVEL`
   - Vérifiez l'espace disque disponible

3. **Performance** :
   - Réduisez `SENTRY_TRACES_SAMPLE_RATE` si surcharge
   - Ajustez les niveaux de log selon l'environnement
   - Surveillez la taille des fichiers de logs

### Commandes utiles

```bash
# Vérifier la configuration Sentry
python manage.py shell -c "from service.sentry_service import configure_sentry; configure_sentry()"

# Analyser les logs
tail -f logs/oc_lettings.log

# Tests de l'application
python manage.py test
pytest

# Tests avec couverture de code
coverage run -m pytest
coverage report
coverage html

# Vérification du code
flake8
```

## Technologies utilisées

- **Django 3.0+** : Framework web Python
- **Python 3.9+** : Langage de programmation
- **Sentry SDK 1.32+** : Surveillance des erreurs et performance
- **SQLite3** : Base de données (développement)
- **HTML/CSS/JavaScript** : Frontend
- **Pytest** : Tests unitaires
- **Coverage.py** : Mesure de la couverture de code
- **Flake8** : Linting et qualité de code

## Contribuer

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## License

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour les détails.
