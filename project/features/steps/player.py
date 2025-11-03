from behave import given, when, then

from django.test import override_settings

from app.factories import UserFactory, TeamMateFactory, GameMasterFactory, GuestFactory, SubscriberFactory


@given("I build a new {player_type}")
def step_impl(context, player_type):
    if hasattr(context, "game_master"):
        game_master = context.game_master
    else:
        game_master = GameMasterFactory.build()
    match player_type:
        case "game master":
            context.player = GameMasterFactory.build()
        case "player" | "subscriber":
            context.player = SubscriberFactory.build(
                sponsor=game_master
            )
        case "guest":
            context.player = GuestFactory.build(
                invited_by=game_master
            )
        case "team mate":
            context.player = TeamMateFactory.build()
        case _:
            raise NotImplementedError


@when("I save the new {player_type}")
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
def step_impl(context, player_type):
    match player_type:
        case "game master":
            context.player.user.save()
            context.game_master = context.player
        case "player" | "subscriber":
            context.player.user.save()
            context.player.sponsor.user.save()
            context.player.sponsor.save()
            if not hasattr(context, "game_master"):
                context.game_master = context.player.sponsor
        case "guest":
            context.player.user.save()
            context.player.invited_by.user.save()
            context.player.invited_by.save()
            if not hasattr(context, "game_master"):
                context.game_master = context.player.invited_by
            context.player.user.save()
        case "team mate":
            pass
        case _:
            raise NotImplementedError

    context.player.save()
    context.player.refresh_from_db()


@when("I create a new {player_type}")
@given("I create a new {player_type}")
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
def step_impl(context, player_type):
    if not hasattr(context, "game_master"):
        context.game_master = GameMasterFactory.create()
    match player_type:
        case "game master":
            context.game_master = context.player = GameMasterFactory.create()
        case "player" | "subscriber":
            context.player = SubscriberFactory.create(
                sponsor=context.game_master
            )
        case "guest":
            context.player = GuestFactory.create(invited_by=context.game_master)
        case "team mate":
            context.player = TeamMateFactory.create()
        case _:
            raise NotImplementedError
    context.player.refresh_from_db()


@when("I create {nb} new players")
@given("I create {nb} new players")
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
def step_impl(context, nb):
    context.players = SubscriberFactory.create_batch(
        int(nb),
        sponsor=context.game_master,
    )
    for player in context.players:
        player.refresh_from_db()
