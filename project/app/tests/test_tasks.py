from django.test import TestCase

from ..tasks import create_avatar
from ..factories import GuestFactory


class PlayerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.player = GuestFactory.create()

    def test_create_avatar(self):
        self.assertIsNone(self.player.avatar.name)
        with self.assertRaisesMessage(ValueError, "The 'avatar' attribute has no file associated with it."):
            self.player.avatar.path

        create_avatar(self.player.pk)

        self.player.refresh_from_db()
        self.assertIn("app/guest/avatar/", self.player.avatar.name)
        self.assertIn("app/guest/avatar/", self.player.avatar.path)
