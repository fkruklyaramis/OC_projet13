#!/bin/bash

# test-pipeline.sh - Script pour tester le pipeline CI/CD en local
# Usage: ./test-pipeline.sh

echo "Test du pipeline CI/CD en local"
echo "=================================="

# Variables
IMAGE_NAME="oc-lettings-site"
CONTAINER_NAME="test-pipeline"
PORT=8001

# Fonction de nettoyage
cleanup() {
    echo "🧹 Nettoyage des ressources..."
    docker stop $CONTAINER_NAME 2>/dev/null || true
    docker rm $CONTAINER_NAME 2>/dev/null || true
    echo "Nettoyage terminé"
}

# Nettoyage initial
cleanup

# Étape 1: Tests et linting
echo ""
echo "Étape 1: Tests et linting"
echo "=============================="

if [ ! -d "venv" ]; then
    echo "Environnement virtuel non trouvé. Veuillez exécuter: python -m venv venv"
    exit 1
fi

source venv/bin/activate

echo "Linting avec flake8..."
if ! flake8 --statistics --show-source; then
    echo "Erreurs de linting détectées"
    exit 1
fi

echo "Exécution des tests avec couverture..."
if ! coverage run -m pytest -v; then
    echo "Tests échoués"
    exit 1
fi

echo "Vérification de la couverture..."
if ! coverage report --fail-under=80; then
    echo "Couverture insuffisante (<80%)"
    exit 1
fi

echo "Tests et linting réussis"

# Étape 2: Build Docker
echo ""
echo "Étape 2: Build Docker"
echo "========================="

echo "Build de l'image Docker..."
if ! docker build -t $IMAGE_NAME:test .; then
    echo "Build Docker échoué"
    exit 1
fi

echo "Image Docker buildée avec succès"

# Étape 3: Test de l'image Docker
echo ""
echo "Étape 3: Test de l'image Docker"
echo "=================================="

echo "Démarrage du container de test..."
if ! docker run -d --name $CONTAINER_NAME -p $PORT:8000 \
    -e DEBUG=False \
    -e SECRET_KEY=test-secret-key-for-testing \
    -e ALLOWED_HOSTS=localhost,127.0.0.1 \
    $IMAGE_NAME:test; then
    echo "Impossible de démarrer le container"
    cleanup
    exit 1
fi

echo "⏳ Attente du démarrage de l'application..."
sleep 10

echo "Test de santé de l'application..."
if curl -f http://localhost:$PORT/ > /dev/null 2>&1; then
    echo "Application accessible sur http://localhost:$PORT/"
    
    # Test des autres endpoints
    if curl -f http://localhost:$PORT/lettings/ > /dev/null 2>&1; then
        echo "Endpoint /lettings/ accessible"
    else
        echo "Endpoint /lettings/ non accessible"
    fi
    
    if curl -f http://localhost:$PORT/profiles/ > /dev/null 2>&1; then
        echo "Endpoint /profiles/ accessible"
    else
        echo "Endpoint /profiles/ non accessible"
    fi
else
    echo "Application non accessible"
    echo "Logs du container:"
    docker logs $CONTAINER_NAME
    cleanup
    exit 1
fi

# Nettoyage final
cleanup

# Résumé
echo ""
echo "Pipeline testé avec succès !"
echo "==============================="
echo "Tests et linting: OK"
echo "Build Docker: OK"
echo "Test de l'image: OK"
echo ""
echo "Le pipeline est prêt pour la production !"
echo "Pour pousser vers GitHub et déclencher le pipeline:"
echo "   git add ."
echo "   git commit -m 'feat: ajout pipeline CI/CD complet'"
echo "   git push origin main"