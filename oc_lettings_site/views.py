"""
Module contenant les vues principales de l'application oc_lettings_site.

Ce module définit la vue principale pour la page d'accueil du site et
les handlers d'erreurs personnalisés avec intégration Sentry.
"""
import logging
import sentry_sdk
from django.shortcuts import render

logger = logging.getLogger('oc_lettings_site')


def home(request):
    """
    Vue pour la page d'accueil du site Orange County Lettings.

    Cette vue affiche la page d'accueil principale avec les liens vers les sections
    lettings et profiles. Enregistre automatiquement les visites pour le monitoring.

    Args:
        request (HttpRequest): L'objet HttpRequest de Django contenant les métadonnées
                              de la requête (headers, IP, session, etc.)

    Returns:
        HttpResponse: Réponse HTTP avec le template 'oc_lettings_site/index.html' rendu
                     contenant les liens de navigation principaux

    Raises:
        Exception: Re-lance toute exception survenue pendant le rendu après logging
                  (erreurs de template, problèmes de contexte, etc.)

    Side Effects:
        - Enregistre un log INFO avec l'adresse IP du visiteur
        - En cas d'erreur : enregistre un log ERROR avant de re-lancer l'exception

    Template:
        oc_lettings_site/index.html : Page d'accueil avec navigation

    URL Pattern:
        '' (racine) : Accessible via l'URL racine du site

    Example:
        GET / HTTP/1.1
        -> Affiche la page d'accueil avec liens vers /lettings/ et /profiles/
    """
    logger.info(f"Page d'accueil visitée par {request.META.get('REMOTE_ADDR', 'IP inconnue')}")

    try:
        return render(request, 'oc_lettings_site/index.html')
    except Exception as e:
        logger.error(f"Erreur lors du rendu de la page d'accueil: {str(e)}")
        raise


def handler404(request, exception):
    """
    Handler personnalisé pour les erreurs 404 avec logging Sentry.

    Cette vue capture les erreurs 404 et les envoie à Sentry comme événements
    pour permettre le monitoring des pages non trouvées.

    Args:
        request (HttpRequest): Requête HTTP qui a causé l'erreur 404
        exception (Http404): L'exception 404 levée

    Returns:
        HttpResponse: Réponse 404 avec template personnalisé
    """
    try:
        error_message = f"404 - Page non trouvée: {request.path}"
        logger.warning(f"{error_message} - IP: {request.META.get('REMOTE_ADDR', 'inconnue')}")

        # Capturer l'événement dans Sentry avec niveau WARNING (seulement si Sentry configuré)
        try:
            sentry_sdk.capture_message(
                error_message,
                level='warning',
                extra={
                    'path': request.path,
                    'method': request.method,
                    'ip_address': request.META.get('REMOTE_ADDR'),
                    'user_agent': request.META.get('HTTP_USER_AGENT'),
                }
            )
        except Exception:
            # Si Sentry échoue, continuer sans interrompre le handler
            pass

        return render(request, '404.html', status=404)
    except Exception as e:
        # Fallback si le handler échoue complètement
        logger.error(f"Erreur dans handler404: {e}")
        from django.http import HttpResponseNotFound
        return HttpResponseNotFound('<h1>404 - Page non trouvée</h1>')


def handler500(request):
    """
    Handler personnalisé pour les erreurs 500 avec logging Sentry.

    Cette vue capture les erreurs serveur 500 et les envoie à Sentry
    avec un niveau d'erreur élevé pour un suivi prioritaire.

    Args:
        request (HttpRequest): Requête HTTP qui a causé l'erreur 500

    Returns:
        HttpResponse: Réponse 500 avec template personnalisé
    """
    try:
        error_message = f"500 - Erreur serveur interne sur: {request.path}"
        logger.error(f"{error_message} - IP: {request.META.get('REMOTE_ADDR', 'inconnue')}")

        # Capturer l'événement dans Sentry avec niveau ERROR (seulement si Sentry configuré)
        try:
            sentry_sdk.capture_message(
                error_message,
                level='error',
                extra={
                    'path': request.path,
                    'method': request.method,
                    'ip_address': request.META.get('REMOTE_ADDR'),
                    'user_agent': request.META.get('HTTP_USER_AGENT'),
                }
            )
        except Exception:
            # Si Sentry échoue, continuer sans interrompre le handler
            pass

        return render(request, '500.html', status=500)
    except Exception as e:
        # Fallback si le handler échoue complètement
        logger.error(f"Erreur dans handler500: {e}")
        from django.http import HttpResponseServerError
        return HttpResponseServerError('<h1>500 - Erreur serveur interne</h1>')


def test_sentry_404(request):
    """
    Vue de test pour générer une erreur 404 et vérifier Sentry.

    Cette vue permet de tester manuellement la capture des erreurs 404 par Sentry.
    Accessible uniquement en mode DEBUG.

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponseNotFound: Force une erreur 404 pour test
    """
    from django.http import Http404
    from django.conf import settings

    if not settings.DEBUG:
        # En production, ne pas exposer cette vue
        raise Http404("Page non trouvée")

    # Générer une erreur 404 pour test Sentry
    logger.warning("Test Sentry 404 - erreur générée volontairement")
    sentry_sdk.capture_message("Test 404 manuel", level='warning')
    raise Http404("Test 404 pour vérification Sentry")


def test_sentry_500(request):
    """
    Vue de test pour générer une erreur 500 et vérifier Sentry.

    Cette vue permet de tester manuellement la capture des erreurs 500 par Sentry.
    Accessible uniquement en mode DEBUG.

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        None: Lève toujours une exception pour test

    Raises:
        Exception: Exception de test pour vérifier Sentry
    """
    from django.conf import settings

    if not settings.DEBUG:
        # En production, ne pas exposer cette vue
        from django.http import Http404
        raise Http404("Page non trouvée")

    # Générer une erreur 500 pour test Sentry
    logger.error("Test Sentry 500 - erreur générée volontairement")
    sentry_sdk.capture_message("Test 500 manuel", level='error')
    raise Exception("Test exception pour vérification Sentry")


def test_sentry_manual(request):
    """
    Vue de test pour forcer l'envoi manuel vers Sentry.

    Cette vue permet de tester la configuration Sentry en envoyant
    manuellement des événements de différents niveaux.

    Args:
        request (HttpRequest): Requête HTTP

    Returns:
        HttpResponse: Confirmation des envois Sentry
    """
    from django.conf import settings
    from django.http import HttpResponse
    import os

    if not settings.DEBUG:
        from django.http import Http404
        raise Http404("Page non trouvée")

    # Vérifier la configuration Sentry
    sentry_dsn = os.getenv('SENTRY_DSN')
    if not sentry_dsn:
        return HttpResponse("""
        <h1>❌ Sentry non configuré</h1>
        <p>SENTRY_DSN n'est pas défini dans les variables d'environnement</p>
        <p>Créez un fichier .env avec votre DSN Sentry</p>
        """, content_type='text/html')

    # Tests d'envoi Sentry
    results = []

    try:
        # Test 1: Message WARNING (404)
        sentry_sdk.capture_message(
            "Test manuel 404",
            level='warning',
            extra={'test': 'manual_404', 'url': request.path}
        )
        results.append("✅ Message WARNING (404) envoyé")
    except Exception as e:
        results.append(f"❌ Erreur WARNING: {e}")

    try:
        # Test 2: Message ERROR (500)
        sentry_sdk.capture_message(
            "Test manuel 500",
            level='error',
            extra={'test': 'manual_500', 'url': request.path}
        )
        results.append("✅ Message ERROR (500) envoyé")
    except Exception as e:
        results.append(f"❌ Erreur ERROR: {e}")

    try:
        # Test 3: Exception
        try:
            raise ValueError("Test exception manuelle")
        except ValueError as e:
            sentry_sdk.capture_exception(e)
            results.append("✅ Exception capturée et envoyée")
    except Exception as e:
        results.append(f"❌ Erreur exception: {e}")

    html_results = "<br>".join(results)

    return HttpResponse(f"""
    <h1>🔍 Test Sentry Manuel</h1>
    <p><strong>DSN configurée:</strong> {sentry_dsn[:50]}...</p>
    <h2>Résultats:</h2>
    <p>{html_results}</p>
    <p><em>Vérifiez votre dashboard Sentry dans quelques minutes</em></p>
    <hr>
    <a href="/">← Retour accueil</a>
    """, content_type='text/html')
