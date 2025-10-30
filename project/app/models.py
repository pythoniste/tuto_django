from functools import partial
from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as gettext

from martor.models import MartorField
from mptt.models import MPTTModel, TreeForeignKey
from polymorphic.models import PolymorphicModel


from .enums import GameLevel, GameStatus
from .managers import (
    PlayerManager,
    GameManager,
    QuestionManager,
    AnswerManager,
    PlayManager,
    GenreManager,
    StatGameManager,
)
from .mixins import (
    OrderingMixin,
    TrackingMixin,
)


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


class Player(TrackingMixin, PolymorphicModel):

    objects = PlayerManager()

    user = models.OneToOneField(
        verbose_name = gettext("user"),
        related_name = "player",
        to = settings.AUTH_USER_MODEL,
        null = False,
        db_index = True,
        on_delete = models.PROTECT,
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
        return self.user.username

    def natural_key(self) -> tuple[str]:
        return (self.user.username,)
    natural_key.dependencies = ["auth.user"]

    class Meta:  # pylint: disable=too-few-public-methods
        """Test Meta class"""

        verbose_name = gettext("player")
        verbose_name_plural = gettext("players")
        ordering = ("user__username",)


class Guest(Player):
    """Player invited by another player."""

    invited_by = models.ForeignKey(
        verbose_name=gettext("invited by"),
        related_name="invited_by_set",
        to=Player,
        blank=False,
        null=False,
        db_index=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.player_ptr.user.username

    def natural_key(self) -> tuple[str]:
        return (self.player_ptr.user.username,)
    natural_key.dependencies = ["app.player", "auth.user"]

    class Meta:  # pylint: disable=too-few-public-methods
        """Test Meta class"""

        verbose_name = gettext("guest")
        verbose_name_plural = gettext("guests")
        ordering = ("user__username",)


class Subscriber(Player):
    """Player that pays a subscription."""

    registration_date= models.DateTimeField(
        verbose_name=gettext("First registration date"),
    )

    sponsor = models.ForeignKey(
        verbose_name=gettext("sponsor"),
        related_name="sponsored_set",
        to=Player,
        blank=False,
        null=False,
        db_index=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.player_ptr.user.username

    def natural_key(self) -> tuple[str]:
        return (self.player_ptr.user.username,)
    natural_key.dependencies = ["app.player", "auth.user"]

    class Meta:  # pylint: disable=too-few-public-methods
        """Test Meta class"""

        verbose_name = gettext("subscriber")
        verbose_name_plural = gettext("subscribers")
        ordering = ("user__username",)


class TeamMate(Player):

    registration_date= models.DateTimeField(
        verbose_name=gettext("First registration date"),
    )

    team_member_date= models.DateTimeField(
        verbose_name=gettext("First membership date"),
    )

    def __str__(self):
        return self.player_ptr.user.username

    def natural_key(self) -> tuple[str]:
        return (self.player_ptr.user.username,)
    natural_key.dependencies = ["app.player", "auth.user"]

    class Meta:  # pylint: disable=too-few-public-methods
        """Test Meta class"""

        verbose_name = gettext("team mate")
        verbose_name_plural = gettext("team mates")
        ordering = ("user__username",)


class GameMaster(Player):

    registration_date= models.DateTimeField(
        verbose_name=gettext("First registration date"),
    )

    team_member_date= models.DateTimeField(
        verbose_name=gettext("First membership date"),
    )

    def __str__(self):
        return self.player_ptr.user.username

    def natural_key(self) -> tuple[str]:
        return (self.player_ptr.user.username,)
    natural_key.dependencies = ["app.player", "auth.user"]

    class Meta:  # pylint: disable=too-few-public-methods

        verbose_name = gettext("game master")
        verbose_name_plural = gettext("game masters")
        ordering = ("user__username",)


class Genre(MPTTModel):
    objects = GenreManager()

    name = models.CharField(
        verbose_name=gettext("name"),
        max_length=50,
        unique=True,
    )

    parent = TreeForeignKey(
        verbose_name=gettext("parent"),
        related_name='children',
        to='self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return self.name

    @property
    def deep_label(self):
        return "\u2003" * ((self.get_level() - 1) * 2 - 1) + (self.get_level() and "\u2514\u2500" or "") + self.name

    def natural_key(self) -> tuple[str]:
        return (self.name,)

    class MPTTMeta:
        verbose_name = gettext("genre")
        verbose_name_plural = gettext("genres")
        order_insertion_by = ['name']


class Game(TrackingMixin, models.Model):

    objects = GameManager()

    name = models.CharField(
        verbose_name=gettext("name"),
        max_length=32,
        blank=False,
        db_index=True,
        unique=True,
    )

    description = MartorField(
        verbose_name=gettext("description"),
    )

    slug = models.SlugField(
        max_length=36,
        blank=False,
        db_index=True,
    )

    master = models.ForeignKey(
        verbose_name = gettext("master"),
        related_name = "own_game_set",
        to = GameMaster,
        blank = True,
        null = True,
        db_index = True,
        on_delete = models.SET_NULL,
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

    genre = models.ForeignKey(
        verbose_name=gettext("genre"),
        related_name="game_set",
        to=Genre,
        null=True,
        db_index=True,
        on_delete=models.CASCADE,
    )

    duration = models.DurationField(
        verbose_name=gettext("duration"),
        blank=True,
        null=True,
    )

    highlight = models.BooleanField(
        verbose_name=gettext("highlight"),
        null=False,
        default=False,
    )

    emphasize = models.BooleanField(
        verbose_name=gettext("emphasize"),
        null=False,
        default=False,
    )

    advertise = models.BooleanField(
        verbose_name=gettext("advertise"),
        null=False,
        default=False,
    )

    recommend = models.BooleanField(
        verbose_name=gettext("recommend"),
        null=False,
        default=False,
    )

    @classmethod
    def generate_slug(cls, name):
        base_slug = slugify(name)
        existing_suffixes = [
            g.slug[len(base_slug) + 1:]
            for g in Game.objects.filter(slug__startswith=base_slug).all()
        ]

        if len(existing_suffixes) == 0:
            return base_slug

        if "" in existing_suffixes:
            existing_suffixes.remove("")
        existing_suffixes.append(1)

        last_number = max(int(suffix) for suffix in existing_suffixes)
        suffix = str(f"-{last_number + 1}")
        return base_slug + suffix

    def __str__(self):
        return self.name

    def natural_key(self) -> tuple[str]:
        return (self.name,)

    class Meta:  # pylint: disable=too-few-public-methods
        """Test Meta class"""

        verbose_name = gettext("game")
        verbose_name_plural = gettext("games")
        ordering = ("name",)


class Question(TrackingMixin, OrderingMixin, models.Model):

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

    def __str__(self):
        return self.text[:47] + "[…]" if len(self.text) > 50 else self.text

    def natural_key(self) -> tuple[str, str]:
        return self.game.name, self.text
    natural_key.dependencies = ["app.game"]

    class Meta:  # pylint: disable=too-few-public-methods
        """Test Meta class"""

        verbose_name = gettext("question")
        verbose_name_plural = gettext("questions")
        ordering = ("game_id", "order")
        indexes = [
            models.Index(
                fields=["game_id", "text"],
                name="question_natural_key_index"),
            models.Index(
                fields=["game_id", "order"],
                name="question_ordering_index"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["game_id", "text"],
                name="question_natural_key_constraint"
            ),
        ]


class Answer(TrackingMixin, OrderingMixin, models.Model):

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

    def __str__(self):
        return self.text[:47] + "[…]" if len(self.text) > 50 else self.text

    def natural_key(self) -> tuple[str, str, str]:
        return self.question.game.name, self.question.text, self.text
    natural_key.dependencies = ["app.game", "app.question"]

    class Meta:  # pylint: disable=too-few-public-methods
        """Test Meta class"""

        verbose_name = gettext("answer")
        verbose_name_plural = gettext("answers")
        ordering = ("question_id", "order",)
        indexes = [
            models.Index(
                fields=["question_id", "text"],
                name="answer_natural_key_index"),
            models.Index(
                fields=["question_id", "order"],
                name="answer_ordering_index"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["question_id", "text"],
                name="answer_natural_key_constraint"
            ),
        ]


class Play(TrackingMixin, models.Model):

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

    def natural_key(self) -> tuple[str, str]:
        return self.player.natural_key() + self.game.natural_key()
    natural_key.dependencies = ["app.game"]

    class Meta:  # pylint: disable=too-few-public-methods
        """Test Meta class"""

        verbose_name = gettext("play")
        verbose_name_plural = gettext("plays")
        ordering = ("player", "game")
        indexes = [
            models.Index(
                fields=["player", "game"],
                name="play_natural_key_index"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["player", "game"],
                name="play_natural_key_constraint"
            ),
        ]


class StatGame(Game):
    class Meta:
        proxy=True
        verbose_name = gettext("stat games")
        verbose_name_plural = gettext("stats games")

    objects = StatGameManager()

    # @property
    # def nb_players(self):
    #     return self.play.count()
