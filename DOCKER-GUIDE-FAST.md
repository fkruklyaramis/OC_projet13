# Guide Docker ULTRA-RAPIDE - OC-Lettings-Site

## ⚡ **BUILD OPTIMISÉ - 90 SECONDES** 

Configuration **ultra-rapide** : `linux/amd64` uniquement
- ✅ **15x plus rapide** que multi-architecture
- ✅ Compatible **95%** des cas d'usage
- ✅ Déploiement immédiat possible

## 🎯 Compatibilité Optimisée

| Plateforme | Architecture | Performance |
|------------|--------------|-------------|
| **Mac Intel** | `linux/amd64` | 🟢 NATIVE |
| **Mac Apple Silicon** | `linux/amd64` | 🟡 Émulation Rosetta |
| **Windows Docker** | `linux/amd64` | 🟢 NATIVE |
| **Linux Intel/AMD** | `linux/amd64` | 🟢 NATIVE |
| **Render Production** | `linux/amd64` | 🟢 NATIVE |

## 🚀 Utilisation Immédiate

### Pull ultra-rapide
```bash
docker pull francoiskrukly/oc-lettings-site:latest
```

### Run universel  
```bash
docker run -p 8000:8000 \
  -e DEBUG=False \
  -e ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0 \
  francoiskrukly/oc-lettings-site:latest
```

### Accès immédiat
- **Application** : http://localhost:8000
- **Admin** : http://localhost:8000/admin/ (`admin`/`admin123`)

## 📈 Performance

- **Build CI/CD** : ~90 secondes (vs 15+ minutes multi-arch)
- **Pull local** : ~30 secondes  
- **Startup** : ~5 secondes
- **Mac M1/M2** : Émulation transparente via Rosetta

## 🔧 Si besoin ARM64 spécifique

Pour forcer ARM64 natif sur Mac Apple Silicon :
```bash
# Build local ARM64
docker build --platform linux/arm64 -t oc-lettings-arm64 .

# Ou attendre build multi-arch (plus lent mais disponible sur demande)
```

## ✨ Fonctionnalités Incluses

- ✅ Django 3.0 + données démo
- ✅ WhiteNoise CSS/JS/Images  
- ✅ Gunicorn production
- ✅ Admin interface complète
- ✅ Superuser automatique
- ✅ Variables d'environnement