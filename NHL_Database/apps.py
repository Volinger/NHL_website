from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class NhlDatabaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NHL_Database'

    def ready(self):
        from . import scheduler
        logger.info('test')
        scheduler.start()
