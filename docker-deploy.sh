#!/bin/bash

# Script pour construire et pousser l'image vers Docker Hub

set -e  # Arrêter le script en cas d'erreur

# Variables à configurer
DOCKER_USERNAME="${DOCKER_USERNAME:-francoiskrukly}"
IMAGE_NAME="oc-lettings-site"
VERSION="${VERSION:-latest}"

# Vérifier que DOCKER_USERNAME est configuré
if [ "$DOCKER_USERNAME" = "votre-username-dockerhub" ]; then
    echo "Erreur : Veuillez configurer votre nom d'utilisateur Docker Hub"
    echo "Usage : DOCKER_USERNAME=francoiskrukly ./docker-deploy.sh"
    echo "Ou modifier la variable DOCKER_USERNAME dans ce script"
    exit 1
fi

echo "Construction de l'image Docker pour production..."
docker build -t $IMAGE_NAME:$VERSION .

echo "Tagging de l'image pour Docker Hub..."
docker tag $IMAGE_NAME:$VERSION $DOCKER_USERNAME/$IMAGE_NAME:$VERSION

# Si VERSION n'est pas "latest", créer aussi un tag latest
if [ "$VERSION" != "latest" ]; then
    docker tag $IMAGE_NAME:$VERSION $DOCKER_USERNAME/$IMAGE_NAME:latest
    echo "Tag 'latest' créé également"
fi

echo "Images créées :"
docker images | grep $IMAGE_NAME

echo ""
echo "Push vers Docker Hub..."
echo "Assurez-vous d'être connecté : docker login"

# Push de l'image
docker push $DOCKER_USERNAME/$IMAGE_NAME:$VERSION

if [ "$VERSION" != "latest" ]; then
    docker push $DOCKER_USERNAME/$IMAGE_NAME:latest
fi

echo ""
echo "Image pushée avec succès sur Docker Hub!"
echo "Disponible à : https://hub.docker.com/r/$DOCKER_USERNAME/$IMAGE_NAME"
echo ""
echo "Pour tester l'image depuis Docker Hub :"
echo "   docker pull $DOCKER_USERNAME/$IMAGE_NAME:$VERSION"
echo "   docker run -p 8002:8000 -e DEBUG=False -e ALLOWED_HOSTS=localhost $DOCKER_USERNAME/$IMAGE_NAME:$VERSION"