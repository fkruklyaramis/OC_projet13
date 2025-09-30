# Guide de Configuration Sentry - OC-Lettings-Site

## 🚀 Configuration Rapide Sentry

### Étape 1 : Créer un compte Sentry

1. Allez sur https://sentry.io
2. Créez un compte gratuit
3. Créez un nouveau projet Django

### Étape 2 : Récupérer votre DSN

Dans votre projet Sentry :
1. Allez dans **Settings** > **Client Keys (DSN)**
2. Copiez votre DSN (ressemble à : `https://xxx@sentry.io/xxx`)

### Étape 3 : Configuration locale

Créez un fichier `.env` à la racine du projet :

```bash
# Configuration Sentry
SENTRY_DSN=https://votre-dsn-ici@sentry.io/votre-projet-id
SENTRY_ENVIRONMENT=development
SENTRY_LOG_LEVEL=INFO
SENTRY_EVENT_LEVEL=WARNING
SENTRY_TRACES_SAMPLE_RATE=1.0
SENTRY_RELEASE=1.0.0

# Configuration Django
DEBUG=True
SECRET_KEY=dev-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

### Étape 4 : Test de la configuration

```bash
# 1. Démarrer le serveur
python manage.py runserver

# 2. Aller sur la vue de test Sentry
open http://localhost:8000/test-sentry/

# 3. Tester une vraie 404
curl http://localhost:8000/page-inexistante/

# 4. Vérifier Sentry dans quelques minutes
```

## 🔍 Vérifications

### URLs de test disponibles :
- **http://localhost:8000/test-sentry/** - Test manuel complet
- **http://localhost:8000/test-404/** - Test erreur 404  
- **http://localhost:8000/test-500/** - Test erreur 500

### Configuration recommandée pour capturer les 404 :
```bash
SENTRY_EVENT_LEVEL=WARNING  # Important pour capturer les 404
```

### Types d'événements capturés :
- ✅ **404 (WARNING)** : Pages non trouvées
- ✅ **500 (ERROR)** : Erreurs serveur
- ✅ **Exceptions** : Erreurs Python non gérées
- ✅ **Logs** : Messages de logging selon le niveau configuré

## 📊 Dashboard Sentry

Une fois configuré, vous verrez dans Sentry :
1. **Issues** : Toutes les erreurs groupées
2. **Performance** : Métriques de performance (si activé)
3. **Releases** : Versions de votre application

## 🔧 Production

Pour la production sur Render :
1. Ajoutez `SENTRY_DSN` dans les variables d'environnement Render
2. Configurez `SENTRY_ENVIRONMENT=production`
3. Réduisez `SENTRY_TRACES_SAMPLE_RATE=0.1` pour économiser les quotas

---

**⚠️ Important :** Sans DSN configurée, Sentry ne peut pas envoyer d'événements !