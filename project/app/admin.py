from django.contrib import admin

from .models import Player, Game, Question, Answer, Play


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    pass
