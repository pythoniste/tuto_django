from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    UpdateView,
    CreateView,
)
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as gettext

from .models import Player, Game
from .forms import GameForm


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


class AlternativeGameUpdateView(UpdateView):
    model = Game
    fields = (
        "name",
        "duration",
        "status",
        "level",
    )
    success_url = reverse_lazy('game:list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        obj = self.get_object()
        data['page_title'] = str(gettext("Update Game: {}")).format(obj.name)
        return data


class GameUpdateView(UpdateView):
    model = Game
    form_class = GameForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        obj = self.get_object()
        data['page_title'] = str(gettext("Update Game: {}")).format(obj.name)
        return data

    def get_success_url(self):
        return reverse("game:update", kwargs={"pk": self.kwargs["pk"]})
        # return reverse_lazy('game:update', kwargs={'pk': self.object.pk})


class GameCreateView(CreateView):
    model = Game
    form_class = GameForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['page_title'] = gettext("Create a new game")
        return data

    def get_success_url(self):
        submit = self.request.POST.get("submit")
        if submit == str(gettext("Create and add another")):
            return reverse_lazy('game:create')
        if submit == str(gettext("Create and continue modification")):
            return reverse_lazy('game:update', kwargs={'pk': self.object.pk})
        return reverse_lazy('game:list')
