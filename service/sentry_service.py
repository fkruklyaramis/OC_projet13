"""
Configuration du service Sentry pour le monitoring et la gestion d'erreurs.
"""
import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration


def configure_sentry():
    """
    Configure et initialise Sentry SDK pour le monitoring et la gestion d'erreurs.

    Cette fonction lit les variables d'environnement pour configurer Sentry avec
    les intégrations Django et logging. Si SENTRY_DSN n'est pas définie, Sentry
    reste désactivé silencieusement.

    Environment Variables:
        SENTRY_DSN (str): Data Source Name de Sentry (URL de configuration)
                         Si absent ou vide, Sentry est désactivé
        SENTRY_LOG_LEVEL (str): Niveau minimum pour capturer les logs
                               Valeurs: DEBUG, INFO, WARNING, ERROR, CRITICAL
                               Défaut: INFO
        SENTRY_EVENT_LEVEL (str): Niveau minimum pour créer des événements Sentry
                                 Valeurs: WARNING, ERROR, CRITICAL
                                 Défaut: ERROR
        SENTRY_TRACES_SAMPLE_RATE (str): Taux d'échantillonnage des traces (0.0-1.0)
                                        Défaut: 0.1 (10% des transactions)
        SENTRY_ENVIRONMENT (str): Environnement de déploiement
                                 Exemples: development, staging, production
                                 Défaut: development
        SENTRY_RELEASE (str): Version/release de l'application pour tracking
                             Défaut: unknown

    Returns:
        None

    Side Effects:
        - Initialise le SDK Sentry globalement
        - Configure les intégrations Django (URLs, middleware, signaux)
        - Configure l'intégration logging (capture automatique des logs)
        - Affiche un message de confirmation ou d'erreur sur stdout

    Integrations:
        - DjangoIntegration: Capture les erreurs Django, URLs comme transactions
        - LoggingIntegration: Capture automatique des logs Python

    Examples:
        >>> import os
        >>> os.environ['SENTRY_DSN'] = 'https://key@sentry.io/project'
        >>> configure_sentry()
        Sentry configuré pour l'environnement: development

        >>> configure_sentry()  # Sans SENTRY_DSN
        SENTRY_DSN non configuré - Sentry désactivé

    Note:
        Cette fonction doit être appelée une seule fois au démarrage de l'application,
        typiquement dans settings.py de Django.
    """
    sentry_dsn = os.getenv('SENTRY_DSN')

    if not sentry_dsn:
        print("SENTRY_DSN non configuré - Sentry désactivé")
        return

    # Configuration de l'intégration de logging avec Sentry
    sentry_logging = LoggingIntegration(
        level=os.getenv('SENTRY_LOG_LEVEL', 'INFO'),
        event_level=os.getenv('SENTRY_EVENT_LEVEL', 'ERROR')
    )

    # Initialisation de Sentry
    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[
            DjangoIntegration(
                transaction_style='url',
                middleware_spans=True,
                signals_spans=True,
            ),
            sentry_logging,
        ],
        # Taux d'échantillonnage des traces de performance
        traces_sample_rate=float(os.getenv('SENTRY_TRACES_SAMPLE_RATE', '0.1')),

        # Envoi des informations personnelles (activé par défaut selon Sentry)
        send_default_pii=True,

        # Configuration de l'environnement
        environment=os.getenv('SENTRY_ENVIRONMENT', 'development'),

        # Version de l'application
        release=os.getenv('SENTRY_RELEASE', 'unknown'),
    )

    print(f"Sentry configuré pour l'environnement: {os.getenv('SENTRY_ENVIRONMENT', 'development')}")
