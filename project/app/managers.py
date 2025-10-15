from django.db import models

from .enums import GameStatus, GameLevel


class PlayerManager(models.Manager):

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


class GameManager(models.Manager):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related("question_set", "question_set__answer_set")

    @property
    def playable(self):
        queryset = self.get_queryset()
        return queryset.filter(status=GameStatus.ONGOING)


class QuestionManager(models.Manager):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related("answer_set").select_related("game")


class AnswerManager(models.Manager):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("question__game")


class PlayManager(models.Manager):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("player", "game").prefetch_related("entry_set")
