from unittest import mock

from django.test import TestCase

from ..models import Player
from ..signals import player_post_save_create_avatar
from ..factories import GuestFactory


class PlayerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.player = GuestFactory.build(pk=1)

    @mock.patch("app.signals.create_avatar.delay")
    def test_player_post_save_create_avatar(self, create_avatar_mock):
        player_post_save_create_avatar(
            sender=Player,
            instance=self.player,
            created=True,
            update_fields=None,
            raw=False,
            using="default",
        )
        create_avatar_mock.assert_called_once_with(1)
