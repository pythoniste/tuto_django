from io import StringIO
from pathlib import Path

from django.core.management import call_command
from django.test import TestCase

from ..factories import GameFactory
from ..models import Genre

file_content ="""\
"game__name","game__description","game__duration","game__status","game__level","game__genre","question__text","question__points","question__order","answer__text","answer__points","answer__order"
"{game.name}","{game.description}","","{game.status}","{game.level}","{game.genre.name}","Question 0","0","0","Answer 2","0","0"
"{game.name}","{game.description}","","{game.status}","{game.level}","{game.genre.name}","Question 0","0","0","Answer 1","0","0"
"{game.name}","{game.description}","","{game.status}","{game.level}","{game.genre.name}","Question 0","0","0","Answer 0","0","0"
"{game.name}","{game.description}","","{game.status}","{game.level}","{game.genre.name}","Question 1","0","0","Answer 2","0","0"
"{game.name}","{game.description}","","{game.status}","{game.level}","{game.genre.name}","Question 1","0","0","Answer 1","0","0"
"{game.name}","{game.description}","","{game.status}","{game.level}","{game.genre.name}","Question 1","0","0","Answer 0","0","0"
"""


class AppCommandTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.game = GameFactory.create(
            genre=Genre.objects.create(name="test")
        )
        cls.path = Path(f"exports/{cls.game.name}_export.csv")

    def test_export_games(self):
        self.assertFalse(self.path.exists())

        out = StringIO()
        call_command(
            "export_games",
            game_name=self.game.name,
            stdout=out,
        )

        self.assertIn("Data exported successfully!", out.getvalue())
        self.assertTrue(self.path.exists())

        # self.maxDiff = None
        with open(self.path) as f:
            self.assertEqual(f.read(), file_content.format(game=self.game))

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        if cls.path.exists():
            cls.path.unlink()
