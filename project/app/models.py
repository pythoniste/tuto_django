from pathlib import Path
from uuid import uuid4

from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as gettext

from .enums import GameStatus, GameLevel
from .managers import (
    PlayerManager,
    GameManager,
    QuestionManager,
    AnswerManager,
    PlayManager,
)


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

    objects = PlayerManager()

    user = models.OneToOneField(
        verbose_name=gettext("user"),
        related_name="player",
        to=settings.AUTH_USER_MODEL,
        null=False,
        db_index=True,
        on_delete=models.PROTECT,
    )

    description = models.TextField(
        verbose_name=gettext("description"),
    )

    score = models.PositiveIntegerField(
        verbose_name=gettext("score"),
        default=0,
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
        default=False,
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
        return self.user.username

    class Meta:  # pylint: disable=too-few-public-methods
        """Test Meta class"""

        verbose_name = gettext("player")
        verbose_name_plural = gettext("players")
        ordering = ("user__username",)


class Game(models.Model):

    objects = GameManager()

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


class Question(models.Model):

    objects = QuestionManager()

    game = models.ForeignKey(
        verbose_name=gettext("game"),
        related_name="question_set",
        to=Game,
        null=False,
        db_index=True,
        on_delete=models.CASCADE,
    )

    text = models.TextField(
        verbose_name=gettext("question content"),
        blank=False,
    )

    points = models.PositiveSmallIntegerField(
        verbose_name=gettext("points"),
    )

    order = models.PositiveSmallIntegerField(
        verbose_name=gettext("order"),
        default=0,
    )

    def __str__(self):
        return self.text[:47] + "[…]" if len(self.text) > 50 else self.text

    class Meta:  # pylint: disable=too-few-public-methods
        """Test Meta class"""

        verbose_name = gettext("question")
        verbose_name_plural = gettext("questions")
        ordering = ("order",)


class Answer(models.Model):

    objects = AnswerManager()

    question = models.ForeignKey(
        verbose_name=gettext("question"),
        related_name="answer_set",
        to=Question,
        null=False,
        db_index=True,
        on_delete=models.CASCADE,
    )

    text = models.TextField(
        verbose_name=gettext("answer content"),
        blank=False,
    )

    points = models.PositiveSmallIntegerField(
        verbose_name=gettext("points"),
        default=0,
    )

    order = models.PositiveSmallIntegerField(
        verbose_name=gettext("order"),
        default=0,
    )

    def __str__(self):
        return self.text[:47] + "[…]" if len(self.text) > 50 else self.text

    class Meta:  # pylint: disable=too-few-public-methods
        """Test Meta class"""

        verbose_name = gettext("answer")
        verbose_name_plural = gettext("answers")
        ordering = ("order",)


class Play(models.Model):

    objects = PlayManager()

    player = models.ForeignKey(
        verbose_name=gettext("player"),
        related_name="play",
        to=Player,
        null=False,
        db_index=True,
        on_delete=models.PROTECT,
    )

    game = models.ForeignKey(
        verbose_name=gettext("game"),
        related_name="play",
        to=Game,
        null=False,
        db_index=True,
        on_delete=models.PROTECT,
    )

    creation_datetime = models.DateTimeField(
        verbose_name=gettext("creation datetime"),
        auto_now_add=True,
    )

    entry_set = models.ManyToManyField(
        verbose_name=gettext("entries"),
        related_name="play_set",
        to=Answer,
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """Test Meta class"""

        verbose_name = gettext("play")
        verbose_name_plural = gettext("plays")
        ordering = ("player", "game")
        unique_together = (
            ("player", "game"),
        )
