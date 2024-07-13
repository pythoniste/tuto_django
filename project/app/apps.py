from importlib import import_module

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as gettext


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    verbose_name = gettext("My app")

    def ready(self):
        """start handling signals"""
        import_module(f"{self.name}.signals")
