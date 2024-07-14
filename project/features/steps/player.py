from behave import given, when, then

from django.test import override_settings

from app.tests.factories import UserFactory
from app.factories import PlayerFactory


@given("I build a new player")
def step_impl(context):
    context.player = PlayerFactory.build(user=UserFactory.create())


@when("I save the new player")
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
def step_impl(context):
    context.player.save()
    context.player.refresh_from_db()


@when("I create a new player")
@given("I create a new player")
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
def step_impl(context):
    context.player = PlayerFactory.create()
    context.player.refresh_from_db()


@when("I create {nb} new players")
@given("I create {nb} new players")
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
def step_impl(context, nb):
    context.players = PlayerFactory.create_batch(int(nb))
    for player in context.players:
        player.refresh_from_db()
