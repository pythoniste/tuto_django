from behave import given, then
from hamcrest import assert_that, equal_to, starts_with

from django.test import override_settings
from app.factories import PlayerFactory


def aux_to_bool(string: str) -> bool:
    conversion = {"does": True, "doesn't": False}

    return conversion[string]


@given("It {aux} have an avatar")
@then("It {aux} have an avatar")
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
def step_impl(context, aux):
    if aux_to_bool(aux):
        assert_that(context.player.avatar.name, starts_with("app/player/avatar/"))
    else:
        assert_that(context.player.avatar.name, equal_to(None))
