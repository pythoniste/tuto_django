from datetime import timedelta

from django.test import TestCase

from rest_framework.exceptions import ValidationError

from ..enums import GameLevel, GameStatus
from ..models import Game, Question, Answer, Genre
from ..serializers import GameSerializer, QuestionSerializer, AnswerSerializer
from ..factories import GameFactory


def format_duration(delta: timedelta | None) -> None | str:
    if delta is None:
        return None

    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days:
        return f"{days} {hours:02}:{minutes:02}:{seconds:02}"
    return f"{hours:02}:{minutes:02}:{seconds:02}"


class SerializerTestCase(TestCase):

    def setUp(self):
        self.genre = Genre.objects.create(name="Test")
        self.game = GameFactory(
            genre=self.genre,
        )
        self.question = self.game.question_set.first()
        self.answer = self.question.answer_set.first()


    def test_answer_serializer(self):
        serializer = AnswerSerializer(self.answer)
        data = serializer.data

        self.assertEqual(
            data,
            {
                "text": self.answer.text,
                "points": self.answer.points,
                "order": self.answer.order,
            }
        )

    def test_question_serializer(self):
        serializer = QuestionSerializer(self.question)
        data = serializer.data

        self.assertEqual(
            set(data.keys()),
            {"text", "points", "order", "answer_set"},
        )
        self.assertEqual(data["text"], self.question.text)
        self.assertEqual(data["points"], self.question.points)
        self.assertEqual(data["order"], self.question.order)
        self.assertEqual(len(data["answer_set"]), self.question.answer_set.count())

    def test_game_serializer(self):
        serializer = GameSerializer(self.game)
        data = serializer.data

        self.assertEqual(
            set(data.keys()),
            {"name", "description", "duration", "status", "level", "genre", "question_set"},
        )
        self.assertEqual(data["name"], self.game.name)
        self.assertEqual(data["description"], self.game.description)
        self.assertEqual(data["duration"], format_duration(self.game.duration))
        self.assertEqual(data["status"], self.game.status)
        self.assertEqual(data["level"], self.game.level)
        self.assertEqual(data["genre"], self.game.genre.name)
        self.assertEqual(len(data["question_set"]), self.game.question_set.count())

    def test_game_serializer_with_valid_data(self):
        game_data = {
            "name": "Game 1",
            "description": "A fun game",
            "duration": timedelta(seconds=300),
            "status": GameStatus.DRAFT,
            "level": GameLevel.MEDIUM,
            "genre": self.genre.name,
        }

        serializer = GameSerializer(data=game_data)
        self.assertTrue(serializer.is_valid())

    def test_question_serializer_with_valid_data(self):
        question_data = {
            "text": "Question 1",
            "points": 20,
            "order": 1,
        }

        serializer = QuestionSerializer(data=question_data)
        self.assertTrue(serializer.is_valid())

    def test_answer_serializer_with_valid_data(self):
        answer_data = {
            "text": "Answer 1",
            "points": 20,
            "order": 1
        }

        serializer = AnswerSerializer(data=answer_data)
        self.assertTrue(serializer.is_valid())

    def test_game_serializer_with_invalid_data(self):
        game_data = {
            "name": "Game with a very long name that will not fit the 32 chars limit",
            "description": "A fun game",
            "duration": -300,
            "status": "undefined",
            "level": 10,
            "genre": "New one",
        }

        serializer = GameSerializer(data=game_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            {k: str(v[0]) for k, v in serializer.errors.items()},
            {
                "name": "Assurez-vous que ce champ comporte au plus 32\xa0caractères.",
                "status": "«\xa0undefined\xa0» n'est pas un choix valide.",
                "level": "«\xa010\xa0» n'est pas un choix valide.",
            }
        )

    def test_question_serializer_with_invalid_data(self):
        question_data = {
            "text": "",
            "points": -20,
            "order": -1,
        }

        serializer = QuestionSerializer(data=question_data)
        self.assertFalse(serializer.is_valid())

    def test_answer_serializer_with_invalid_data(self):
        answer_data = {
            "text": "",
            "points": -20,
            "order": -1,
        }

        serializer = AnswerSerializer(data=answer_data)
        self.assertFalse(serializer.is_valid())

    def test_game_serializer_with_nested_valid_data(self):
        game_data = {
            "name": "Game 1",
            "description": "A fun game",
            "duration": timedelta(seconds=300),
            "status": GameStatus.DRAFT,
            "level": GameLevel.MEDIUM,
            "genre": self.genre.name,
            "question_set": [
                {
                    "text": "Question 1",
                    "points": 20,
                    "order": 1,
                    "answer_set": [
                        {
                            "text": "Answer 1",
                            "points": 20,
                            "order": 1,
                        },
                        {
                            "text": "Answer 2",
                            "points": 0,
                            "order": 2,
                        },
                        {
                            "text": "Answer 3",
                            "points": 0,
                            "order": 3,
                        },
                    ]
                },
                {
                    "text": "Question 2",
                    "points": 10,
                    "order": 2,
                    "answer_set": [
                        {
                            "text": "Answer 1",
                            "points": 0,
                            "order": 1,
                        },
                        {
                            "text": "Answer 2",
                            "points": 10,
                            "order": 2,
                        },
                    ]
                },
            ]
        }

        serializer = GameSerializer(data=game_data)
        self.assertTrue(serializer.is_valid())

    def test_game_serializer_with_nested_invalid_data(self):
        game_data = {
            "name": "Game with a very long name that will not fit the 32 chars limit",
            "description": "A fun game",
            "duration": -300,
            "status": "undefined",
            "level": 10,
            "genre": "New one",
            "question_set": [
                {
                    "text": "",
                    "points": -1,
                    "order": -1,
                    "answer_set": [
                        {
                            "text": "",
                            "points": -1,
                            "order": -1
                        },
                    ]
                },
            ]
        }

        serializer = GameSerializer(data=game_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            {k: str(v[0]) for k, v in serializer.errors.items()},
            {
                "name": "Assurez-vous que ce champ comporte au plus 32\xa0caractères.",
                "status": "«\xa0undefined\xa0» n'est pas un choix valide.",
                "level": "«\xa010\xa0» n'est pas un choix valide.",
            }
        )

    def test_game_serializer_with_nested_invalid_question_data(self):
        game_data = {
            "name": "Game with a normal name",
            "description": "A fun game",
            "duration": 300,
            "status": GameStatus.DRAFT,
            "level": GameLevel.MEDIUM,
            "genre": self.genre.name,
            "question_set": [
                {
                    "text": "",
                    "points": -1,
                    "order": -1,
                    "answer_set": [
                        {
                            "text": "",
                            "points": -1,
                            "order": -1
                        }
                    ]
                }
            ]
        }

        serializer = GameSerializer(data=game_data)
        self.assertTrue(serializer.is_valid())
