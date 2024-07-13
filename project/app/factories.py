from functools import partial
from datetime import date

import factory

from app.tests.factories import UserFactory
from .models import Player


Faker = partial(factory.Faker, locale="fr_FR")


class PlayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Player

    user = factory.SubFactory(UserFactory)

    description = Faker("paragraph", nb_sentences=1)
    score = Faker("pyint", min_value=50, max_value=100)
    subscription_date = Faker("date_between_dates", date_start=date(2022, 1, 1), date_end=date(2023, 12, 31))
    profile_activated = True
