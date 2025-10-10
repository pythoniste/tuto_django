from django.db import models
from django.utils.translation import gettext_lazy as gettext


__all__ = (
    "GameStatus",
    "GameLevel",
)


class GameStatus(models.TextChoices):
    """Statuses of a game"""

    DRAFT = "draft", gettext("draft")
    READY = "ready", gettext("ready")
    ONGOING = "ongoing", gettext("ongoing")
    DONE = "done", gettext("done")


class GameLevel(models.IntegerChoices):
    """Level of difficulty of a game"""

    EASY = 1, gettext("easy")
    MEDIUM = 2, gettext("medium")
    HARD = 3, gettext("hard")
    EXTREME = 4, gettext("extreme")
    NIGHTMARE = 5, gettext("nightmare")
