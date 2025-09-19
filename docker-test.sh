#!/bin/bash

# Script pour construire et tester l'image Docker localement

set -e  # Arrêter le script en cas d'erreur

echo "🐳 Construction de l'image Docker..."
docker build -t oc-lettings-site:local .

echo "🚀 Démarrage du conteneur..."
docker run -d \
    -p 8001:8000 \
    -e DEBUG=False \
    -e ALLOWED_HOSTS=localhost,127.0.0.1 \
    --name oc-lettings-local \
    oc-lettings-site:local

echo "⏳ Attente du démarrage..."
sleep 3

echo "🧪 Test de l'application..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8001)

if [ "$HTTP_CODE" -eq 200 ]; then
    echo "✅ Application accessible sur http://localhost:8001 (Code: $HTTP_CODE)"
    
    # Test de l'interface d'administration
    ADMIN_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/admin/)
    echo "✅ Interface admin accessible (Code: $ADMIN_CODE)"
    
    echo ""
    echo "🎉 Tests réussis ! L'application fonctionne correctement."
    echo "📝 Pour voir les logs : docker logs oc-lettings-local"
    echo "🛑 Pour arrêter : docker stop oc-lettings-local && docker rm oc-lettings-local"
else
    echo "❌ Erreur : Application non accessible (Code: $HTTP_CODE)"
    echo "📝 Logs du conteneur :"
    docker logs oc-lettings-local
    
    # Nettoyage en cas d'erreur
    docker stop oc-lettings-local && docker rm oc-lettings-local
    exit 1
fi