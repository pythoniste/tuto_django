from functools import partial
from pathlib import Path
from uuid import uuid4

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as gettext


def compute_upload_path(current_object, sub_path, filename) -> str:
    """Describe an uploaded document storage path"""

    today = now()
    return str(
        Path.joinpath(*list(
            map(
                Path,
                (
                    current_object._meta.app_label,  # pylint: disable=protected-access
                    current_object._meta.model_name,  # pylint: disable=protected-access
                    sub_path,
                    str(today.year),
                    str(today.month),
                    str(uuid4()) + Path(filename).suffix)))))


def compute_signed_engagement_path(current_object, filename):
    return compute_upload_path(current_object, "file", filename)


def compute_avatar_path(current_object, filename):
    return compute_upload_path(current_object, "avatar", filename)


class Player(models.Model):

    name = models.CharField(
        verbose_name=gettext("name"),
        max_length=32,
        blank=False,
        # null=False,
        db_index=True,
        unique=True,
    )

    email = models.EmailField(
        verbose_name=gettext("email"),
        blank=True,
        null=True,
        db_index=True,
        unique=True,
    )

    description = models.TextField(
        verbose_name=gettext("description"),
    )

    score = models.PositiveIntegerField(
        verbose_name=gettext("score"),
    )

    creation_datetime = models.DateTimeField(
        verbose_name=gettext("creation datetime"),
        auto_now_add=True,
    )

    last_modification_datetime = models.DateTimeField(
        verbose_name=gettext("last modification datetime"),
        auto_now=True,
    )

    subscription_date = models.DateField(
        verbose_name=gettext("subscription date"),
        blank=True,
        null=True,
    )

    profile_activated = models.BooleanField(
        verbose_name=gettext("profile activated"),
    )

    signed_engagement = models.FileField(
        verbose_name=gettext("signed engagement"),
        max_length=256,
        upload_to=compute_signed_engagement_path,
        null=True,
        blank=True,
    )

    avatar = models.ImageField(
        verbose_name=gettext("avatar"),
        max_length=256,
        upload_to=compute_avatar_path,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:  # pylint: disable=too-few-public-methods
        """Test Meta class"""

        verbose_name = gettext("player")
        verbose_name_plural = gettext("players")
        ordering = ("name",)


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


class Game(models.Model):

    name = models.CharField(
        verbose_name=gettext("name"),
        max_length=32,
        blank=False,
        db_index=True,
        unique=True,
    )

    duration = models.DurationField(
        verbose_name=gettext("duration"),
        blank=True,
        null=True,
    )

    status = models.CharField(
        verbose_name=gettext("status"),
        choices=GameStatus,
        default=GameStatus.DRAFT,
        max_length=8,
        blank=False,
        db_index=True,
    )

    level = models.SmallIntegerField(
        verbose_name=gettext("level"),
        choices=GameLevel,
        blank=True,
        null=True,
        db_index=True,
    )

    def __str__(self):
        return self.name

    class Meta:  # pylint: disable=too-few-public-methods
        """Test Meta class"""

        verbose_name = gettext("game")
        verbose_name_plural = gettext("games")
        ordering = ("name",)
