from django.db import models
from django.utils.translation import gettext_lazy as gettext


__all__ = (
    "StickerCategory",
)


class StickerCategory(models.TextChoices):
    """Category of statuses"""

    COLOR = "color", gettext("color")
    QUALITY = "quality", gettext("quality")
    SIZE = "size", gettext("size")
