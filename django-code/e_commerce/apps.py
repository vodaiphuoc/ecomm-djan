from django.apps import AppConfig


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'e_commerce'

    def ready(self):
        import e_commerce.signals