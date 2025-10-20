from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
)
from django.utils.translation import gettext_lazy as gettext

from .models import Player, Game


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data |= {
            'page_title': gettext('Home'),
            'nb_players': Player.objects.count(),
            'best_players': Player.objects.order_by("-score")[:5],
            'nb_games': Game.objects.count(),
        }
        return data


class GameListView(ListView):
    queryset = Game.objects.playable

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['page_title'] = gettext("Games list")
        return data


class GameDetailView(DetailView):
    model = Game

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        obj = self.get_object()
        data['page_title'] = str(gettext("Game: {}")).format(obj.name)
        return data
