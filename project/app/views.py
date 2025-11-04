from itertools import product

from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView,
)
from django.db import transaction
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as gettext
from django.views.decorators.cache import cache_page

from datatableview.views import DatatableView
from rest_framework import viewsets

from project.ninja import api

from .models import Player, Game, Question, Answer, Genre, Play, Entry
from .forms import GameForm, BulkQuestionAnswerGenerationForm, PlayForm, PlayFormSet, PlayFormSetHelper
from .schemas import GameSchema, MessageSchema
from .serializers import GameSerializer, QuestionSerializer, AnswerSerializer


User = get_user_model()


@method_decorator(cache_page(60 * 15, key_prefix="home_view"), name="dispatch")
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
        if self.request.user.is_authenticated:
            data['plays'] = {play.game_id: play.pk for play in self.request.user.player.play.all()}
        return data


class GameDetailView(DetailView):
    model = Game

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        obj = self.get_object()
        data['page_title'] = str(gettext("Game: {}")).format(obj.name)
        if self.request.user.is_authenticated:
            try:
                data['play'] = self.request.user.player.play.filter(game_id=obj.pk).first()
            except User.player.RelatedObjectDoesNotExist:
                pass
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


class GamePlayView(DetailView):
    model = Game
    template_name = "admin/app/game/play.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['app_label'] = "app"
        data['app_verbose_name'] = gettext("My app")
        return data


class GenreDatatableView(DatatableView):
    queryset = Genre.objects.all()


def bulk_create_questions_answers(request, pk):
    if not Game.objects.filter(pk=pk).exists():
        messages.error(request, "The game you tried to get does not exist.")
        return redirect("game:list")

    if request.method == 'POST':
        form = BulkQuestionAnswerGenerationForm(request.POST)
        if form.is_valid():
            num_questions = form.cleaned_data['num_questions']
            question_prefix = form.cleaned_data['question_prefix']
            num_answers_per_question = form.cleaned_data['num_answers_per_question']
            answer_prefix = form.cleaned_data['answer_prefix']

            questions = Question.objects.bulk_create(
                [
                    Question(game_id=pk, text=f"{question_prefix} {i}", points=i)
                    for i in range(1, num_questions + 1)
                ]
            )

            answers = Answer.objects.bulk_create(
                [
                    Answer(question=question, text=f"{answer_prefix} {i}", points=i)
                    for question, i in product(questions, range(1, num_answers_per_question + 1))
                ]
            )
            messages.success(
                request,
                f"{len(questions)} questions {len(answers)} and answer have been created.",
            )
            return redirect("game:detail", pk=pk)
        else:
            messages.error(request, "Please fix the errors below.")

    else:
        form = BulkQuestionAnswerGenerationForm()

    return render(
        request,
        'app/game_form.html',
        {
            'form': form,
            'game': Game.objects.get(pk=pk),
        },
    )


def create_play(request, pk: int):
    try:
        player = request.user.player
    except AttributeError:
        messages.add_message(request, messages.WARNING, gettext("Please authenticate to play"))
        url = reverse_lazy("login")
    except User.player.RelatedObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, gettext("You do not have a player profile"))
        url = reverse_lazy("game:list")
    else:
        play = Play.objects.create(player=player, game_id=pk)
        # url = reverse_lazy("game:list")  # TEMPORAIRE
        url = reverse_lazy("game:play", kwargs={"pk": play.pk})
    return HttpResponseRedirect(url)


class PlayUpdateView(UpdateView):
    model = Play
    template_name = "app/play_form.html"
    form_class = PlayForm
    success_url = reverse_lazy("game:list")

    def get_object(self, queryset=None):
        return get_object_or_404(Play, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            context["entry_set"] = PlayFormSet(self.request.POST, instance=self.object)
        else:
            context["entry_set"] = PlayFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        entry_set = context["entry_set"]
        with transaction.atomic():
            if entry_set.is_valid():
                entry_set.save()
                messages.add_message(self.request, messages.SUCCESS, gettext("Saved."))
            else:
                messages.add_message(self.request, messages.WARNING, gettext("Please answer all questions."))
                for error in entry_set.errors:
                    messages.add_message(self.request, messages.ERROR, error)
                return self.form_invalid(form)

        return HttpResponseRedirect(self.get_success_url())
