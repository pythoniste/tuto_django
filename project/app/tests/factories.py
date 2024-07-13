from functools import partial
import factory

from django.contrib.auth.models import User


Faker = partial(factory.Faker, locale="fr_FR")


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
