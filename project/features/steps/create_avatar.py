from behave import when, then

from django.test import override_settings
from app.factories import PlayerFactory


@when("a new player is created without an avatar")
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
def step_impl(context):
    context.player = PlayerFactory.create()


@then("the player's avatar is generated")
def step_impl(context):
    context.player.refresh_from_db()
    assert context.player.avatar.name.startswith("app/player/avatar/")
