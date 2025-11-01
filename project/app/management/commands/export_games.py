import csv

from django.core.management.base import BaseCommand
from django.utils.translation import gettext

from app.models import Game
from app.serializers import GameSerializer


class Command(BaseCommand):
    help = gettext("Export Games to CSV")

    def add_arguments(self, parser):
        # Add optional "game_name" argument to filter export by game name
        parser.add_argument(
            "--game-name",
            type=str,
            help=gettext("Export data for a specific game (by name)"),
        )

    def handle(self, *args, **kwargs):
        game_name = kwargs.get("game_name", None)
        data = []

        if game_name is not None:
            try:
                games = [Game.objects.get_by_natural_key(game_name=game_name)]
                filename = f"exports/{game_name}_export.csv"
            except Game.DoesNotExist:
                self.stdout.write(self.style.ERROR(gettext(f"The game {game_name} does not exists!")))
                return
        else:
            filename = "exports/games_export.csv"
            games = Game.objects.all()

        for game in games:
            game_data = GameSerializer(game)
            for question_data in game_data["question_set"].value:
                for answer_data in question_data["answer_set"]:
                    data.append(
                        {f"game__{field_name}": value for field_name, value in list(game_data.data.items())[:-1]}
                        |
                        {f"question__{field_name}": value for field_name, value in list(question_data.items())[:-1]}
                        |
                        {f"answer__{field_name}": value for field_name, value in answer_data.items()}
                    )

        if len(data) == 0:
            self.stdout.write(self.style.NOTICE(gettext("There is no data to export!")))

        with open(filename, mode="w") as file:
            writer = csv.DictWriter(file, dialect=csv.unix_dialect, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

        self.stdout.write(self.style.SUCCESS(gettext("Data exported successfully!")))
