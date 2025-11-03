# import json
from datetime import timedelta

from rest_framework.test import APITestCase
from rest_framework import status

from ..models import Game


class GamesAPITest(APITestCase):

    __test__ = False
    url_prefix=None

    fixtures = ["auth_data", "test_data"]

    @staticmethod
    def format_duration(delta: timedelta | None) -> None | str:
        raise NotImplementedError

    @classmethod
    def get_list_expected_results(cls):
        raise NotImplementedError

    def test_list_games(self):
        url = f"/api-{self.url_prefix}/games/"

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), self.get_list_expected_results())

        # with open("test_gauche.json", "w") as f:
        #     json.dump(response.json(), f, indent=4)
        # with open("test_droit.json", "w") as f:
        #     json.dump(self.get_list_expected_results(), f, indent=4)


class DRFGamesAPITest(GamesAPITest):

    __test__ = True
    url_prefix="drf"

    @staticmethod
    def format_duration(delta: timedelta | None) -> None | str:
        if delta is None:
            return None

        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if days:
            return f"{days} {hours:02}:{minutes:02}:{seconds:02}"
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    @classmethod
    def get_list_expected_results(cls):
        return [
            {
                'name': game.name,
                'description': game.description,
                'duration': cls.format_duration(game.duration),
                'status': game.status,
                'level': game.level,
                'genre': game.genre.name if game.genre else None,
                'question_set': [
                    {
                        'text': question.text,
                        'points': question.points,
                        'order': question.order,
                        'answer_set': [
                            {
                                'text': answer.text,
                                'points': answer.points,
                                'order': answer.order
                            }
                            for answer in question.answer_set.all()
                        ],
                    }
                    for question in game.question_set.all()
                ],
            }
            for game in Game.objects.all()
        ]



class NinjaGamesAPITest(GamesAPITest):

    __test__ = True
    url_prefix="ninja"

    @staticmethod
    def format_duration(delta: timedelta | None) -> None | str:
        if delta is None:
            return None

        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        return f'P{days}DT{hours:02}H{minutes:02}M{seconds:02}S'

    @classmethod
    def get_list_expected_results(cls):
        return [
            {
                'name': game.name,
                'duration': cls.format_duration(game.duration),
                'status': game.status,
                'level': game.level,
                'question_set': [
                    {
                        'text': question.text,
                        'points': question.points,
                        'order': question.order,
                        'answer_set': [
                            {
                                'text': answer.text,
                                'points': answer.points,
                                'order': answer.order
                            }
                            for answer in question.answer_set.all()
                        ],
                    }
                    for question in game.question_set.all()
                ],
            }
            for game in Game.objects.all()
        ]
