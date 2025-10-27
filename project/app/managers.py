from django.contrib.postgres.search import TrigramSimilarity
from django.db import models

from mptt.managers import TreeManager
from polymorphic.managers import PolymorphicManager

from .enums import GameStatus, GameLevel


class PlayerManager(PolymorphicManager):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("user")

    @property
    def active(self):
        queryset = self.get_queryset()
        return queryset.filter(
            user__is_active=True,
            subscription_date__isnull=False,
            profile_activated=True,
        )

    def get_by_natural_key(self, user_username: str):
        return self.non_polymorphic().get(user__username=user_username)


class GameManager(models.Manager):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related("question_set", "question_set__answer_set")

    @property
    def playable(self):
        queryset = self.get_queryset()
        return queryset.filter(status=GameStatus.ONGOING)

    def get_by_natural_key(self, game_name: str):
        return self.get(name=game_name)

    def search_by_name(self, game_name: str, *, similarity=0.3):
        return self.annotate(
            similarity=TrigramSimilarity("name", game_name)
        ).filter(
            similarity__gt=similarity
        ).order_by(
            "-similarity"
        )

class QuestionManager(models.Manager):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related("answer_set").select_related("game")

    def get_by_natural_key(self, game_name: str, question_text: str):
        return self.get(
            game__name=game_name,
            text=question_text,
        )


class AnswerManager(models.Manager):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("question__game")

    def get_by_natural_key(self, game_name: str, question_text: str, answer_text: str):
        return self.get(
            question__game__name=game_name,
            question__text=question_text,
            text=answer_text,
        )


class PlayManager(models.Manager):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("player__user", "game").prefetch_related("entry_set")

    def get_by_natural_key(self, user_username, game_name):
        return self.get(
            player__user__username=user_username,
            game__name=game_name,
        )


class GenreManager(TreeManager):

    def get_by_natural_key(self, name: str):
        return self.get(name=name)
