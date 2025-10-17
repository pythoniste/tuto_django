from django.contrib import admin
from django.utils.translation import gettext_lazy as gettext

from .models import Player, Game, Question, Answer, Play


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
    )
    list_filter = (
        "profile_activated",
        "subscription_date",
        "score",
    )
    list_display = (
        "user_username",
        "user_first_name",
        "user_last_name",
        "avatar",
        "profile_activated",
        "subscription_date",
        "score",
    )
    list_display_links = (
        "user_username",
        "user_first_name",
        "user_last_name",
    )
    list_editable = (
        "profile_activated",
    )

    @admin.display(description=gettext("username"))
    def user_username(self, obj):
        return obj.user.username

    @admin.display(description=gettext("first name"))
    def user_first_name(self, obj):
        return obj.user.first_name

    @admin.display(description=gettext("last name"))
    def user_last_name(self, obj):
        return obj.user.last_name


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
        "duration",
    )
    list_filter = (
        "status",
        "level",
    )
    list_display = (
        "name",
        "status",
        "duration",
        "level",
        "link",
    )
    list_display_links = (
        "link",
    )
    list_editable = (
        "name",
        "status",
        "duration",
        "level",
    )
    readonly_fields = (
        "link",
    )

    def link(self, obj):
        return gettext("Ouvrir")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    list_display = (
        "player",
        "game",
    )
