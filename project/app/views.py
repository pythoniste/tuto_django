from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
)
from django.utils.translation import gettext_lazy as gettext

from .models import Player, Game
from .enums import GameStatus

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['page_title'] = gettext('Home')
        data['nb_players'] = Player.objects.count()
        data['best_players'] = Player.objects.order_by("-score")[:5]
        data['nb_games'] = Game.objects.count()
        return data


class GameListView(ListView):
    model = Game

    # def get_queryset(self):
    #     # return super().get_queryset().filter(status=GameStatus.ONGOING)
    #     return Game.objects.playable()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['page_title'] = gettext("Player's list")
        return data


class GameDetailView(DetailView):
    model = Game

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        obj = self.get_object()
        data['page_title'] = str(gettext("Player: {}")).format(obj.name)
        return data
