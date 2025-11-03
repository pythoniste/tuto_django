from functools import partial
from datetime import date, datetime, timedelta
from random import randint
from zoneinfo import ZoneInfo

from django.contrib.auth import get_user_model
from django.utils.timezone import now

import factory

from .models import Player, Guest, Subscriber, TeamMate, GameMaster, Game, Genre
from .enums import GameStatus, GameLevel


User = get_user_model()
zone_info = ZoneInfo("Europe/Paris")

Faker = partial(factory.Faker, locale="fr_FR")


__all__ = [
    "UserFactory",
    "AdminFactory",
    "GuestFactory",
    "SubscriberFactory",
    "TeamMateFactory",
    "GameMasterFactory",
    "GameFactory",
]


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda x: f"user_{x:02}")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = factory.LazyAttribute(lambda x: f"{x.first_name}.{x.last_name}@example.com")
    password = factory.PostGenerationMethodCall('set_password', 'Us3r')

    is_superuser = False
    is_staff = True
    is_active = True


class AdminFactory(UserFactory):

    username = factory.Sequence(lambda x: f"admin_{x:02}")
    password = factory.PostGenerationMethodCall('set_password', 'adm1n')

    is_superuser = True


class PlayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Player

    user = factory.SubFactory(UserFactory)

    score = Faker("pyint", min_value=50, max_value=250)
    subscription_date = Faker("date_between_dates", date_start=date(2022, 1, 1), date_end=date(2025, 12, 31))
    profile_activated = True


class GuestFactory(PlayerFactory):
    class Meta:
        model = Guest

    invited_by = factory.SubFactory(PlayerFactory)


class SubscriberFactory(PlayerFactory):
    class Meta:
        model = Subscriber

    registration_date = Faker("date_time_this_decade", tzinfo=zone_info)
    sponsor = factory.SubFactory(PlayerFactory)


class TeamMateFactory(PlayerFactory):
    class Meta:
        model = TeamMate

    registration_date = Faker("date_time_this_decade", tzinfo=zone_info)
    team_member_date = factory.LazyFunction(lambda: now() - timedelta(days=randint(1, 50)))


class GameMasterFactory(PlayerFactory):
    class Meta:
        model = GameMaster

    registration_date = Faker("date_time_this_decade", tzinfo=zone_info)
    team_member_date = factory.LazyAttribute(lambda x: x.registration_date + timedelta(days=randint(50, 100)))


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game

    name = Faker("word")
    description = Faker("paragraph", nb_sentences=1)
    master = factory.SubFactory(GameMasterFactory)
    status = factory.Iterator(GameStatus)
    level = factory.Iterator(GameLevel)
    genre = factory.Iterator(Genre.objects.all())
    highlight = Faker("pybool")
    emphasize = Faker("pybool")
    advertise = Faker("pybool")
    recommend = Faker("pybool")
