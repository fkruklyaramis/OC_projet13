## Résumé

Site web d'Orange County Lettings

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
- `git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git`

#### Créer l'environnement virtuel

- `cd /path/to/Python-OC-Lettings-FR`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(Python-OC-Lettings-FR_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  Python-OC-Lettings-FR_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`


## Surveillance et Logging avec Sentry

### Configuration de Sentry

L'application intègre **Sentry** pour la surveillance des erreurs et le logging avancé.

#### 1. Prérequis Sentry

1. **Créer un compte Sentry** : https://sentry.io/
2. **Créer un nouveau projet Django** dans votre organisation
3. **Récupérer la DSN** (Data Source Name) de votre projet

#### 2. Configuration des variables d'environnement

Copiez le fichier `.env.example` vers `.env` :

```bash
cp .env.example .env
```

Modifiez le fichier `.env` avec vos valeurs :

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

#### 4. Configuration des logs

L'application utilise plusieurs loggers :
- `oc_lettings_site` : Logs de l'application principale
- `lettings` : Logs de l'application lettings
- `profiles` : Logs de l'application profiles
- `django` : Logs du framework Django

Les logs sont envoyés vers :
- **Console** : Tous les niveaux (DEBUG et plus)
- **Fichier** : `logs/oc_lettings.log` (INFO et plus)
- **Sentry** : Erreurs uniquement (ERROR et CRITICAL)

#### 5. Test de la configuration Sentry

Une fois l'application démarrée, vous pouvez tester Sentry :

```bash
# Test sans erreur
curl "http://localhost:8000/sentry-debug/?type=test"

# Test division par zéro
curl "http://localhost:8000/sentry-debug/?type=division"

# Test clé manquante
curl "http://localhost:8000/sentry-debug/?type=key"

# Test index hors limites
curl "http://localhost:8000/sentry-debug/?type=index"

# Test erreur personnalisée
curl "http://localhost:8000/sentry-debug/?type=custom"
```

#### 6. Points de logging dans l'application

**Vues** :
- Logs d'accès avec adresses IP
- Gestion des erreurs 404
- Exceptions capturées

**Modèles** :
- Création/modification/suppression d'objets via signaux Django
- Opérations critiques sur les données

**Niveaux de log utilisés** :
- `INFO` : Accès aux pages, opérations normales
- `WARNING` : Erreurs 404, suppressions d'objets
- `ERROR` : Erreurs d'application, exceptions

#### 7. Déploiement en production

Pour la production, modifiez les variables d'environnement :

```bash
SENTRY_ENVIRONMENT=production
SENTRY_LOG_LEVEL=WARNING
SENTRY_TRACES_SAMPLE_RATE=0.05
```

**Important** : Ne jamais committer le fichier `.env` contenant vos vraies clés Sentry !

### Vérification des logs

Les logs sont disponibles dans :
- **Console** : Pendant le développement
- **Fichier** : `logs/oc_lettings.log`
- **Sentry Dashboard** : Pour les erreurs et événements

### Dépannage

1. **Sentry ne capture pas d'erreurs** :
   - Vérifiez que `SENTRY_DSN` est correctement configuré
   - Vérifiez le niveau `SENTRY_EVENT_LEVEL`

2. **Logs manquants** :
   - Vérifiez les permissions du dossier `logs/`
   - Vérifiez la configuration `SENTRY_LOG_LEVEL`

3. **Performance** :
   - Réduisez `SENTRY_TRACES_SAMPLE_RATE` si trop de traces
   - Ajustez les niveaux de log selon l'environnement
