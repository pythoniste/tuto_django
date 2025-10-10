from functools import partial
from pathlib import Path
from uuid import uuid4

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as gettext


def compute_upload_path(current_object, filename, sub_path) -> str:
    """Describe an uploaded document storage path"""

    today = now()
    return str(
        Path.joinpath(
            *list(
                map(
                    Path,
                    (
                        current_object._meta.app_label,  # pylint: disable=protected-access
                        current_object._meta.model_name,  # pylint: disable=protected-access
                        sub_path,
                        str(today.year),
                        str(today.month),
                        str(uuid4()) + Path(filename).suffix
                    )
                )
            )
        )
    )


class Player(models.Model):

    name = models.CharField(
        verbose_name=gettext("name"),
        max_length=32,
        blank=False,  # Mandatory field
        # null=False,  # Implicit, because Blank is False
        db_index=True,
        unique=True,
    )

    email = models.EmailField(
        verbose_name=gettext("email"),
        blank=True,  # Optional field
        null=True,  # Because Blank is True, null can be allowed or not (else, blank value will be "")
        db_index=True,
        unique=True,
    )

    score = models.PositiveSmallIntegerField(
        verbose_name=gettext("score"),
        default=0,
    )

    subscription_date = models.DateField(
        verbose_name=gettext("subscription date"),
        blank=True,
        null=True,
    )

    creation_datetime = models.DateTimeField(
        verbose_name=gettext("creation datetime"),
        auto_now_add=True,
    )

    last_modification_datetime = models.DateTimeField(
        verbose_name=gettext("last modification datetime"),
        auto_now=True,
    )

    profile_activated = models.BooleanField(
        verbose_name=gettext("profile activated"),
    )

    avatar = models.ImageField(
        verbose_name=gettext("avatar"),
        max_length=256,
        upload_to=partial(compute_upload_path, sub_path="avatar"),
        null=True,
        blank=True,
    )

    signed_engagement = models.FileField(
        verbose_name=gettext("signed_engagement"),
        max_length=256,
        upload_to=partial(compute_upload_path, sub_path="signed_engagement"),
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

    def __str__(self):
        return self.name

    class Meta:  # pylint: disable=too-few-public-methods
        """Test Meta class"""

        verbose_name = gettext("game")
        verbose_name_plural = gettext("games")
        ordering = ("name",)
