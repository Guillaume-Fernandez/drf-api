from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "common"
    
    def ready(self):
        from .permissions import create_groups
        create_groups()