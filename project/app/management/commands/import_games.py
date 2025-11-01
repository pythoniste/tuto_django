import csv
import pathlib

from django.core.management.base import BaseCommand
from django.db.models.signals import post_save, Signal
from django.utils.translation import gettext

from app.models import Game, Question, Answer, Genre
from app.signals import game_create_first_questions, question_create_first_answers

class Command(BaseCommand):
    help = gettext("Import Games from CSV")

    def add_arguments(self, parser):
        # Add optional "game_name" argument to filter export by game name
        parser.add_argument(
            "--game-name",
            type=str,
            help=gettext("Import data for a specific game (by name)"),
        )

    def handle(self, *args, **kwargs):
        game_name = kwargs.get("game_name", None)
        data = []

        if game_name is not None:
            filename = pathlib.Path(f"exports/{game_name}_export.csv")
            if not filename.exists():
                self.stdout.write(self.style.ERROR(gettext(f"The file {filename} does not exists!")))
                return
        else:
            filename = "exports/games_export.csv"

        with open(filename) as file:
            reader = csv.DictReader(file, dialect=csv.unix_dialect)
            data = list(reader)

        old_game_datum = old_question_datum = {}
        game = question = None

        post_save.disconnect(
            game_create_first_questions,
            sender=Game,
            dispatch_uid="game_create_first_questions"
        )
        post_save.disconnect(
            question_create_first_answers,
            sender=Question,
            dispatch_uid="question_create_first_answers"
        )

        for datum in data:
            game_datum = {
                k.split("__", 1)[-1]: v
                for k, v in datum.items()
                if k is not None and k.startswith("game__")
            } | {
                "genre": Genre.objects.get_by_natural_key(name=datum["game__genre"])
            }
            question_datum = {
                k.split("__", 1)[-1]: v
                for k, v in datum.items()
                if k is not None and k.startswith("question__")
            }
            answer_datum = {
                k.split("__", 1)[-1]: v
                for k, v in datum.items()
                if k is not None and k.startswith("answer__")
            }
            if game_datum != old_game_datum:
                game, _ = Game.objects.get_or_create(
                    name=game_datum.pop("name"),
                    defaults=game_datum,
                )
                old_game_datum = game_datum

            if question_datum != old_question_datum:
                question, _ = Question.objects.get_or_create(
                    game_id=game.pk,
                    text=question_datum.pop("text"),
                    defaults=question_datum,
                )
                old_question_datum = question_datum

            Answer.objects.get_or_create(
                question_id=question.pk,
                text=answer_datum.pop("text"),
                defaults=answer_datum,
            )
        self.stdout.write(self.style.SUCCESS(gettext("Data imported successfully!")))
