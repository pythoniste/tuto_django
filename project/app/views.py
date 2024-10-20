
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView,
    FormView,
)
from django.db import transaction
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as gettext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib import messages

from rest_framework import viewsets

from project.ninja import api

from .models import Player, Game, Question, Answer, Play, Entry
from .enums import GameStatus
from .forms import GameForm, PlayForm, PlayFormSet, PlayFormSetHelper
from .serializers import GameSerializer, QuestionSerializer, AnswerSerializer
from .schemas import GameSchema


User = get_user_model()


class GamePlayView(DetailView):
    model = Game
    template_name = "admin/app/game/play.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['app_label'] = "app"
        data['app_verbose_name'] = gettext("My app")
        # data['nb_players'] = Player.objects.count()
        # data['best_players'] = Player.objects.order_by("-score")[:5]
        # data['nb_games'] = Game.objects.count()
        return data


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


class GameUpdateView(UpdateView):
    model = Game
    form_class = GameForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        obj = self.get_object()
        data['page_title'] = str(gettext("Update Player: {}")).format(obj.name)
        return data

    def get_success_url(self):
        return reverse("game:update", kwargs={"pk": self.kwargs["pk"]})
        # return reverse_lazy('game:update', kwargs={'pk': self.object.pk})


class GameCreateView(CreateView):
    model = Game
    form_class = GameForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['page_title'] = gettext("Create a new Player")
        return data

    def get_success_url(self):
        submit = self.request.POST.get("submit")
        if submit == str(gettext("Create and add another")):
            return reverse_lazy('game:create')
        if submit == str(gettext("Create and continue modification")):
            return reverse_lazy('game:update', kwargs={'pk': self.object.pk})
        return reverse_lazy('game:list')


class GameDeleteView(DeleteView):
    model = Game

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        obj = self.get_object()
        data['page_title'] = str(gettext("Delete Player: {}")).format(obj.name)
        return data

    def get_success_url(self):
        return reverse_lazy('game:list')


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


@api.get("/games/", response=list[GameSchema])
def game_list(request):
    queryset = Game.objects.prefetch_related("question_set__answer_set").all()
    return list(queryset)

# def create_play(request, game_pk: int):
#     try:
#         player = request.user.player
#     except AttributeError:
#         content = gettext("Please authenticate to play")
#     except User.player.RelatedObjectDoesNotExist:
#         content = gettext("You do not have a player profile")
#     else:
#         content = f"Player {player}"
#     return HttpResponse(content=content.encode("utf-8"))


def create_play(request, game_pk: int):
    try:
        player = request.user.player
    except AttributeError:
        messages.add_message(request, messages.WARNING, gettext("Please authenticate to play"))
        url = reverse_lazy("login")
    except User.player.RelatedObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, gettext("You do not have a player profile"))
        url = reverse_lazy("game:list")
    else:
        Play.objects.create(player=player, game_id=game_pk)
        url = reverse_lazy("game:list")  # TEMPORAIRE
    return HttpResponseRedirect(url)


class PlayView(UpdateView):
    model = Play
    template_name = "app/play_form.html"
    form_class = PlayForm
    success_url = reverse_lazy("game:list")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # data['helper'] = PlayFormSetHelper
        if self.request.method == "POST":
            data["entry_set"] = PlayFormSet(self.request.POST, instance=self.object)
        else:
            data["entry_set"] = PlayFormSet(instance=self.object)
        data["entry_set"].helper = PlayFormSetHelper()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        entry_set = context["entry_set"]
        with transaction.atomic():
            # for entry in entry_set:
            #     aaa = entry.data
            #     Entry.objects.filter(pk=entry.instance.pk).update(answer=entry.fields["answer"].value)
            if entry_set.is_valid():
                entry_set.save()
            messages.add_message(self.request, messages.WARNING, gettext("Saved."))
            # if entry_set.is_valid():
            #     entry_set.save()
            #     messages.add_message(self.request, messages.SUCCESS, gettext("Saved."))
            # else:
            #     messages.add_message(self.request, messages.ERROR, gettext("An error occurred."))

        return HttpResponseRedirect(self.get_success_url())
