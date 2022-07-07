from django.apps import AppConfig


class BeergameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'beergame'

    def ready(self):
        import beergame.signals
