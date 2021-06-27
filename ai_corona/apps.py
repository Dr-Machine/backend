from django.apps import AppConfig


class AiCoronaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai_corona'

    def ready(self):
        from CT_LIS import signals
