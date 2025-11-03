from datetime import date, timedelta

from django.db.models.signals import pre_save, post_save
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils.timezone import now

from unittest import mock
from factory.django import mute_signals

from ..models import GameMaster
from ..factories import UserFactory, AdminFactory


class GameMasterTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory.create()

    @mute_signals(pre_save, post_save)
    def test_model_with_minimal_data_without_signals(self):
        start_datetime = now()
        player = GameMaster.objects.create(
            user=self.user,
            profile_activated=False,
            registration_date=start_datetime,
            team_member_date=start_datetime,
        )
        stop_datetime = now()
        self.assertEqual(player.user, self.user)
        self.assertEqual(player.score, 0)
        self.assertGreater(player.created_at, start_datetime)
        self.assertLess(player.created_at, stop_datetime)
        self.assertGreater(player.updated_at, start_datetime)
        self.assertLess(player.updated_at, stop_datetime)
        self.assertIsNone(player.subscription_date)
        self.assertEqual(player.registration_date, start_datetime)
        self.assertEqual(player.team_member_date, start_datetime)
        self.assertFalse(player.profile_activated)
        self.assertIsNone(player.signed_engagement.name)
        self.assertIsNone(player.avatar.name)

    @mute_signals(pre_save, post_save)
    def test_model_without_user(self):
        with self.assertRaisesMessage(
            IntegrityError,
            """null value in column "user_id" of relation "app_player" violates not-null constraint""",
        ):
            GameMaster.objects.create(
                profile_activated=False,
                registration_date=now(),
                team_member_date=now(),
            )

    @mock.patch.object(post_save, "send")
    def test_model_nominal(self, mock_send):
        date_subscription = date.today() - timedelta(days=34)
        registration_date = now() - timedelta(days=28)
        team_member_date = now() - timedelta(days=10)
        start_datetime = now()
        player = GameMaster.objects.create(
            user=self.user,
            score=42,
            subscription_date=date_subscription,
            profile_activated=True,
            registration_date=registration_date,
            team_member_date=team_member_date,
        )
        stop_datetime = now()
        self.assertEqual(player.user, self.user)
        self.assertEqual(player.score, 42)
        self.assertGreater(player.created_at, start_datetime)
        self.assertLess(player.created_at, stop_datetime)
        self.assertGreater(player.updated_at, start_datetime)
        self.assertLess(player.updated_at, stop_datetime)
        self.assertEqual(player.subscription_date, date_subscription)
        self.assertTrue(player.profile_activated)
        self.assertIsNone(player.signed_engagement.name)
        self.assertIsNone(player.avatar.name)
        self.assertEqual(player.registration_date, registration_date)
        self.assertEqual(player.team_member_date, team_member_date)
        mock_send.assert_called_once_with(
            sender=GameMaster,
            instance=player,
            created=True,
            update_fields=None,
            raw=False,
            using="default",
        )
