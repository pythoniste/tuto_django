"""Signaux liés à l'application."""

from typing import Any

from django.apps import AppConfig
from django.db.models.signals import (
    pre_save,
    post_save,
    post_delete,
)
from django.dispatch import receiver, Signal
from django.utils.translation import gettext_lazy as gettext

from .models import Game, Question, Answer, Play, Entry


__all__ = [
    "game_create_slug",
]


@receiver(pre_save, sender=Game, dispatch_uid="game_create_slug")
def game_create_slug(
    sender: AppConfig,
    instance: Game,
    raw: bool,
    using: str,
    update_fields: list[str] | None,
    **_: dict[str, Any],
) -> None:
    if raw or instance.slug:
        return

    instance.slug = Game.generate_slug(instance.name)

    if (update_fields is not None) and ("user" not in update_fields):
        update_fields.append("slug")


@receiver(post_save, sender=Game, dispatch_uid="game_create_first_questions")
def game_create_first_questions(
    sender: AppConfig,
    instance: Game,
    created: bool,
    raw: bool,
    using: str,
    update_fields: list[str] | None,
    **_: dict[str, Any],
) -> None:
    if raw or not created:
        return

    questions = Question.objects.bulk_create(
        [
            Question(
                game=instance,
                text=gettext("Question {}".format(i)),
                points=0,
            )
            for i in range(2)
        ]
    )
    for question in questions:
        post_save.send(
            sender=Question,
            instance=question,
            created=True,
            raw=False,
            using=using,
            update_fields=None,
        )


@receiver(post_save, sender=Question, dispatch_uid="question_create_first_answers")
def question_create_first_answers(
    sender: AppConfig,
    instance: Question,
    created: bool,
    raw: bool,
    using: str,
    update_fields: list[str] | None,
    **_: dict[str, Any],
) -> None:
    if raw or not created:
        return

    Answer.objects.bulk_create(
        [
            Answer(
                question=instance,
                text=gettext("Answer {}".format(i)),
                points=0,
            )
            for i in range(3)
        ]
    )


@receiver(post_save, sender=Answer, dispatch_uid="answer_points_consistency_on_save")
def answer_points_consistency_on_save(
    sender: AppConfig,
    instance: Answer,
    created: bool,
    raw: bool,
    using: str,
    update_fields: list[str] | None,
    **_: dict[str, Any],
) -> None:
    if raw:
        return

    if int(instance.points) > int(instance.question.points):
        instance.question.points = int(instance.points)
        instance.question.save(update_fields=["points"])


@receiver(post_delete, sender=Answer, dispatch_uid="answer_points_consistency_on_delete")
def answer_points_consistency_on_delete(
    sender: AppConfig,
    instance: Answer,
    using: str,
    **_: dict[str, Any]
) -> None:

    other_answers = instance.question.answer_set.exclude(pk=instance.pk).all()

    if len(other_answers) == 0:
        instance.question.points = 0
        instance.question.save(update_fields=["points"])
        return

    if (nb_points := max(answer.points for answer in other_answers)) < instance.question.points:
        instance.question.points = nb_points
        instance.question.save(update_fields=["points"])


@receiver(post_save, sender=Play, dispatch_uid="question_create_entries_when_creating_play")
def question_create_entries_when_creating_play(
    sender: AppConfig,
    instance: Question,
    created: bool,
    raw: bool,
    using: str,
    update_fields: list[str] | None,
    **_: dict[str, Any],
) -> None:
    if raw or not created:
        return

    Entry.objects.bulk_create(
        [
            Entry(play=instance, question=question)
            for question in instance.game.question_set.all()
        ]
    )
