from django.apps import AppConfig

from django.utils.translation import gettext_lazy as gettext


class ExampleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'example'
    verbose_name = gettext("Example app")
