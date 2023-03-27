from django.apps import AppConfig


class NhlDatabaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NHL_Database'

    def ready(self):
        from . import scheduler
        updater.start()
