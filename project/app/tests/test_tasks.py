from django.test import TestCase

from ..tasks import create_avatar
from ..factories import PlayerFactory


class PlayerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.player = PlayerFactory.create()

    def test_create_avatar(self):
        self.assertIsNone(self.player.avatar.name)
        with self.assertRaisesMessage(ValueError, "The 'avatar' attribute has no file associated with it."):
            self.assertIsNone(self.player.avatar.path)

        create_avatar(self.player.pk)

        self.player.refresh_from_db()
        self.assertIn("app/player/avatar/", self.player.avatar.name)
        self.assertIn("app/player/avatar/", self.player.avatar.path)
