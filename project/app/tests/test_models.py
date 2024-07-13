from datetime import date, timedelta

from django.db.models.signals import pre_save, post_save
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils.timezone import now

from unittest import mock
from factory.django import mute_signals

from ..models import Player
from .factories import UserFactory
from ..signals import post_save


class PlayerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory.create()

    @mute_signals(pre_save, post_save)
    def test_model_with_minimal_data_without_signals(self):
        start_datetime = now()
        player = Player.objects.create(
            user=self.user,
        )
        stop_datetime = now()
        self.assertEqual(player.user, self.user)
        self.assertEqual(player.score, 0)
        self.assertEqual(player.description, "")
        self.assertGreater(player.creation_datetime, start_datetime)
        self.assertLess(player.creation_datetime, stop_datetime)
        self.assertGreater(player.last_modification_datetime, start_datetime)
        self.assertLess(player.last_modification_datetime, stop_datetime)
        self.assertIsNone(player.subscription_date)
        self.assertFalse(player.profile_activated)
        self.assertIsNone(player.signed_engagement.name)
        self.assertIsNone(player.avatar.name)

    @mute_signals(pre_save, post_save)
    def test_model_without_user(self):
        with self.assertRaisesMessage(
            IntegrityError,
            """null value in column "user_id" of relation "app_player" violates not-null constraint""",
        ):
            Player.objects.create()

    @mock.patch.object(post_save, "send")
    def test_model_nominal(self, mock_send):
        date_subscription = date.today() - timedelta(days=34)
        start_datetime = now()
        player = Player.objects.create(
            user=self.user,
            description="desc",
            score=42,
            subscription_date=date_subscription,
            profile_activated=True,
        )
        stop_datetime = now()
        self.assertEqual(player.user, self.user)
        self.assertEqual(player.score, 42)
        self.assertEqual(player.description, "desc")
        self.assertGreater(player.creation_datetime, start_datetime)
        self.assertLess(player.creation_datetime, stop_datetime)
        self.assertGreater(player.last_modification_datetime, start_datetime)
        self.assertLess(player.last_modification_datetime, stop_datetime)
        self.assertEqual(player.subscription_date, date_subscription)
        self.assertTrue(player.profile_activated)
        self.assertIsNone(player.signed_engagement.name)
        self.assertIsNone(player.avatar.name)
        mock_send.assert_called_once_with(
            sender=Player,
            instance=player,
            created=True,
            update_fields=None,
            raw=False,
            using="default",
        )
