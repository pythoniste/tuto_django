from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView,
)
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as gettext

from rest_framework import viewsets

from project.ninja import api

from .models import Player, Game, Question, Answer
from .forms import GameForm
from .schemas import GameSchema, MessageSchema
from .serializers import GameSerializer, QuestionSerializer, AnswerSerializer


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


class GameDeleteView(DeleteView):
    model = Game
    success_url = reverse_lazy('game:list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        obj = self.get_object()
        data['page_title'] = str(gettext("Delete Game: {}")).format(obj.name)
        return data


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
    queryset = Game.objects.all()
    return list(queryset)


@api.get("/games/{game_id}", response={200: GameSchema, 404: MessageSchema})
def game_detail(request, game_id: int):
    try:
        return 200, Game.objects.get(pk=game_id)
    except Game.DoesNotExist as exc:
        return 404, MessageSchema(message="Not found")


@api.post("/items", response={201: GameSchema, 422: MessageSchema, 500: MessageSchema})
def game_create(request, game_data: GameSchema):
    try:
        game = Game(
            name=game_data.name,
            duration=game_data.duration,
            status=game_data.status,
            level=game_data.level,
        )
        game.full_clean()
        game.save()
        for question_data in game_data.question_set:
            question = Question(
                game=game,
                text=question_data.text,
                points=question_data.points,
                order=question_data.order,
            )
            question.full_clean()
            question.save()
            answers = [
                Answer(question=question, **answer_data.model_dump())
                for answer_data in question_data.answer_set
            ]
            for answer in answers:
                answer.full_clean()
            Answer.objects.bulk_create(answers)
    except ValidationError as e:
        return 422, MessageSchema(message=str(e))
    except Exception as e:
        return 500, MessageSchema(message=str(e))
    return 201, game
