from django.apps import AppConfig


class CheckAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'check_app'

    def ready(self):
        from check_app import signals