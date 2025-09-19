"""
Configuration du service Sentry pour le monitoring et la gestion d'erreurs.
"""
import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration


def configure_sentry():
    """
    Configure Sentry avec les paramètres définis par les variables d'environnement.

    Variables d'environnement utilisées:
    - SENTRY_DSN: Data Source Name de Sentry
    - SENTRY_LOG_LEVEL: Niveau minimum de log (défaut: INFO)
    - SENTRY_EVENT_LEVEL: Niveau pour créer des événements Sentry (défaut: ERROR)
    - SENTRY_TRACES_SAMPLE_RATE: Taux d'échantillonnage des traces (défaut: 0.1)
    - SENTRY_ENVIRONMENT: Environnement de déploiement (défaut: development)
    - SENTRY_RELEASE: Version de l'application (défaut: unknown)
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
