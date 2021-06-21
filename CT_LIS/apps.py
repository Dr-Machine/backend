from django.apps import AppConfig


class InferencesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CT_LIS'

    def ready(self):
        from CT_LIS import signals
