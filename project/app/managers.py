from django.db import models

from typing import TYPE_CHECKING

from polymorphic.managers import PolymorphicManager

from .enums import GameStatus, GameLevel

if TYPE_CHECKING:
    from .models import (
        Player,
        Game,
        Question,
        Answer,
    )


class PlayerManager(PolymorphicManager):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("user")

    def get_by_natural_key(self, username: str) -> "Player":
        """Gestion des clés naturelles."""
        return self.get(user__username=username)

    def get_active(self):
        queryset = self.get_queryset()
        return queryset.filter(
            user__is_staff=True,
            user__is_active=True,
            subscription_date__isnull=False,
            profile_activated=True,
        )


class GameManager(models.Manager):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related("question_set")

    def get_by_natural_key(self, name: str) -> "Game":
        """Gestion des clés naturelles."""
        return self.get(name=name)

    def playable(self):
        queryset = super().get_queryset()
        return queryset.filter(status=GameStatus.ONGOING)


class QuestionManager(models.Manager):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related("answer_set").select_related("game")

    def get_by_natural_key(self, game_name: str, text: str) -> "Question":
        """Gestion des clés naturelles."""
        return self.get(game__name=game_name, text=text)


class AnswerManager(models.Manager):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("question__game")

    def get_by_natural_key(self, game_name: str, question_text: str, answer_text: str) -> "Answer":
        """Gestion des clés naturelles."""
        return self.get(
            question__game__name=game_name,
            game__text=question_text,
            text=answer_text,
        )


class PlayManager(models.Manager):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("player").select_related("game").prefetch_related("entry_set")
