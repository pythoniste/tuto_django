from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as gettext

from .models import Player, Game


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['page_title'] = gettext('Home')
        data['nb_players'] = Player.objects.count()
        data['best_players'] = Player.objects.order_by("-score")[:5]
        data['nb_games'] = Game.objects.count()
        return data
