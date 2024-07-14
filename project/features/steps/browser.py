from behave import when, given, then
from hamcrest import assert_that, equal_to, starts_with
from bs4 import BeautifulSoup

from django.test import override_settings


@when("I visit '{page_name}'")
@override_settings(DEBUG_TOOLBAR_CONFIG={'SHOW_TOOLBAR_CALLBACK': lambda request: False})
def visit(context, page_name):
    response = context.test.client.get(page_name)
    assert_that(response.status_code, equal_to(200))
    context.response = BeautifulSoup(response.content, 'html.parser')


@then(u'I should see {nb_players} players and {nb_games} games')
def visit(context, nb_players, nb_games):
    response = context.response
    assert_that(
        [tag.get_text() for tag in response.find_all("td")[:4]],
        equal_to(
            [
                "nombre de joueurs",
                nb_players,
                "nombre de parties",
                nb_games,
            ]
        )
    )
